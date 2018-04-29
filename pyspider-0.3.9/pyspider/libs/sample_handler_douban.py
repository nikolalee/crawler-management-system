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
            "Referer": "https://movie.douban.com/subject/"
        }
        #"proxy":"58.216.202.149:8118"
    }
    def __init__(self):
        self.url = start_url
        

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url, callback=self.index_page)

    def index_page(self,response):
        #link = response.doc('#morelink-wrapper > p > a').attr('href')
        
        #link = link + "/p1"
        movie_name = response.doc('#content > h1 > span:nth-child(1)').text()
        link = response.doc('section.reviews.mod.movie-content > p > a').attr('href')
        print(link)
        print("Hello")
        self.crawl(link,callback=self.detail_page,save={'movie_name':movie_name})
    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        print("hi")
        pageNum = response.doc('div.paginator > span.thispage').attr('data-total-page')
        print(pageNum)
        movie_name = response.save['movie_name']
        for i in range(0,int(pageNum)):
            time.sleep(0.2)
            url = self.url + "/reviews?start=" + str(i*20)
            print(url)
            self.crawl(url,callback=self.process_page,save={'movie_name':movie_name})
       
    def process_page(self,response):
        lists = response.doc('div.review-list > div').items()
        movie_name = response.save['movie_name']
        for item in lists:
            time.sleep(0.2)
            link = item('div.main-bd > h2 > a').attr('href')
            if link:
                self.crawl(link,callback=self.domain_page,save={'movie_name':movie_name})
    
    
    def domain_page(self,response):
        if not response:
            print("Over")
            return
        result = {}
        movie_name = response.save['movie_name']
        result['comment_user'] = response.doc('header.main-hd > a > span').text()
        result['comment_time'] = response.doc('header.main-hd > span.main-meta').text()
        result['comment_vote'] = response.doc('div.main-panel-useful > button.useful_count').text()
        result['comment'] = ""
        lists = response.doc('div.review-content.clearfix > p').items()
        for each in lists:
            result['comment'] += each.text()
        #print result
        self.on_result(result,movie_name)
        comment_page = response.doc('div.paginator')
        comment_items = response.doc('div.comment-item').items()
        if comment_page:
            num = comment_page('a:nth-last-child(2)').text()
            print(num)
            #Id = self.url.split('/')[-1]
            for i in range(0,int(num)):
                url = response.url +"/?start=" + str(i*100)+"#comments"
                time.sleep(0.2)
                self.crawl(url,callback=self.recomment_page,save={'movie_name':movie_name,'author':result['comment_user']})
        elif comment_items:
            result1 = {}
            for item in comment_items:
                result1['user'] = item('div.content > div.header > a').text()
                result1['comment_time'] = item('div.content > div.header > span').text()
                result1['comments'] = item('div.content > p.comment-text').text()
                self.insert_to_sql(result1,movie_name,result['comment_user'])
         
    
    def on_result(self,result,movie_name):
        if not result:
            return
        print(result)
        if not result['comment_user']:
            return
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from douban where movie_name = %s and user_name = %s", (movie_name,result['comment_user']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        #print movie_name
        cur.execute("insert into douban(movie_name,user_name,comment_time,vote,comments) values(%s,%s,%s,%s,%s)", (movie_name,result['comment_user'],result['comment_time'], result['comment_vote'], result['comment']))
        conn.commit()
        cur.close()
        conn.close()
        
        
    def recomment_page(self,response):
        result = {}
        lists = response.doc('div.comment-item').items()
        movie_name = response.save['movie_name']
        author = response.save['author']
        for item in lists:
            result['user'] = item('div.content > div.header > a').text()
            result['comment_time'] = item('div.content > div.header > span').text()
            result['comments'] = item('div.content > p.comment-text').text()
            self.insert_to_sql(result,movie_name,author)
     
    def insert_to_sql(self,result,movie_name,author):
        if not result:
            return
        if not result['user']:
            return
        print("hu")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from douban_comment where movie_name = %s and user_name = %s", (movie_name,result['user']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        print("movie_name")
        cur.execute("insert into douban_comment(movie_name,author,user_name,comment_time,comments) values(%s,%s,%s,%s,%s)", (movie_name,author,result['user'],result['comment_time'],  result['comments']))
        conn.commit()
        cur.close()
        conn.close()

    



