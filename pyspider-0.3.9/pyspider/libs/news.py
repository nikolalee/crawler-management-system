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
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyquery import PyQuery as pq

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
        self.count = 1
        

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.url,fetch_type="js", callback=self.index_page)

    def index_page(self,response):
        if nextpage_format == "move":
            self.more_move(response)
        elif nextpage_format == "click":
            self.more_click(response) 
        elif nextpage_format == "btn":
            self.more_btn(response)
        
    def more_move(self,response):
        url = response.url
        driver = webdriver.PhantomJS()
        driver.get(url)
        js = " window.scrollTo(0,document.body.scrollHeight);console.log(12)"
        for i in range(0,int(deep_num)):
            print(i)
            time.sleep(0.3)
            driver.execute_script(js)
        content = driver.page_source.encode('utf-8')
        pyq = pq(content)
        items = pyq(href_css).items()
        self.phantomjs_parser(items)
    
    def more_click(self,response):
        url = response.url
        driver = webdriver.PhantomJS()
        driver.get(url)
        for i in range(0,int(deep_num)):
            print(i)
            time.sleep(0.3)
            if(driver.find_element_by_css_selector(nextpage_css).is_displayed()):
                driver.find_element_by_css_selector(nextpage_css).click()
            else:
                break
        content = driver.page_source
        pyq = pq(content)
        print(pyq(nextpage_css).text())
        items = pyq(href_css).items()
        self.phantomjs_parser(items)
        
    def more_btn(self,response):
        items = response.doc(href_css).items()
        self.phantomjs_parser(items)
        print(1)
        self.back(response)
        
            
            
    def back(self,response):
        url = self.get_nextpage_url(response)
        time.sleep(0.1)
        print(2)
        if url:
            if self.count < int(deep_num):
                print(self.count)
                self.count = self.count + 1
                time.sleep(1)
                self.crawl(url,fetch_type="js", callback=self.more_btn)
            else:
                print("too much")
        else:
            print('wrong url')
            
            
    def get_nextpage_url(self,response):
        items = response.doc(nextpage_css).items()
        next_url = ""
        for item in items:
            if item.text().find('下') is not -1:
                next_url = item.attr.href
                print(next_url)
                break
            elif item.text().find('后') is not -1:
                next_url = item.attr.href
                print(next_url)
                break
            elif item.text().find('>') is not -1:
                next_url = item.attr.href
                print(next_url)
                break
        return next_url
      
     
                    
        
        
            
    def phantomjs_parser(self,items):
        print("3")
        #print(response.js_script_result)
        #items = response.doc(href_css).items()
        count = 0
        for item in items:
            url = item.attr('href')
            url = self.sohu_url(url)
            print(url)
            count = count + 1
            if(count >= 10):
                count = 0
            self.crawl(url,callback=self.detail_page)
            
    def sohu_url(self,url):
        if url.find('http') == -1:
            head = start_url.split(':')[0]
            if url.find(':') == -1 and url.find('//')==-1:
                domain = self.get_domain()
                url = head +"://"+domain+'/'+ url
            elif url.find(':') == -1:
                url = head +':'+ url
            else:
                url = head + url
        return url
    
    def get_domain(self):
        urls = self.url.split('/')
        return urls[2]
                

    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        print("hi")
        result = {}
        result['url'] = response.url
        result['title'] = response.doc(title_css).text()
       
        result['src'] = response.doc(src_css).text()
        if len(result['src']) > 127:
            result['src'] = ''
            
        Time = response.doc(time_css).clone()
        Time.find(':nth-child(n)').remove()
        result['time'] = Time.text()
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
       
    
    
    
    






