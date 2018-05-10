#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

project_name = '__PROJECT_NAME__'
start_url='__START_URL__'

nextpage_tag = '__NEXTPAGE_TAG__'

nextpage_name = '__NEXTPAGE_NAME__'

comment_box_css = '__COMMENT_BOX_CSS__'
comment_author_css = '__COMMENT_AUTHOR_CSS__'
time_css = '__TIME_CSS__'
content_css = '__CONTENT_CSS__'
#有回复时，评论内容的css
has_re_content_css = '__HAS_RE_CONTENT_CSS__'
#当该项在网页上不存在时，将值赋为“#”
vote_css = '__VOTE_CSS__'

#回复的类型，回复他人或被他人回复
response_type = "__RESPONSE_TYPE__" 
#回复他人时
response_css = '__RESPONSE_CSS__'
#被他人回复时
response_box_css = '__RESPONSE_BOX_CSS__'
res_user_css = '__RES_USER_CSS__'
res_time_css = '__RES_TIME_CS__'
res_content_css = '__RES_CONTENT_CSS__'

#评论在iframe中时，现在只在tencent上看到
iframe_id = "__IFRAME_ID__"
isIframe = '__IS_IFRAME__'

#获取更多评论的方式
more_type = '__MORE_TYPE__'
#爬取深度
deep_num = '__DEEP_NUM__'
step = '__STEP__'

from pyspider.libs.base_handler import *

