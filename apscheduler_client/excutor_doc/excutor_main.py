
#此脚本将从中间层获取任务，执行器，抓取器，解析器，发送器的功能方法都封装,本地一个任务封装了一组相同类型的任务
#可进行业务拆分

"""
topic名称定义：
抓取任务：jm_crawl
解析任务：parsing
发送任务：send

"""
from concurrent.futures import ProcessPoolExecutor
import zmq,time,queue,uuid
from excutor_doc import setting
import requests
from excutor_doc import task_class
import asyncio
import aiohttp,threading
from excutor_doc import _interface
from aiocfscrape import CloudflareScraper
class excutor_cls:
    def __init__(self):
        self.count = 0
        #lib requests/aiohttp
        #本地生成的任务格式统一如下，服务器生成的多个本地任务将全部集成到一个任务中
        self.local_task = {

                            'topic':'jm_crawl',
                             'guid':'',#沿用服务器下发的任务id
                             'body':
                                    {
                                     'crawl':{'name':'','version':''},
                                     'urls':'',
                                     'abstime':'',
                                    #异步字段（是否使用异步）
                                    #使用平台
                                    #content主要是一组任务共有的关键信息
                                     'content':{

                                                'proxymode':'auto','encode':'utf-8',
                                                'lib':'aiohttp','max_retry':0,'bulk':False,
                                                'cookie':'','debug':False,'usephantomjs':False,

                                               },
                                    'result':[],#{'url': '', 'time': '', 'html': '', 'error': '', 'proxy': '', 'retry': 0, 'headers': '', 'other': '', 'sucess': False, 'platform': ''}
                                    'parsing_data':[],
                                    'callback':{"topic":'parsing',},
                                    }

                             }#excutor_interface的输出，catcher_interface的输入

        context = zmq.Context()
        self.socket_excutor = context.socket(zmq.REQ)#向中间层获取任务端口
        self.socket_excutor.connect("tcp://localhost:" + setting.EXCUTOR_PORT)

        self.socket_add = context.socket(zmq.REQ)  # 向中间层添加本地任务端口
        self.socket_add.connect("tcp://localhost:" + setting.LOCAL_TASK_PORT)

        self.poll = zmq.Poller()
        self.poll.register(self.socket_excutor, zmq.POLLIN)
        self.poll1 = zmq.Poller()
        self.poll1.register(self.socket_add, zmq.POLLIN)
        self.obj = task_class.jd_task_class()#生成本地任务和解析的对象

        self.inter_obj = _interface.oprate_task_job(setting.CENTER_INTERFACE_PORT)  # 通过中间层对客户端操作的对象


    def interface(self, dict):  # 参数必须是一个字典
        print ('input interface****************')
        next_topic = str(uuid.uuid1())  # 根据时间戳生成随机的uuid
        task = {'topic': 'JM_Crawl',
                'guid': '1',  # 沿用服务器下发的任务id
                'body':
                    {
                        'crawl': {'name': '', 'version': '1.1.1.1'},
                        'urls': dict['urls'],
                        'abstime': time.time(),
                        # content主要是一组任务共有的关键信息
                        'content': {

                            'proxymode': 'auto', 'encode': 'utf-8',
                            'lib': 'aiohttp', 'max_retry': 0, 'bulk': False,
                            'cookie': '', 'debug': False, 'usephantomjs': False,

                        },
                        'callback': {'topic': next_topic,'guid':dict['guid']},
                        'result': [],
                        # {'url': '', 'time': '', 'html': '', 'error': '', 'proxy': '', 'retry': 0, 'headers': '', 'other': '', 'sucess': False, 'platform': ''}
                        'parsing_data': [],
                    }
                }
        #task.update(dict)  # 有值则更新，没值则默认
        self.send(task)
        while True:
            # 从中间层获得topc = 'JM_Crawl_Result'+'guid' 的任务
            task = self.Access_to_task('get_task', next_topic)#????? + task['guid']
            if task:
                return task
            else:
                time.sleep(0.1)


    def send(self,task):#将任务添加到中间层的接口
        self.socket_add.send_json(task)
        while True:  # 服务器中断会一直尝试重连
            socks = dict(self.poll1.poll(3000))
            if socks.get(self.socket_add) == zmq.POLLIN:
                break
            else:#尝试重连
                self.socket_add.setsockopt(zmq.LINGER, 0)
                self.socket_add.close()
                self.poll1.unregister(self.socket_add)
                context = zmq.Context()
                self.socket_add = context.socket(zmq.REQ)
                self.socket_add.connect("tcp://localhost:" + setting.LOCAL_TASK_PORT)
                self.poll1.register(self.socket_add, zmq.POLLIN)
                self.socket_add.send_json(task)
        self.socket_add.recv_json()

#获取任务
    def Access_to_task(self,type = 'get_task',topic='test',count=1):#从中间层获取任务的接口
        req = {'type':type,'topic':topic,'count':count}#topic代表任务类型， count代表期望申请的任务个数,type :'get_task'（得到任务）/'get_size'（得到队列长度）不关心count
        req1 ={'type':'get_size','topic':topic,'count':count}#得到队列的长度
        self.socket_excutor.send_json(req)
        while True:#服务器中断会一直尝试重连
            socks = dict(self.poll.poll(3000))
            if socks.get(self.socket_excutor) == zmq.POLLIN:
                break
            else:#尝试重连
                print ("access_to_task 重连")
                time.sleep(0.1)
                self.socket_excutor.setsockopt(zmq.LINGER, 0)
                self.socket_excutor.close()
                self.poll.unregister(self.socket_excutor)
                context = zmq.Context()
                self.socket_excutor = context.socket(zmq.REQ)
                self.socket_excutor.connect("tcp://localhost:" + setting.EXCUTOR_PORT)
                self.poll.register(self.socket_excutor, zmq.POLLIN)
                self.socket_excutor.send_json(req)
        task_list = self.socket_excutor.recv_json()
        return task_list# 申请到的任务链表






if __name__ =='__main__':

    parsing()
    #task = t.Access_to_task('get_task','',count=1)[0]
    #print (task)
    #t.catcher_interface(task)#抓取任务接口，因为本地任务是相同类型任务的集合，所以此接口内部一次只取一个任务，然后分解并发
    #t.parsing_interface(task)

    """
    for i in task_list:
        t.excutor_interface(i)
    """