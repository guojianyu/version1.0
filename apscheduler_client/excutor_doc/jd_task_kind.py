#-*- coding:utf-8 -*-
import json

from excutor_doc.jd_tools import *
import requests
import re

class jd_task_kind:

    @classmethod
    def getMaxPage(cls, task):
        platform = task['body']['platform']
        kind = task['body']['kind']
        sort = task['body']['sort']
        if platform == 'jd_web':
            url = 'https://list.jd.com/list.html?cat='+ kind + '&page=1&stock=0&sort=' + sort + '&trans=1&JL=4_7_0#J_main'
            myheader = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, sdch',
                'accept-language': 'zh-CN,zh;q=0.8',
                'connection': 'keep-alive',
                #   'origin': '',
                #     'host': '',
                'referer': '',
                'user-agent': '',
                #   'cookie': ''
            }
            myheader['referer'] = 'https://list.jd.com/list.html?cat=' + kind
            myheader['user-agent'] = jd_tools.get_web_useragent()
         #   myheader['cookie'] = jd_tools.get_jd_web_cookie()
            r = requests.get(url, headers = myheader)
            urldata = r.text
            rst = re.search(r'class=\"fp-text\"', urldata)
            if rst is not None:
                strEndPos = rst.end()
                rst1 = re.findall(r'\d+', urldata[strEndPos:strEndPos + 50])
                if rst1 is not None and len(rst1)>=2:
                    totalPageS = rst1[1]
                    totalPage = int(totalPageS)
        elif platform == 'jd_app':
            kind = kind.replace(',','-')
            url = 'https://so.m.jd.com/products/'+ kind +'.html'
            myheader = {
              #  'origin': '',
                #  'host': '',
              #  'referer': '',
                'user-agent': '',
                #   'cookie': '',
            }
           # myheader['origin'] = 'https://so.m.jd.com'
          #  myheader['referer'] = 'https://so.m.jd.com/category/all.html'
            myheader['user_agent'] = jd_tools.get_app_useragent()
           # myheader['cookie'] = jd_tools.get_jd_app_cookie()
            r = requests.get(url, headers = myheader)
            urldata = r.text
            rst = re.search(r'wareCount', urldata)
            if rst is not None:
                strEndPos = rst.end()
                rst1 = re.findall(r'\d+', urldata[strEndPos:strEndPos + 15])
                if rst1 is not None and len(rst1)>=1:
                    totalPageS = rst1[0]
                    totalPage = int(totalPageS)/10
                    totalPage = int(totalPage)
        print ('totalPage=',totalPage)
        return totalPage

    @classmethod
    def get_urls(cls,task):
        platform = task['body']['platform']
        kind = task['body']['kind']
        sort = task['body']['sort']
        urlList=[]
        maxpage = cls.getMaxPage(task)
        page = 1
        if platform == 'jd_web':
            url = 'https://list.jd.com/list.html?'
            method = 'GET'
            myheader = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'connection': 'keep-alive',
         #   'origin': '',
       #     'host': '',
            'referer': '',
            'user-agent': '',
         #   'cookie': ''
            }
            myheader['referer'] = 'https://list.jd.com/list.html?cat='+kind
            myheader['user-agent'] = jd_tools.get_web_useragent()
            useproxy = True
        elif platform == 'jd_app':
            url = 'https://so.m.jd.com/ware/searchList.action'
            method = 'POST'
            myheader = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'content-length':'59',
            'connection': 'keep-alive',
            'content-type':'application/x-www-form-urlencoded',
            'x-requested-with':'XMLHttpRequest',
            'origin': '',
          #  'host': '',
            'referer': '',
            'user-agent': '',
         #   'cookie': '',
            }
            myheader['origin'] = 'https://so.m.jd.com'
            nkind = kind.replace(',', '-')
            myheader['referer'] = 'https://so.m.jd.com/products/'+ nkind +'.html'
            myheader['user-agent'] = jd_tools.get_app_useragent()
            useproxy = False
        while(page<=maxpage):
            if platform == 'jd_web':
                data = {'cat':kind,'page':str(page), 'stock':'0','sort':sort,'trans':'1','JL':'6_0_0'}
            elif platform == 'jd_app':
                kindstrlist = kind.split(",")
                print ('kindstrlist-----------------------',kindstrlist)
                data = {'_format_':'json','stock':0,'sort':sort,'page':page,'categoryId':kindstrlist[0],'c1':kindstrlist[1],'c2':kindstrlist[2]}
            myurl = {'url': url, 'method': method, 'data': data, 'header': myheader, 'useproxy': useproxy,
                     'platform': platform}
            urlList.append(myurl)
            page=page+1
        return urlList

    @classmethod
    def getstr(cls, str, left, right):
        str = str[str.find(left) + left.__len__():]
        str = str[:str.find(right)]
        return str

    @classmethod
    def parser(cls,html,task):
        platform = task['url']['platform']
        data = []
        if platform == 'jd_web':
            page = html
            data = cls.getstr(page, "pay_after = [","];").split(",")
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

    """
    @classmethod
    def print(cls):
        print ("ok")
    """

    @classmethod
    def parser_run(cls):
        pass

#obj = jd_task_kind()
#obj.pre_run()

