#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

start_url = '__START_URL__'


from pyspider.libs.base_handler import *

import sys, time, pymysql,time,re

class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
            "Referer": "http://tech.huanqiu.com/"
        }
        #"proxy":"58.216.202.149:8118"
    }
    def __init__(self):
        self.url = start_url
        

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url, callback=self.index_page)

    def index_page(self,response):
        nextarea = response.doc('#pages > a').items()
        if not nextarea:
            print("null")
            return
        pagenum = response.doc('div#pages > a:nth-last-child(2)').text()
        for i in range(2,int(pagenum)+1):
            new_url = response.url + str(i) + ".html"
            print(new_url)
            time.sleep(2)
            self.crawl(new_url,callback=self.detail_page)
        print("1")
        self.detail_page(response)
        
        
    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        print("hi")
        lists = response.doc('div.fallsFlow > ul > li').items()
        for item in lists:
            link = item('h3 > a').attr('href')
            time.sleep(2)
            self.crawl(link,callback=self.process_page)
        
       
    def process_page(self,response):
        result = {}
        result['news_title'] = response.doc('div.con > div.con_left > div.l_a > h1').text()
        if not result['news_title']:
            result['news_title'] = response.doc('div.con > div.conLeft > div.conText > h1').text()
        result['publish_time'] = response.doc('div.con > div.con_left > div.l_a > div.la_tool > span.la_t_a').text()
        if not result['publish_time']:
            result['publish_time'] = response.doc('#pubtime_baidu').text()
        result['url'] = response.url
        result['content'] = ""
        content = response.doc('div.con_left > div.l_a > div.la_con > p').items()
        if not content:
            ps = response.doc('#text > p').items()
        else:
            ps = content
        for each in ps:
            sp = each('span')
            if sp:
                result['content'] += sp.text()
            else:
                result['content'] += each.text()
        self.on_result(result)
     
    def on_result(self,result):
        if not result:
            print("empty")
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from huanqiu where news_title = %s", result['news_title'])
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into huanqiu(news_title,url,publish_time,content) values(%s,%s,%s,%s)", (result['news_title'],result['url'], result['publish_time'], result['content']))
        conn.commit()
        cur.close()
        conn.close()
       
    
    
    
    






