#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-02-23 00:19:06


import sys
import time
import socket
import inspect
import datetime
import traceback
from flask import render_template, request, json
import pymysql
from flask import Response
from pyspider.libs import result_dump
import csv

try:
    import flask_login as login
except ImportError:
    from flask.ext import login

from pyspider.libs import utils, sample_handler, dataurl, news, comment, forum
from pyspider.libs.response import rebuild_response
from pyspider.processor.project_module import ProjectManager, ProjectFinder
from .app import app

default_task = {
    'taskid': 'data:,on_start',
    'project': '',
    'url': 'data:,on_start',
    'process': {
        'callback': 'on_start',
    },
}
default_script = inspect.getsource(sample_handler)
default_script_news = inspect.getsource(news)
default_script_comment = inspect.getsource(comment)
default_script_forum = inspect.getsource(forum)



@app.route('/debug/<project>', methods=['GET', 'POST'])
def debug(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    if info:
        script = info['script']
    else:
        script = (default_script
                  .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  .replace('__PROJECT_NAME__', project)
                  .replace('__START_URL__', request.values.get('start-urls') or '__START_URL__'))

    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task

    default_task['project'] = project
    return render_template("debug.html", task=task, script=script, project_name=project)



@app.route('/debug/<project>/get_script_save', methods=['GET', 'POST'])
def spiderweb_debug_get_script_save(project):
    print("hello project")    
    print(request.values)
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    web_type = request.values.get('web-type')
    if info:
        script = info['script']
    else:
        if web_type == "news":
            script = (default_script_news
                      .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                      .replace('__PROJECT_NAME__', project)
                      .replace('__START_URL__', request.values.get('url') or '__START_URL__')
                      .replace('__TITLE_CSS__', request.values.get('title_css') or '__TITLE_CSS__')
                      .replace('__NEXTPAGE_CSS__', request.values.get('nextpage_css') or '__NEXTPAGE_CSS__')
                      .replace('__HREF_CSS__', request.values.get('href_css') or '__HREF_CSS__')
                      .replace('__TIME_CSS__', request.values.get('time_css') or '__TIME_CSS__')
                      .replace('__SRC_CSS__', request.values.get('src_css') or '__SRC_CSS__')
                      .replace('__CONTENT_CSS__', request.values.get('content_css') or '__CONTENT_CSS__')
                      .replace('__NEXTPAGE_FORMAT__', request.values.get('nextpage_format') or '__NEXTPAGE_FORMAT__'))
        elif web_type == "comment":
           script = (default_script_comment
                     .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     .replace('__PROJECT_NAME__', project)
                     .replace('__START_URL__', request.values.get('start_url') or '__START_URL__')
                     .replace('__NEXTPAGE_TAG__',request.values.get('nextpage_tag') or '__NEXTPAGE_TAG__')
                     .replace('__NEXTPAGE_NAME__',request.values.get('nextpage_name') or '__NEXTPAGE_NAME__')
                     .replace('__COMMENT_BOX_CSS__',request.values.get('comment_box_css') or '__COMMENT_BOX_CSS__')
                     .replace('__COMMENT_AUTHOR_CSS__',request.values.get('comment_author_css') or '__COMMENT_AUTHOR_CSS__')
                     .replace('__TIME_CSS__',request.values.get('time_css') or '__TIME_CSS__')
                     .replace('__CONTENT_CSS__',request.values.get('content_css') or '__CONTENT_CSS__')
                     .replace('__HAS_RE_CONTENT_CSS__',request.values.get('has_re_content_css') or '__HAS_RE_CONTENT_CSS__')
                     .replace('__VOTE_CSS__',request.values.get('vote_css') or '__VOTE_CSS__')
                     .replace('__RESPONSE_TYPE__',request.values.get('response_type') or '__RESPONSE_TYPE__')
                     .replace('__RESPONSE_CSS__',request.values.get('response_css') or '__RESPONSE_CSS__')
                     .replace('__RESPONSE_BOX_CSS__',request.values.get('response_box_css') or '__RESPONSE_BOX_CSS__')
                     .replace('__RES_USER_CSS__',request.values.get('res_user_css') or '__RES_USER_CSS__')
                     .replace('__RES_TIME_CSS__',request.values.get('res_time_css') or '__RES_TIME_CSS__')
                     .replace('__RES_CONTENT_CSS__',request.values.get('res_content_css') or '__RES_CONTENT_CSS__')
                     .replace('__IFRAME_ID__',request.values.get('iframe_id ') or '__IFRAME_ID__')
                     .replace('__IS_IFRAME__',request.values.get('isIframe') or '__IS_IFRAME__')
                     .replace('__MORE_TYPE__',request.values.get('more_type') or '__MORE_TYPE__')
                     .replace('__DEEP_NUM__',request.values.get('deep_num') or '__DEEP_NUM__')
                     .replace('__STEP__',request.values.get('step') or '__STEP__'))
        else:
           script = (default_script_forum
                     .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     .replace('__PROJECT_NAME__', project)
                     .replace('__START_URL__', request.values.get('start_url') or '__START_URL__')
                     .replace('__MAIN_NEXTPAGE_TAG__',request.values.get('main_nextpage_tag') or '__MAIN_NEXTPAGE_TAG__')
                     .replace('__NEXTPAGE_KEYWORD__',request.values.get('nextpage_keyword') or '__NEXTPAGE_KEYWORD__')
                     .replace('__NEXTPAGE_TYPE__',request.values.get('nextpage_type') or '__NEXTPAGE_TYPE__')
                     .replace('__MAIN_PAGE_NUM__',request.values.get('main_page_num') or '__MAIN_PAGE_NUM__')
                     .replace('__HREF_CSS__',request.values.get('href_css') or '___HREF_CSS__')
                     .replace('__TITLE_CSS__',request.values.get('title_css') or '__TITLE_CSS__')
                     .replace('__AUTHOR_CSS__',request.values.get('author_css') or '__AUTHOR_CSS__')
                     .replace('__PUBLISH_TIME_CSS__',request.values.get('publish_time_css') or '__PUBLISH_TIME_CSS__')
                     .replace('__CONTENT_CSS__',request.values.get('content_css') or '__CONTENT_CSS__')
                     .replace('__MAIN_STEP__',request.values.get('main_step') or '__MAIN_STEP__')
                     .replace('__SUB_PAGE_NUM__',request.values.get('sub_page_num') or '__SUB_PAGE_NUM__')
                     .replace('__SUB_NEXTPAGE_TAG__',request.values.get('sub_nextpage_tag') or '__SUB_NEXTPAGE_TAG__')
                     .replace('__TIE_BOX_CSS__',request.values.get('tie_box_css') or '__TIE_BOX_CSS__')
                     .replace('__TIE_USER_CSS__',request.values.get('tie_user_css') or '__TIE_USER_CSS__')
                     .replace('__TIE_TIME_CSS__',request.values.get('tie_time_css') or '__TIE_TIME_CSS__')
                     .replace('__TIE_CONTENT_CSS__',request.values.get('tie_content_css') or '__TIE_CONTENT_CSS__')
                     .replace('__SUB_STEP__',request.values.get('sub_step') or '__SUB_STEP__'))
    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task

    default_task['project'] = project
    # return render_template("debug_spiderweb.html", task=task, script=script, project_name=project)
    # projectdb = app.config['projectdb']
    # if not projectdb.verify_project_name(project):
    #     return 'project name is not allowed!', 400
    # script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if project_info:
        info = {
            'script': script,
        }
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 3),
        }
        projectdb.insert(project, info)

    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200
    data = {}    
    data['status'] = 'ok'
    data['code'] = 200
    result_json = json.dumps(data)
    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.before_first_request