import sys, time, pymysql,time,re
from selenium import webdriver
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
        
    @every(minutes=24 * 60)
    def on_start(self):
        if int(isIframe):
            self.dealIframe()
        else:
            self.crawl(self.url, callback=self.index_page)
    
    def dealIframe(self):
        driver = webdriver.PhantomJS()
        driver.get(start_url)
        time.sleep(5)
        driver.switch_to.frame('commentIframe')
        print('33')
        for i in range(1,int(deep_num)):
            time.sleep(0.2)
            print("hi"+str(i))
            driver.find_element_by_css_selector(nextpage_css).click()
            content = driver.page_source.encode('utf-8')
            iframe = pq(content)
            items = iframe(comment_box_css).items()
            self.deal_item(items)

    def index_page(self,response):
        print("1")
        time.sleep(5)
        url = response.url+"#more"
        if more_type == "more_move":
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
            self.crawl(url,callback=self.phantomjs_parser,fetch_type="js",js_script=script)
        elif more_type == "more_click":
            script = """function(){
                var num = """+str(deep_num)+""";
                var count = 0;
                var timer = setInterval(function(){
                    $('"""+nextpage_tag+"""')[0].click();
                    count++;
                    if(count > num){
                        clearInterval(timer);
                    }
                },10)
                return 123;
            }"""
            self.crawl(url,callback=self.phantomjs_parser,fetch_type="js",js_script=script)
           
            
        elif more_type == "more_list":
            call_func = self.mid_page
            self.get_nextpage_url(response, nextpage_tag, call_func, step)
        else:
            print("undefined type")
            return        
    
    def phantomjs_parser(self,response):
        print("3")
        time.sleep(6)
        print(response.js_script_result)
        items = response.doc(comment_box_css).items()
        self.deal_item(items)
    
    def deal_item(self,items):
        for item in items:
            result = {}
            result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            author = item.children(comment_author_css).text()
            #print(author == "")
            if author == "":
                result['comment_author'] = item.children('div > span.author > span.from').text()
                print(22)
            else:
                result['comment_author'] = author
            Time = item(time_css).clone()
            Time.find(':nth-child(n)').remove()
            result['time'] = Time.text()
            if response_type == "before":
                res_content = item.children(response_css).text()
                if res_content:
                    result['content'] = item.children(has_re_content_css).text()
                    result['response'] = res_content
                else:
                    result['content'] = item.children(content_css).text()
                    result['response'] = ""
            elif response_type == "after":
                result['content'] = item.children(content_css).text()
                result['response'] = ""
               #处理vote的获取
            if vote_css != "#":
                vote = item.children(vote_css).text()
                votes = re.findall('\d+',vote)
                if not votes:
                    result['vote'] = 0
                else:
                    result['vote'] = votes[0]
            else:
                result['vote'] = ""
            self.on_result(result)
            if response_type == "after":
                reply_items = item.find(response_box_css).items()
                self.detail_page(reply_items,result['content'],result['comment_author'])
               
    def detail_page(self,items,content,author):
        count = 0
        for item in items:
            count = count + 1
            print(count)
            result = {}
            result['user'] = item.children(res_user_css).text()
            #print(result['user'])
            result['res_time'] = item.children(res_time_css).text()
            res_content = item.children(res_content_css).clone()
            res_content.find(':nth-child(n)').remove()
            result['res_content'] = res_content.text()
            if not result['user']:
                result['user'] = item.children('p > span > b').text()
                res_content = item.children('p.reply-content').clone()
                res_content.find(':nth-child(n)').remove()
                result['res_content'] = res_content.text()
            print(result['res_content'])
            result['author'] = author
            result['content'] = content
            result["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.res_result(result)
     
    def notEmpty(self,items):
        result = []
        for item in items:
            result.append(item.text())
            print(result)
        if result:
            return 1
        else:
            return 0
    
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
    def get_nextpage_url(self,response,nextpage_tag,call_func,step):
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
            self.go_to_next(items1,call_func,step)
            
    #获取“下一页”的href   
    def go_to_next(self,items,call_func,step):
        nextpage_url = self.get_next_url(items)
        print(nextpage_url)
        if nextpage_url:
            if nextpage_url.find('http') == -1:
                head = start_url.split(":")[0]
                nextpage_url = head + ":" + nextpage_url
            print(nextpage_url)
            self.get_nextpage(nextpage_url, call_func, step)
        else:
            print("no url")
    
    #通过css得到下一页的url    
    def get_next_url(self,items):
        next_url = ""
        for item in items:
            if item.text().find(nextpage_name) is not -1:
                next_url = item.attr.href
                print(next_url)
                break
            elif item.text().find('页') is not -1:
                next_url = item.attr.href
                print(next_url)
                break
        return next_url 
    
    #生成所有爬取链接
    def get_nextpage(self,nextpage_url,call_func,step):
        nextpage_url_list = self.get_nextpage_url_list(nextpage_url)
        for i in range(0, int(deep_num) + 1):
            if len(nextpage_url_list) is 3:
                url = nextpage_url_list[0] +str(i*int(step)) +nextpage_url_list[1]+nextpage_url_list[2]
            if len(nextpage_url_list) is 2:
                url = nextpage_url_list[0] + str(i*int(step)) + nextpage_url_list[1]
            elif len(nextpage_url_list) is 1:
                url = nextpage_url_list[0] + str(i*int(step))
            print(url)
            self.crawl(url,callback=call_func)

    def mid_page(self,response):
        items = response.doc(comment_box_css).items()
        self.deal_item(items)        

        
    def on_result(self,result):
        if not result:
            print("result is empty")
            return
        print(result)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from comments2 where comment_author = %s and content=%s", (result['comment_author'],result['content']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into comments2(project_name,comment_author,publish_time,content,vote,response,crawl_time) values(%s,%s,%s,%s,%s,%s,%s)", (project_name,result['comment_author'],result['time'], result['content'],result['vote'], result['response'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()
        
    def res_result(self,result):
        if not result:
            return
        print(result)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='repository', passwd='repository', db='repository', charset='utf8')
        cur = conn.cursor()
        cur.execute("select * from comment_reply where reply_user = %s and reply_content=%s", (result['user'],result['res_content']))
        rows = cur.fetchall()
        if len(rows):
            cur.close()
            conn.close()
            return
        cur.execute("insert into comment_reply(author,content,reply_user,reply_time,reply_content,crawl_time) values(%s,%s,%s,%s,%s,%s)", (result['author'],result['content'],result['user'],result['res_time'], result['res_content'],result['crawl_time']))
        conn.commit()
        cur.close()
        conn.close()














