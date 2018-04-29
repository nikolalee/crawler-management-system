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
            "Referer": "http://bbs.xiaomi.cn"
        }
        #"proxy":"58.216.202.149:8118"
    }
    def __init__(self):
        self.url = start_url
        

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url, callback=self.index_page)

    def index_page(self,response):
        nextarea = response.doc('div.contain_right.fl > div > div.theme_con > div.base_widget_paging > div > ul > li.next > a').text()
        lastarea = response.doc('div.contain_right.fl > div > div.theme_con > div.base_widget_paging > div > ul > li.last > a').attr('href')
        if lastarea:
            print("last")
            pagenum = lastarea.split('-')[-1]
            for i in range(1,int(pagenum)+1):
                link = response.url + "-" + str(i)
                time.sleep(2)
                self.crawl(link,callback=self.detail_page)
        elif nextarea:
            print("next")
            pagenum = response.doc('#comment_top > div.base_widget_paging > div >ul >li:nth-child(2)').text()
            for i in range(1,int(pagenum)+1):
                link = response.url + "-" + str(i)
                time.sleep(2)
                self.crawl(link,callback=self.detail_page)
        else:
            print("no next")
            self.detail_page(response)
      
        
        
        
    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        print("hi")
        lists = response.doc('ul.themelistcon > li').items()
        for item in lists:
            author = item('div.theme_list_con > div.auth_msg > a.user_name').text()
            print(author)
            link = item('div.theme_list_con > div.title > a').attr('href')
            print(link)
            if link:
                time.sleep(3)
                self.crawl(link,callback=self.process_page,save={'author':author})
        
       
    def process_page(self,response):
        result = {}
        result['title'] = response.doc('div.filtrate.invitation > div.invitation_con > h1 > span.name').text()
        
        result['author'] = response.save['author']
        result['publish_time'] = response.doc('div.filtrate.invitation > div.invitation_con > p > span.time').text()
        result['url'] = response.url
        result['content'] = ""
        contents = response.doc('div.filtrate.invitation > div.invitation_con > div.invitation_content > p').items()
        for item in contents:
            result['content'] += item.text()
        self.on_result(result)
        nextarea = response.doc('#comment_top > div.base_widget_paging > div > ul > li.next > a').text()
        lastarea = response.doc('#comment_top > div.base_widget_paging > div >ul >li.last>a').attr('href')
        if lastarea:
            print("last1")
            pagenum = lastarea.split('-')[2]
            for i in range(1,int(pagenum)+1):
                link = response.url + "-" + str(i) + "-o1#comment_top" 
                time.sleep(3)
                self.crawl(link,callback=self.domain_page,save={'title':result['title']})
        elif nextarea:
            print("next")
            pagenum = response.doc('#comment_top > div.base_widget_paging > div > ul > li:nth-last-child(2)').text()
            for i in range(1,int(pagenum)+1):
                link = response.url + "-" + str(i) + "-o1#comment_top" 
                time.sleep(3)
                self.crawl(link,callback=self.domain_page)
        else:
            print("no next")
            self.crawl(response.url,callback=self.domain_page,save={'title':result['title']})
        
                
    
    def domain_page(self,response):
        if not response:
            return
        print("hi")
        #print response
        #print response.save['a']
        #title = response.save['title']
        #print title
        title = response.save['title']
        lists = response.doc('#comment_top > div.reply_con > ul > li').items()
        result = {}
        for item in lists:
            result['user'] = item('div.reply_list_con > div.auth_msg > a.auth_name').text()
            print(result['user'])
            result['time'] = item('div.reply_list_con > div.auth_msg > span:nth-child(5)').text()
            result['comment'] = item('div.reply_list_con > div.reply_txt > p').text()
            if not result['comment']:
                result['comment'] = item('div.reply_list_con > div.reply_txt').text()
            self.comment_page(result,title)
     
    def on_result(self,result):
        if not result:
            print("empty")
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from xiaomi where title = %s", result['title'])
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into xiaomi(title,author,url,publish_time,content) values(%s,%s,%s,%s,%s)", (result['title'],result['author'],result['url'], result['publish_time'], result['content']))
        conn.commit()
        cur.close()
        conn.close()
        
    def comment_page(self,result,title):
        if not result:
            print("it's null")
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from xiaomi_comment where users = %s and send_time = %s"  , (result['user'],result['time']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into xiaomi_comment(users,title,send_time,content) values(%s,%s,%s,%s)", (result['user'],title, result['time'], result['comment']))
        conn.commit()
        cur.close()
        conn.close()
       
    
    
    
    









