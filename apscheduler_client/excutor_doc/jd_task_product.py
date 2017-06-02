#-*- coding utf-8 -*-
import json
import re
from util import config
from util import Motor
from util.jd_tools import *

class jd_task_product:

    @classmethod
    def get_urls(cls,task):
        sku = task['body']['sku']
        platform = task['body']['platform']
        myheader = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'connection': 'keep-alive',
            #   'origin': '',
            #     'host': '',
            # 'referer': '',
            'user-agent': '',
            #   'cookie': ''
        }
        myheader['user-agent'] = jd_tools.get_app_useragent()
        urlList=[]
        if platform =='jd_app':
            url = 'https://item.m.jd.com/ware/detail.json?'#'https://mitem.jd.hk/ware/detail.json?'
            data = {'wareId':sku}
            myurl = {'url': url, 'method':'GET', 'data': data, 'header':myheader}
            urlList.append(myurl)
        return urlList

    @classmethod
    def getTargetStrList(cls, str, leftstr, rightstr):
        rstlist = re.finditer(leftstr, str)
        if rstlist is not None:
            strInfoList=[]
            for index, item in enumerate(rstlist):
                pos = item.start()
                targetStr = str[pos+leftstr.__len__():]
                targetStr = targetStr[:targetStr.find(rightstr)]
                strInfoList.append(targetStr)
            return strInfoList
        else:
            return None

    @classmethod
    def getdetailPhotoPaths(cls, photohtmlStr):
        newpathlist=[]
        photoPathList = cls.getTargetStrList(photohtmlStr,u'img src=\"',u'\" ')
        for item in photoPathList:
            newpathlist.append('http:'+item)
        return newpathlist

    @classmethod
    def parser_app(cls,html):
        page = json.loads(html)
        data = {}
        myDict = {}
        productDict = page['ware']
        productShopDict = productDict['mobileShopInfo']
        myDict['photoPath'] = productDict['chatUrl']
        templist = productDict['images']
        displayList = []
        for index, item in enumerate(templist):
            tempDict = {}
            tempDict['bigpath'] = item['bigpath']
            tempDict['smallpath'] = item['newpath']
            displayList.append(tempDict)
        myDict['displayPhotoPaths'] = displayList
        myDict['isPostByJd'] = productDict['isPostByJd']
        myDict['shopId'] = productShopDict['shopId']
        myDict['venderId'] = productDict['venderId']
        myDict['sku'] = productDict['wareId']
        detailPhoto = page['wdis']
        myDict['detailProductPhotoPaths'] = cls.getdetailPhotoPaths(detailPhoto)
        detailProductStr = productDict['wi']['code']
        detailProduct = json.loads(detailProductStr)
        myDict['detailProductDes'] = detailProduct
        myDict['kind'] = productDict['category'].replace(';', ',')
        childProductsStr = productDict['skuColorSizeHandler']['skuColorSizeJson']
        childProducts = json.loads(childProductsStr)
        childSkuInfo = childProducts['colorSize']
        myDict['childSku'] = []
        spu = myDict['sku']
        for index, item in enumerate(childSkuInfo):
            if myDict['sku'] != item['skuId']:
                myDict['childSku'].append(item['skuId'])
            if int(spu) > int(item['skuId']):
                spu = item['skuId']
        myDict['spu'] = spu
        shopid = myDict['shopId']
        data['skuInfo'] = myDict

        myDict = {}
        myDict['title'] = productDict['wname']
        data['skuInfoHistory'] = myDict

        myDict = {}
        myDict['shopId'] = shopid
        myDict['shopName'] = productShopDict['name']
        myDict['shopLogoPath'] = 'http:' + productShopDict['logo']
        myDict['shopBrief'] = productShopDict['brief']
        data['shopInfo'] = myDict

        myDict = {}
        myDict['followCount'] = productShopDict['followCount']
        myDict['productNum'] = productShopDict['totalNum']
        myDict['newProductNum'] = productShopDict['newNum']
        myDict['shopActivityTotalNum'] = productShopDict['shopActivityTotalNum']  # 店铺动态数
        data['shopInfoHistory'] = myDict
        return data

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