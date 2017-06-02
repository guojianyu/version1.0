#-*- coding utf-8 -*-
import json
import re

from util import jd_tools
import requests

class jd_task_shop:

    @classmethod
    def getMaxPage(cls,task):
        shopid = task['body']['shopid']
        platform = task['body']['platform']
        if platform == 'jd_app':
            url = 'https://shop.m.jd.com/search/searchWareAjax.json?r=1493968950605'
            myheader = {}
            myheader['host'] = 'shop.m.jd.com'
            myheader['origin'] = 'https://shop.m.jd.com'
            myheader['referer'] = 'https://shop.m.jd.com/search/search?shopId='+ shopid
            myheader['user_agent'] = jd_tools.get_app_useragent()
            #myheader['cookie'] = jd_tools.get_jd_app_cookie()
            myheader = jd_tools.get_headers(myheader)
            data={'shopId':shopid, 'searchPage':'1', 'searchSort':'0'}
            r = requests.post(url, data = data, headers=myheader)
            urldata = r.text
            page = json.loads(urldata)
            totalPage = page['results']['totalPage']
        return totalPage

    @classmethod
    def get_urls(cls, task):
        shopid = task['body']['shopid']
        platform = task['body']['platform']
        urlList=[]
        maxpage = cls.getMaxPage(task)
        if platform == 'jd_app':
            url = 'https://shop.m.jd.com/search/searchWareAjax.json?r=1493968950605'
            myheader = {}
            myheader['origin'] = 'https://shop.m.jd.com'
            myheader['referer'] = 'https://shop.m.jd.com/search/search?shopId=' + shopid
            myheader['user_agent'] = jd_tools.get_app_useragent()
            myheader = jd_tools.get_headers(myheader)
        page = 1
        while (page <= maxpage):
            if platform == 'jd_app':
                data = {'shopId':shopid,'searchPage':str(page),'searchSort':'0'}
                myurl = {'url': url, 'method':'POST', 'data': data, 'header': myheader}
                urlList.append(myurl)
        return urlList

    @classmethod
    def parser_app(cls,html):
        page = json.loads(html)
        productList = page['results']['wareInfo']
        productInfoList = []
        for index, item in enumerate(productList):
            productDict = {}
            productDict['sku'] = str(item['wareId'])
            productDict['goodRate'] = item['good']
            productDict['isHotSale'] = item['isHot']
            productDict['isNewProduct'] = item['isNew']
            productInfoList.append(productDict)
        return productInfoList

    @classmethod
    def parser(cls,html,task):
        platform = task['body']['platform']
        if platform == 'jd_app':
            data = cls.parser_app(html)
        return data

    @classmethod
    def saver(cls, data, task):
        taskid = task['guid']
        unique = taskid
        Motor.saveMongo(unique, data)

    @classmethod
    def get_next_time(cls):
        pass