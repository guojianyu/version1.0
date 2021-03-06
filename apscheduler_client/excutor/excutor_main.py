
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
from center_layer.center_interface import _interface
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

        self.semaphore = asyncio.Semaphore(100)
        self.url_q = asyncio.Queue()
        self.result_q = asyncio.Queue()
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
                print ("重连")
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



    def run(self):
        tasks = []
        for _ in range(0, 10):
            tasks.append(self.work())#抓取任务
        tasks.append(self.create_parstask())  # 将同一任务分解的单个抓取任务得到的数据拼接为一个解析任务
        tasks.append(self.get_crawltask())  # 将任务分解为单个抓取任务
        f = asyncio.wait(tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f)
        self.url_q.join()
        self.result_q.join()

    async def work(self):
        while True:
            await asyncio.sleep(0)
            url = await self.get_url()
            if url:
                await self.parseUrl(url)

    async def get_crawltask(self):#将任务分解为单个抓取任务
        while True:
           # print ('url_q:',self.url_q.qsize(),"result_q",self.result_q.qsize())
            task = self.Access_to_task('get_task', 'JM_Crawl', count=1)
            if task:
                print('分解抓取任务')
                urls = task[0]['body']['urls']
                guid = task[0]['guid']
                callback = task[0]['body']['callback']
                task_count= len(urls)
                for url in urls:
                    print (url)
                    url['guid'] = guid#将服务器下发的任务id添加进去
                    url['task_count'] = task_count#将任务总数加到url中
                    url['callback'] = callback#
                    await self.url_q.put(url)  # 将url添加到队列

            else:
                await asyncio.sleep(0.1)


    async def get_url(self):
        try:
            url = await self.url_q.get()
        except:
            pass
        return url


    async def create_parstask(self):#拼接解析任务
        i = 0
        while True:
            result =await self.result_q.get()#取到url解析相关的内容
            if result:
                collection = str(result['url']['guid']) + '_queue'  # 拼接到解析任务自己队列
                try:
                    queue_name = getattr(self, collection)
                except:
                    setattr(self, collection, queue.Queue(0))  # 没ut有队列就创建
                    queue_name = getattr(self, collection)
                finally:
                    queue_name.put(result)  # 添加数据
                if queue_name.qsize() >= result['url']['task_count']:  # 队列长度大等于任务的总url个数
                    task = self.local_task
                    task['topic'] = result['url']['callback']['topic']
                    for _ in range(result['url']['task_count']):
                        task['body']['result'].append(queue_name.get())
                        print (queue_name.qsize(),"**************",result['url']['task_count'])
                    self.send(task)#将解析任务添加到中间层
                    i += 1
                    print (task['body']['result'],' 生成解析********',i)
                    task['body']['result'] = []
                    pass  # 该任务拼接完成，可以生成解析任务。
                self.result_q.task_done()
            else:
                asyncio.sleep(0.1)

    async def parseUrl(self,url):
        try:
            await self.aiohttp_lib(url)
        except Exception as e:
            print('Failed....', e, url['url'])
            # return page

    async def aiohttp_lib(self,url):  #可用
        result = {'url': '', 'time': '', 'html': '',  'retry': 0,'sucess': False} #url字段对应了的内容包含所有内容
        # guid代表父任务id,count代表该任务总共有多少页


        html = ''
        method = url['method']  # 方法
        conn = aiohttp.TCPConnector(verify_ssl=False,
                                    limit=100,  # 连接池在windows下不能太大, <500
                                    use_dns_cache=True)

        headers = {}
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36 vulners.com/bot'})
        with (await self.semaphore):
            async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
                while True:
                    try:
                        if method == 'POST':
                            #with aiohttp.Timeout(0.1):设置请求的超时时间
                            async with session.post(url['url'], data=url['data'], headers=url['header']) as resp:
                                if resp.status == 200:
                                    html =await resp.text()

                                else:
                                    resp.release
                        elif method == 'GET':
                            async with session.get(url['url'], data=url['data'], headers=url['header']) as resp:
                                if resp.status == 200:
                                    html =await resp.text()

                                else:
                                    resp.release
                    except Exception as e:
                        if result['retry'] >= 5:
                            print('Get error', e)
                            raise e
                        result['retry'] += 1 #重试次数加1

                    if html:
                        result['sucess'] = True
                        result['html'] = html
                        break
                self.url_q.task_done()
                result['url'] = url
                result['time'] = time.time()
                await self.result_q.put(result)#将单个url的抓取结果放入队列
                self.count  += 1
                #print ('抓取*********',result,self.result_q.qsize())
                print ( url['task_count'],'****',self.count,'---------',self.result_q.qsize())






def catcher():
    print ('catcher')
    t = excutor_cls()
    t.run()

if __name__ =='__main__':

    #task = t.Access_to_task('get_task','',count=1)[0]
    #print (task)
    #t.catcher_interface(task)#抓取任务接口，因为本地任务是相同类型任务的集合，所以此接口内部一次只取一个任务，然后分解并发
    #t.parsing_interface(task)

    """
    for i in task_list:
        t.excutor_interface(i)
    """