def enable_projects_import():
    sys.meta_path.append(ProjectFinder(app.config['projectdb']))


@app.route('/debug/<project>/run', methods=['POST', 'GET'])
def run(project):
    start_time = time.time()
    try:
        print('nice')
        task = utils.decode_unicode_obj(json.loads(request.form['task']))
    except Exception:
        result = {
            'fetch_result': "",
            'logs': u'task json error',
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        #return json.dumps(utils.unicode_obj(result)), \
         #   200, {'Content-Type': 'application/json'}
        result_json = json.dumps({'status':'ok1','code':200})
        resp = Response(result_json)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    print('yes')
    project_info = {
        'name': project,
        'status': 'DEBUG',
        'script': request.form['script'],
    }

    if request.form.get('webdav_mode') == 'true':
        projectdb = app.config['projectdb']
        info = projectdb.get(project, fields=['name', 'script'])
        if not info:
            result = {
                'fetch_result': "",
                'logs': u' in wevdav mode, cannot load script',
                'follows': [],
                'messages': [],
                'result': None,
                'time': time.time() - start_time,
            }
           # return json.dumps(utils.unicode_obj(result)), \
            #    200, {'Content-Type': 'application/json'}
        result_json = json.dumps({'status':'ok','code':200})
        resp = Response(result_json)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp        
        project_info['script'] = info['script']

    fetch_result = {}
    try:
        module = ProjectManager.build_module(project_info, {
            'debugger': True,
            'process_time_limit': app.config['process_time_limit'],
        })

        # The code below is to mock the behavior that crawl_config been joined when selected by scheduler.
        # but to have a better view of joined tasks, it has been done in BaseHandler.crawl when `is_debugger is True`
        # crawl_config = module['instance'].crawl_config
        # task = module['instance'].task_join_crawl_config(task, crawl_config)

        fetch_result = app.config['fetch'](task)
        response = rebuild_response(fetch_result)

        ret = module['instance'].run_task(module['module'], task, response)
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': fetch_result,
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
    else:
        result = {
            'fetch_result': fetch_result,
            'logs': ret.logstr(),
            'follows': ret.follows,
            'messages': ret.messages,
            'result': ret.result,
            'time': time.time() - start_time,
        }
        result['fetch_result']['content'] = response.text
        if (response.headers.get('content-type', '').startswith('image')):
            result['fetch_result']['dataurl'] = dataurl.encode(
                response.content, response.headers['content-type'])

    try:
        # binary data can't encode to JSON, encode result as unicode obj
        # before send it to frontend
        #return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}
        result_json = json.dumps({'status':'ok','code':200})
        resp = Response(result_json)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': "",
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        #return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}
        print('ok')        
        result_json = json.dumps({'status':'ok','code':200})
        resp = Response(result_json)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/debug/<project>/get_status',methods=['POST','GET'])
def get_status(project):
    projectdb = app.config['projectdb']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response
    status = project_info.get('status')
    print('status')
    return status

@app.route('/debug/<project>/save', methods=['POST', ])
def save(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if project_info:
        info = {
            'script': script,
        }
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 3),
        }
        projectdb.insert(project, info)

    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200

    return 'ok', 200


@app.route('/debug/<project>/get')
def get_script(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    return json.dumps(utils.unicode_obj(info)), \
        200, {'Content-Type': 'application/json'}


@app.route('/blank.html')
def blank_html():
    return ""
