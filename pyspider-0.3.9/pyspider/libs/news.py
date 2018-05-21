#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

project_name = '__PROJECT_NAME__'
start_url = '__START_URL__'
title_css = '__TITLE_CSS__'
nextpage_css = '__NEXTPAGE_CSS__'
href_css = '__HREF_CSS__'
time_css = '__TIME_CSS__'
src_css = '__SRC_CSS__'
content_css = '__CONTENT_CSS__'
nextpage_format  = '__NEXTPAGE_FORMAT__'
deep_num = '__DEEP_NUM__'
from pyspider.libs.base_handler import *

import sys, time, pymysql,time,re

class Handler(BaseHandler):
    crawl_config = {
        
        "headers": {
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Referer": start_url
        }
        #"proxy":"58.216.202.149:8118"
    }
    def __init__(self):
        self.url = start_url
        

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url,fetch_type="js", callback=self.index_page)

    def index_page(self,response):
        print("1")
        url = response.url+"#more"
        if nextpage_format == "move":
            script = '''function(){
                var num = '''+str(deep_num)+''';
                var count = 0;
                var timer = setInterval(function(){
                    window.scrollTo(0,document.body.scrollHeight);
                    count++;
                    if (count > num){
                        clearInterval(timer);
                        }            
                    },600)
                    return 123;
                } ''';
        elif nextpage_format == "click":
            script = """function(){
                var num = """+str(deep_num)+""";
                var count = 0;
                var timer = setInterval(function(){
                    $('"""+nextpage_css+"""')[0].click();
                    count++;
                    if(count > num){
                        clearInterval(timer);
                    }
                },100)
                return 12;
            }"""    
        self.crawl(url,callback=self.phantomjs_parser,fetch_type="js",js_script=script)
        
    def phantomjs_parser(self,response):
        print("3")
        print(response.js_script_result)
        items = response.doc(href_css).items()
        for item in items:
            url = item.attr('href')
            print(url)
            time.sleep(0.2)
            self.crawl(url,callback=self.detail_page)

    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        print("hi")
        result = {}
        result['url'] = response.url
        result['title'] = response.doc(title_css).text()
       
        result['src'] = response.doc(src_css).text()
      
        result['time'] = response.doc(time_css).text()
        print(result['time'])
        contentArea = response.doc(content_css)
        result['content'] = response.doc(content_css).text();
        if result['content'] == "":
            ps = contentArea('p').items()
            for item in ps:
                result['content'] += item.text()
        result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.on_result(result)

     
    def on_result(self,result):
        if not result:
            print("empty")
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from news where news_title = %s", result['title'])
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into news(project_name,news_title,url,src,publish_time,content,crawl_time) values(%s,%s,%s,%s,%s,%s,%s)", (project_name,result['title'],result['url'], result['src'],result['time'], result['content'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()
       
    
    
    
    






