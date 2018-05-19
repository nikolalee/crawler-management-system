#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-22 23:20:39

import socket

from six import iteritems, itervalues
from flask import render_template, request, json,Response

try:
    import flask_login as login
except ImportError:
    from flask.ext import login

from .app import app

index_fields = ['name', 'group', 'status', 'comments', 'rate', 'burst', 'updatetime']


@app.route('/spiderweb/')
def spiderweb_index():
    projectdb = app.config['projectdb']
    projects = sorted(projectdb.get_all(fields=index_fields),
                      key=lambda k: (0 if k['group'] else 1, k['group'] or '', k['name']))
    return render_template("index_spiderweb.html", projects=projects)


@app.route('/spiderweb/queues')
def spiderweb_get_queues():
    def try_get_qsize(queue):
        if queue is None:
            return 'None'
        try:
            return queue.qsize()
        except Exception as e:
            return "%r" % e

    result = {}
    queues = app.config.get('queues', {})
    for key in queues:
        result[key] = try_get_qsize(queues[key])
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


@app.route('/spiderweb/update', methods=['POST', ])
def spiderweb_project_update():
    projectdb = app.config['projectdb']
    project = request.form['pk']
    name = request.form['name']
    value = request.form['value']

    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if name not in ('group', 'status', 'rate'):
        return 'unknown field: %s' % name, 400
    if name == 'rate':
        value = value.split('/')
        if len(value) != 2:
            return 'format error: rate/burst', 400
        rate = float(value[0])
        burst = float(value[1])
        update = {
            'rate': min(rate, app.config.get('max_rate', rate)),
            'burst': min(burst, app.config.get('max_burst', burst)),
        }
    else:
        update = {
            name: value
        }

    ret = projectdb.update(project, update)
    if ret:
        rpc = app.config['scheduler_rpc']
        if rpc is not None:
            try:
                rpc.update_project()
            except socket.error as e:
                app.logger.warning('connect to scheduler rpc error: %r', e)
                return 'rpc error', 200
        return 'ok', 200
    else:
        return 'update error', 500


@app.route('/spiderweb/counter')
def spiderweb_counter():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        return json.dumps({})

    result = {}
    try:
        data = rpc.webui_update()
        for type, counters in iteritems(data['counter']):
            for project, counter in iteritems(counters):
                result.setdefault(project, {})[type] = counter
        for project, paused in iteritems(data['pause_status']):
            result.setdefault(project, {})['paused'] = paused
    except socket.error as e:
        app.logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({}), 200, {'Content-Type': 'application/json'}

    #return json.dumps(result), 200, {'Content-Type': 'application/json'}
    result_json = json.dumps(result)
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/spiderweb/run', methods=['POST', ])
def spiderweb_runtask():
    rpc = app.config['scheduler_rpc']
    if rpc is None:
        print("error")
        return json.dumps({})

    projectdb = app.config['projectdb']
    project = request.form['project']
    project_info = projectdb.get(project, fields=('name', 'group'))
    if not project_info:
        print("no such project.")
        return "no such project.", 404
    if 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    newtask = {
        "project": project,
        "taskid": "on_start",
        "url": "data:,on_start",
        "process": {
            "callback": "on_start",
        },
        "schedule": {
            "age": 0,
            "priority": 9,
            "force_update": True,
        },
    }

    try:
        ret = rpc.newtask(newtask)
    except socket.error as e:
        app.logger.warning('connect to scheduler rpc error: %r', e)
        return json.dumps({"result": False}), 200, {'Content-Type': 'application/json'}
    #return json.dumps({"result": ret}), 200, {'Content-Type': 'application/json'}
    result_json = json.dumps({'result':ret,'status':'ok','code':200})
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/spiderweb/robots.txt')
def spiderweb_robots():
    return """User-agent: *
Disallow: /
Allow: /$
Allow: /spiderweb/debug
Disallow: /spiderweb/debug/*?taskid=*
""", 200, {'Content-Type': 'text/plain'}

@app.route('/spiderweb/delete',methods=['POST',])
def spiderweb_delete():
    project = request.form['project']
    projectdb = app.config['projectdb']
    # resultdb = app.config['resultdb']
    # taskdb = app.config['taskdb']
    projectdb.drop(project)
    # resultdb.drop(project)
    # taskdb.drop(project)
    #return "删除项目 '"+project+"' 成功!!!"
    result_json = json.dumps({'status':'ok','code':200})
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
