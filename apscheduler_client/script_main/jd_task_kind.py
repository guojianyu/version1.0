#-*- coding:utf-8 -*-
import json,uuid
from excutor_doc.jd_tools import *
import requests
import re
import time
from excutor_doc.excutor_main import *
from center_layer.center_interface._interface import *

class jd_task_kind:

    @classmethod
    def generateTask(cls):
        tasks=[]
        kinds=[]
        allKindId = {"portablePower": "9987,830,13658", "dataLine": "9987,830,13661", "phoneCase": "9987,830,866",
                      "flatAccessories": "670,671,5146", "padPasting": "9987,830,867", "mobilePhone": "9987,653,655",
                      "carAccessories": "9987,830,864", "charger": "9987,830,13660",
                      "mobilephoneBattery": "9987,830,13657", "accessoriesOfAppleProducts": "9987,830,13659",
                      "smartBracelet": "652,12345,12347", "healthMonitoring": "652,12345,12351",
                      "mobileMemoryCard": "9987,830,1099", "mobilePhoneEarphone": "9987,830,862",
                      "creativeAccessories": "9987,830,868", "mobileAccessories": "9987,830,11302",
                      "bluetoothHeadset": "9987,830,863", "mobileBracket": "9987,830,12811",
                      "cameraAccessories": "9987,830,12809", "smartWatch": "652,12345,12348",
                      "smartGlasses": "652,12345,12349", "intelligentRobot": "652,12345,12806",
                      "motionTracker": "652,12345,12350", "intelligentAccessories": "652,12345,12352",
                      "smartHome": "652,12345,12353", "inmotion": "652,12345,12354",
                      "unmannedAerialVehicle": "652,12345,12807",
                      "otherEquipmentOfIntelligentDevice": "652,12345,12355"}
        for index, item in enumerate(allKindId):
            kinds.append(allKindId[item])
        basic_task = {'device':{'type': '', 'version': '127.22', 'id': ''},
                    'guid': '',
                    'time': '',#time.time(),
                    'timeout': 1200,
                    'topic': 'jd_task_kind',
                    'interval': 86400,  # 任务执行周期间隔时间
                    'suspend': 0,  # 暂停标识
                    'status': 0,
                    'body': {
                          'kind': '', 'platform': '', 'sort': '',
                        }
        }
        sortlist = ['sort_totalsales15_desc','sort_rank_asc']
        platformlist = ['jd_app','jd_web']
        for i in range(len(kinds)):
            for index1, item1 in enumerate(sortlist):
                for index2, item2 in enumerate(platformlist):
                    guid = str(uuid.uuid1())  # 根据时间戳生成随机的uuid
                    dictUpdate={'guid':guid,'time':time.time(),'body':{'kind':kinds[i],'platform':item1,'sort':item2}}
                    basic_task.update(dictUpdate)
                    tasks.append(basic_task)
        return tasks

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
                data = {'_format_':'json','stock':0,'sort':sort,'page':page,'categoryId':kindstrlist[0],'c1':kindstrlist[1],'c2':kindstrlist[2]}
            myurl={'url':url,'method':method,'data':data,'header':myheader,'useproxy':useproxy,'platform':platform,'sort':sort,'kind':kind,'page':page}
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
        sort = task['url']['sort']
        kind = task['url']['kind']
        ppage = task['url']['page']
        data = []
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S BJT", time.localtime(time.time()))
        if platform == 'jd_web':
            page = html
            data = cls.getstr(page, "pay_after = [","];").split(",")
            return {'time':timeStr,'key_search':0,'key_word':None,'platform':platform,'sort':sort,'kind':kind,'page':page,'order':data}
        elif platform == 'jd_app':
            try:
                page = json.loads(html)
                page = page['value']
                page = json.loads(page)
                mydatalist = page['wareList']['wareList']
                for index, item in enumerate(mydatalist):
                    data.append(item['wareId'])
            except Exception as e:
                print (e)
            finally:
                return {'time':timeStr,'key_search':0,'key_word':None,'platform': platform, 'sort': sort, 'kind': kind, 'page': ppage, 'order': data}

    @classmethod
    def isAntiSpider(cls, html,task):
        isAntiSpier = False
        platform = task['url']['platform']
        if platform == 'jd_app':
            constStr1 = '{"areaName":"","value":"{\\"searchFilter\\":{\\"filterItemPromotion\\":{},\\"filterItemAttrs\\":[],\\"filter\\":[]},\\"wareList\\":{\\"adEventId\\":\\"\\",\\"errorCorrection\\":\\"\\",\\"gaiaContent\\":false,\\"hasTerm\\":true,\\"isFoot\\":false,\\"isSpecialStock\\":\\"0\\",\\"showStyleRule\\":\\"\\",\\"wareCount\\":0}}'
            constStr2 = '{"areaName":"","value":"{\\"searchFilter\\":{\\"filterItemPromotion\\":\\"{\\\\\\"imgUrl\\\\\\":\\\\\\"http:\\/\\/m.360buyimg.com\\/mobilecms\\/jfs\\/t5491\\/219\\/1639317102\\/1775\\/467927d7\\/5912bc85Nfe97ec68.png\\\\\\",\\\\\\"promotionId\\\\\\":\\\\\\"423909\\\\\\",\\\\\\"name\\\\\\":\\\\\\"618\\\\\\",\\\\\\"promType\\\\\\":\\\\\\"icon\\\\\\"}\\",\\"filter\\":[{\\"classfly\\":\\"\\",\\"itemArray\\":[{\\"itemName\\":\\"\\",\\"termList\\":[{\\"otherAttr\\":{},\\"text\\":\\"京东配送\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"self\\"}},{\\"otherAttr\\":{},\\"text\\":\\"货到付款\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"cod\\"}},{\\"otherAttr\\":{},\\"text\\":\\"仅看有货\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"stock\\"}},{\\"otherAttr\\":{},\\"text\\":\\"促销\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"promotion\\"}},{\\"otherAttr\\":{},\\"text\\":\\"全球购\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"globalPurchaseFilter\\"}},{\\"otherAttr\\":{},\\"text\\":\\"PLUS尊享\\",\\"value\\":{\\"bodyValues\\":\\"1\\",\\"bodyKey\\":\\"plusWareFilter\\"}}]}],\\"itemKey\\":\\"\\",\\"key\\":\\"configuredFilters\\",\\"otherAttr\\":{}}]},\\"wareList\\":{\\"adEventId\\":\\"\\",\\"errorCorrection\\":\\"\\",\\"gaiaContent\\":false,\\"hasTerm\\":true,\\"isFoot\\":false,\\"isSpecialStock\\":\\"0\\",\\"showStyleRule\\":\\"\\",\\"wareCount\\":0}}"}'
            charStr1 = '\\"wareCount\\":0'
            charStr2 = '京东下载页'
            charStr3 = '专业网上购物平台品质保障'
            if html == constStr1:
                print ("fangpa**********constStr1")
                isAntiSpier = True
            if html == constStr2:
                print("fangpa**********constStr2")
                isAntiSpier = True
            if html.find(charStr1) is not -1:
                print("fangpa**********charStr1")
                isAntiSpier = True
            if html.find(charStr2) is not -1:
                print("fangpa**********charStr2")
                isAntiSpier = True
            if html.find(charStr3) is not -1:
                print("fangpa**********charStr3")
                isAntiSpier = True
        return isAntiSpier

    @classmethod
    def run(cls,task):

        obj = excutor_cls()
        urls = cls.get_urls(task)
        arg = {'urls':urls,'guid':task['guid']}
        ptask = obj.interface(arg)
       # print (ptask,"*************ptask")
        zresult={'guid':task['guid'],'result':[],'data':[]}
        if ptask:
            results = ptask[0]['body']['result']
            for index, _result in enumerate(results):
                if cls.isAntiSpider(_result['html'], _result):
                    zresult['result'].append({'platform':_result['url']['platform'],'sort':_result['url']['sort'],'kind':_result['url']['kind'],'page':_result['url']['page'],'html':'isAntiSpider'})
                    continue
                data = cls.parser(_result['html'],_result)
                if data:
                    zresult['result'].append({'platform': _result['url']['platform'], 'sort': _result['url']['sort'],'kind': _result['url']['kind'], 'page': _result['url']['page'],'html': 'has parsed'})
                    zresult['data'].append(data)
                else:
                    zresult['result'].append({'platform': _result['url']['platform'], 'sort': _result['url']['sort'],'kind': _result['url']['kind'], 'page': _result['url']['page'],'html':_result['html']})
            obj.inter_obj.upload_data(zresult)
      #  return data

    @classmethod
    def saver(cls):
        taskid = task['guid']
        unique = taskid
       # Motor.saveMongo(unique, data)

    @classmethod
    def saver_server(cls, data, task):#运行在server端
        savedata = task['content']['body']['parsing_data']
        mongodb.insert(savedata,'SKUORDER')

    @classmethod
    def get_next_time(cls):
        pass


    """
    @classmethod
    def print(cls):
        print ("ok")
    """
    """
    @classmethod
    def pre_run(cls):
        tObj = getSock_topic()
        req = {'topic':'kind','count':1}
        task = tObj.send_and_get_json(req)
        print (task)
        urllist = self.get_urls(task)
        uObj = getSock_url()
        for index, item in enumerate(urllist):
            urlTask = {'topic':task,'url':item}
            ret = uObj.send_and_get_json(urlTask)
            if ret['ret'] is not 'ok':
                uObj.send_and_get_json(urlTask)
            print (index+1)
    """
    @classmethod
    def parser_run(cls):
        pass



if __name__ == '__main__':
    task = {'device':{'type': '', 'version': '127.22', 'id': ''},
        'guid': '9a4e4a10-45d6-11e7-9169-a860b60c7382',
        'time': time.time(),
        'timeout': 1200,
        'topic': 'jd_task_kind',
        'interval': 86400,  # 任务执行周期间隔时间
        'suspend': 0,  # 暂停标识
        'status': 0,
        'body': {
             'kind': '9987,830,866', 'platform': 'jd_app', 'sort': None,
                }
    }

    obj = oprate_task_job(9995)
    ret = obj.add_task(task)
    print (ret)
    obj = jd_task_kind()
    obj.run(task)
