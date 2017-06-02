#-*- coding:utf-8 -*-
import json


from util import jd_tools
import requests
import re

class jd_task_keyword:

    @classmethod
    def getMaxPage(cls, task):
        platform = task['body']['platform']
        keyword = task['body']['keyword']
        sort = task['body']['sort']
        if platform == 'jd_web':
            url = 'https://search.jd.com/Search?keyword='+ keyword['urlCoding'] +'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&click=0'+'&psort='+ sort
            myheader = {}
            myheader['host'] = 'search.jd.com'
            myheader['user_agent'] = jd_tools.get_web_useragent()
         #   myheader['cookie'] = jd_tools.get_jd_web_cookie()
            myheader = jd_tools.get_headers(myheader)
            urldata = requests.get(url, headers=myheader)
            rst = re.search(r'class=\"fp-text\"', urldata)
            if rst is not None:
                strEndPos = rst.end()
                rst1 = re.findall(r'\d+', urldata[strEndPos:strEndPos + 50])
                if rst1 is not None and len(rst1) >= 2:
                    totalPageS = rst1[1]
                    totalPage = int(totalPageS)
        elif platform == 'jd_app':
            url = 'https://so.m.jd.com/ware/search.action?keyword=' + keyword['urlCoding']
            myheader = {}
            myheader['origin'] = 'so.m.jd.com'
            myheader['user_agent'] = jd_tools.get_app_useragent()
         #   myheader['cookie'] = jd_tools.get_jd_app_cookie()
            myheader = jd_tools.get_headers(myheader)
            urldata = requests.get(url, headers=myheader)
            rst = re.search(r'wareCount', urldata)
            if rst is not None:
                strEndPos = rst.end()
                rst1 = re.findall(r'\d+', urldata[strEndPos:strEndPos + 15])
                if rst1 is not None and len(rst1) >= 1:
                    totalPageS = rst1[0]
                    totalPage = int(totalPageS)/10
        return totalPage

    @classmethod
    def get_urls(cls, task):
        platform = task['body']['platform']
        keyword = task['body']['keyword']
        sort = task['body']['sort']
        urlList=[]
        maxpage = cls.getMaxPage(task)
        if platform == 'jd_web':
            page = 1
            url = 'https://search.jd.com/s_new.php?'
            method = 'GET'
        elif platform == 'jd_app':
            page = 1
            url = 'https://so.m.jd.com/ware/searchList.action'
            method = 'POST'
            myheader = {
                'accept': 'application/json',
                'accept-encoding': 'gzip, deflate, sdch',
                'accept-language': 'zh-CN,zh;q=0.8',
                'content-length': '59',
                'connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded',
                'x-requested-with': 'XMLHttpRequest',
                'origin': '',
                #  'host': '',
                #'cookie':'',
                'referer': '',
                'user-agent': '',
            }
            myheader['user-agent'] = jd_tools.get_app_useragent()
            myheader['origin'] = 'https://so.m.jd.com'
            myheader['referer'] = 'https://so.m.jd.com/ware/search.action?keyword='+ keyword['urlCoding']
         #   myheader['cookie'] = jd_tools.get_jd_app_cookie()
        while(page<=maxpage):
            if platform == 'jd_web':
                myheader = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, sdch',
                    'accept-language': 'zh-CN,zh;q=0.8',
                    'connection': 'keep-alive',
                    'origin': '',
                    'host': '',
                    'referer': '',
                    'user-agent': '',
                    'cookie': ''
                }
                myheader['host'] = 'search.jd.com'
                myheader['user_agent'] = jd_tools.get_web_useragent()
              #  myheader['cookie'] = jd_tools.get_jd_web_cookie()
                if page % 2 == 1:
                    data = {'keyword': keyword['urlCoding'], 'enc': 'utf-8', 'qrst': '1', 'rt': '1', 'stop': '1', 'vt': '2', 'page': str(page), 's': str((page - 1) * 30 + 1), 'click': '0', 'psort':sort}
                    myheader['referer'] = 'https://search.jd.com/s_new.php?keyword='+ keyword['urlCoding']+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page='+str(page)+'&s='+str((page - 1) * 30 + 1)+'&click=0&psort='+ sort
                elif page % 2 == 0:
                    data = {'keyword': keyword['urlCoding'], 'enc': 'utf-8', 'qrst': '1', 'rt': '1', 'stop': '1', 'vt': '2', 'page': str(page), 's': str((page - 1) * 30 + 1), 'scrolling': 'y', 'pos': '30','psort': sort}
                    myheader['referer'] = 'https://search.jd.com/s_new.php?keyword='+ keyword['urlCoding']+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page='+str(page)+'&s='+str((page - 1) * 30 + 1)+ '&scrolling=y&pos=30&psort='+ sort
                myheader = jd_tools.get_headers(myheader)
            elif platform == 'jd_app':
                data = {'_format_':'json','stock':'0','sort':sort,'page':page,'keyword':keyword['urlCoding']}
            myurl={'url':url,'method':method,'data':data,'header':myheader}
            urlList.append(myurl)
            page=page+1
        return urlList

    @classmethod
    def parser(cls,html, task):
        platform = task['body']['platform']
        data = []
        if platform == 'jd_web':
            page = html
            rst = re.finditer(r'<li class=\"gl-item\" data-sku=\"', page)
            for index, item in enumerate(rst):
                strEndPos = item.end()
                rst1 = re.search(r'\d+', page[strEndPos:strEndPos + 20])
                if rst1 is not None:
                    data.append(rst1.group(0))
        elif platform == 'jd_app':
            page = json.loads(html)
            page = page['value']
            page = json.loads(page)
            mydatalist = page['wareList']['wareList']
            for index, item in enumerate(mydatalist):
                data.append(item['wareId'])
        return data

    @classmethod
    def saver(cls, data, task):
        taskid = task['guid']
        unique = taskid
        Motor.saveMongo(unique, data)

    @classmethod
    def get_next_time(cls):
        pass

    @classmethod
    def run(cls):
        pass