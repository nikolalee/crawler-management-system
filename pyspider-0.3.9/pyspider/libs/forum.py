#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

project_name = '__PROJECT_NAME__'
start_url='__START_URL__'

main_nextpage_tag = '__MAIN_NEXTPAGE_TAG__'
nextpage_keyword = '__NEXTPAGE_KEYWORD__'
#下一页的形式
nextpage_type = "__NEXTPAGE_TYPE__"
#爬取深度
main_page_num = '__MAIN_PAGE_NUM__'


href_css = '__HREF_CSS__'
title_css = '__TITLE_CSS__'
author_css = '__AUTHOR_CSS__'
publish_time_css = '__PUBLISH_TIME_CSS__'
content_css = '__CONTENT_CSS__'
main_step = '__MAIN_STEP__'
sub_page_num = '__SUB_PAGE_NUM__'


#当没有下一页时为“#”
sub_nextpage_tag = '__SUB_NEXTPAGE_TAG__'
tie_box_css = '__TIE_BOX_CSS__'
tie_user_css = '__TIE_USER_CSS__'
tie_time_css = '__TIE_TIME_CSS__'
tie_content_css = '__TIE_CONTENT_CSS__'
sub_step = '__SUB_STEP__'

# 以上几个字符串参数都不为'#',page_num>=0,filter_words可以为''
from pyspider.libs.base_handler import *
import sys, time, pymysql
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver



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
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(start_url,callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        if main_nextpage_tag == "#":
            self.domain_page(response)
        else:
            if nextpage_type == "btn_list":
                nextpage_area = response.doc(main_nextpage_tag).text()
                func = self.domain_page
                if not nextpage_area:
                    self.request(start_url,func,main_step)
                time.sleep(1)
                self.get_nextpage_url(response,main_nextpage_tag,func,main_step," ",main_page_num)
            else:
                num = main_page_num
                self.list_page(response.url,num)
            
    #通过css得到下一页的url    
    def get_next_url(self,items):
        next_url = ""
        for item in items:
            if item.text().find(nextpage_keyword) is not -1:
                next_url = item.attr.href
                print(next_url)
                break
            elif item.text().find('页') is not -1:
                next_url = item.attr.href
                print(next_url)
                break
        return next_url 
        
    #得到主域名地址  
    def get_head(self,url):
        urls = url.split("/")
        new_url =   urls[0]+"//"+urls[2]
        #print(new_url)
        return new_url

    #以requests实现爬取多个列表页
    def list_page(self,url,num):
        for i in range(1,int(num)):
            time.sleep(3)
            print(url)
            if url:
                response = requests.get(url)
                pyq = pq(response.content)
                self.request_domain_page(pyq)
                # print(pyq(nextpage_css).attr.href)
                items = pyq(main_nextpage_tag).items()
                url = self.get_next_url(items)
                if url.find('http') == -1:
                    head = self.get_head(start_url)
                    url = head + url
            else:
                print("wrong url")
                break
                
    def request_domain_page(self,response):
        hrefs = response(href_css).items()
        for item in hrefs:
            url = item.attr.href
            if url.find('http') == -1:
                url = self.get_head(start_url)+url
            self.crawl(url,callback=self.main_page)
        
    # 当self.crawl无法爬取到内容时
    def request(self,url,func,step):
        r=requests.get(url)
        html=r.content
        pyq = pq(html)
        nextpage_url = pyq(main_nextpage_tag).attr.href
        if nextpage_url.find('http') == -1:
            head = start_url.split(":")[0]
            nextpage_url = head + ":" + nextpage_url
        time.sleep(1)
        self.get_nextpage(nextpage_url, func, step," ")
         
    def notEmpty(self,items):
        result = []
        for item in items:
            result.append(item.text())
            print(result)
        if result:
            return 1
        else:
            return 0
        
    #帖子列表页面
    def domain_page(self,response):
        hrefs = response.doc(href_css).items()
        flag = self.notEmpty(hrefs)
        print(flag)
        if not flag:
            r=requests.get(response.url)
            html=r.content
            pyq = pq(html)
            hrefs = pyq(href_css).items()
        for item in hrefs:
            url = item.attr.href
            if url.find('http') == -1:
                url = self.get_head(start_url)+url
                print("domain_url:"+url)
            time.sleep(2)
            self.crawl(url,callback=self.main_page)
            
    #帖子主页面
    def main_page(self,response):
        result = {}
        result['url'] = response.url
        result['author'] = response.doc(author_css).text()
        result['title'] = response.doc(title_css).text()
        result['publish_time'] = response.doc(publish_time_css).text()
        result['content'] = response.doc(content_css).text()
        result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.on_result(result)
        flag = self.existed(response,sub_nextpage_tag)
        if flag:
            func = self.mid
            self.get_nextpage_url(response, sub_nextpage_tag,func,sub_step,result['title'],sub_page_num)
        else:
            self.detail_page(response,result['title'])
    
    def existed(self,response,css):
        flag = 0;
        nextarea = response.doc(css).text()
        if not nextarea:
            r=requests.get(response.url)
            html=r.content
            pyq = pq(html)
            nextarea2 = pyq(css).text()
            if nextarea2:
                flag = 1
        else:
            flag = 1
        return flag
        
        
    #解析出链接公共部分
    def get_nextpage_url_list(self, url):
        filetype_list = [".shtml", ".html", ".htm", ".php", ".jsp"]
        url_list = []
        for t in filetype_list:
            l = min([len(url), len(max(filetype_list))])
            if url[len(url) - l:len(url)].find(t) != -1:
                url = url.replace(t, '')[::-1]
                for i in range(len(url)):
                    if url[i].isdigit() is False:
                        url = url[i:len(url)][::-1]
                        url_list.append(url)
                        url_list.append(t)
                        break
                break
        if len(url_list) == 0:
            print("url2")
            url2 = url[::-1]
            for i in range(len(url2)):
                if url2[0].isdigit() is False:
                    break
                else:
                    if url2[i].isdigit() is False:
                        url2 = url2[i:len(url2)][::-1]
                        url_list.append(url2)
                        break
            if len(url_list) == 0:
                print("url3")
                if url.find('#') is not -1:
                    url3 = url.split('#')
                    print(url3)
                    url4 = url3[0][::-1]
                    for i in range(0,len(url4)):
                        if url4[i].isdigit() is False:
                            url4 = url4[i:len(url4)][::-1]
                            url_list.append(url4)
                            url_list.append('#')
                            url_list.append(url3[1])
                            break
        return url_list
    
    #获取“下一页”的href,初步处理
    def get_nextpage_url(self,response,nextpage_tag,call_func,step,title,num):
        items1 = response.doc(nextpage_tag).items()
        flag = self.notEmpty(items1)
        print("flag:"+str(flag))
        if not flag:
            r=requests.get(response.url)
            html=r.content
            pyq = pq(html)
            items2 = pyq(nextpage_tag).items()
            self.go_to_next(items2,call_func,step,title)
        else:
            items1 = response.doc(nextpage_tag).items()
            self.go_to_next(items1,call_func,step,title,num)
            
    #获取“下一页”的href   
    def go_to_next(self,items,call_func,step,title,num):
        nextpage_url = self.get_next_url(items)
        print(nextpage_url)
        if nextpage_url:
            if nextpage_url.find('http') == -1:
                head = start_url.split(":")[0]
                nextpage_url = head + ":" + nextpage_url
            print(nextpage_url)
            self.get_nextpage(nextpage_url, call_func, step,title,num)
        else:
            print("no url")
            
    #生成所有爬取链接
    def get_nextpage(self,nextpage_url,call_func,step,title,num):
        nextpage_url_list = self.get_nextpage_url_list(nextpage_url)
        for i in range(0, int(num) + 1):
            if len(nextpage_url_list) is 3:
                url = nextpage_url_list[0] +str(i*int(step)) +nextpage_url_list[1]+nextpage_url_list[2]
            if len(nextpage_url_list) is 2:
                url = nextpage_url_list[0] + str(i*int(step)) + nextpage_url_list[1]
            elif len(nextpage_url_list) is 1:
                url = nextpage_url_list[0] + str(i*int(step))
            print(url)
            time.sleep(2)
            self.crawl(url,callback=call_func,save={'title':title})
    
    def mid(self,response):
        title = response.save['title']
        self.detail_page(response,title)
        
    #爬取帖子内容
    @config(priority=3)
    def detail_page(self, response,title):
        items = response.doc(tie_box_css).items()
        for item in items:
            result = {}
            result['tie_user'] = item.children(tie_user_css).text()
            result['publish_time'] = item.children(tie_time_css).text()
            result['tie_content'] = item.children(tie_content_css).text()
            result['tie_title'] = title
            result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            result['response'] = ""
            self.tie_result(result)

        

    def on_result(self,result):
        if not result:
            print("result is empty")
            return
        print(result)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from forum where title = %s ", result['title'])
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into forum(project_name,url,title,author,publish_time,content,crawl_time) values(%s,%s,%s,%s,%s,%s,%s)", 
            (project_name,result['url'],result['title'],result['author'],result['publish_time'], result['content'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()

    def tie_result(self,result):
        if not result:
            print("result is empty")
            return
        print(result)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from tie2 where project_name = %s and tie_user = %s and publish_time = %s", (project_name,result['tie_user'],result['publish_time']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into tie2(project_name,tie_title,tie_user,publish_time,tie_content,response,crawl_time) values(%s,%s,%s,%s,%s,%s,%s)", 
            (project_name,result['tie_title'],result['tie_user'],result['publish_time'], result['tie_content'],result['response'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()

    















