
#此脚本将从中间层获取任务，执行器，抓取器，解析器，发送器的功能方法都封装,本地一个任务封装了一组相同类型的任务
#可进行业务拆分

"""
topic名称定义：
抓取任务：jm_crawl
解析任务：parsing
发送任务：send

"""

import time,queue
import motor.motor_asyncio
import asyncio,aiohttp


class excutor_cls:



    async def db_find(self, topic='JM_Crawl'):  # 只返回查找的第一条数据
        return await self.tb.find_one({'topic': topic})

    async def db_delete(self, arg):  # 删除数据
        await self.tb.remove(arg)

    async def db_insert(self, task):  # 插入数据
        # await self.tb.insert(task,upsert =True)
        a = await self.tb.update(
            {
                'topic': task['topic'],
            },
            task,
            True
        )

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



        self.semaphore = asyncio.Semaphore(100)
        self.url_q = asyncio.Queue()
        self.result_q = asyncio.Queue()


        #存放抓取任务的数据库
        conn = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = conn['pasrsing_data']
        self.tb = self.db['pasrsing_tb']
        #存放解析任务的数据库



    def run(self):
        tasks = []
        for _ in range(0, 100):
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
            task = await self.db_find('JM_Crawl') #从数据库查找一个抓取任务
            if task:
                await self.db_delete({'guid': task['guid']})#获取到该抓取任务后，应将数据库中该任务id的任务全部删除,防止重复抓取任务
                print('分解抓取任务***************')
                urls = task['body']['urls']
                guid = task['guid']
                callback = task['body']['callback']
                task_count= len(urls)
                for url in urls:
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
        j = 0
        while True:

            result = await self.result_q.get()#取到url解析相关的内容
            j += 1
            print('task *************************',j)
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
                    #将解析任务写到数据库
                    print ('reday插入数据库***********')
                    i += 1
                    #await self.db_insert(task)#插入数据库
                    await self.db_insert(task)  # 插入数据库
                    print(' 生成解析********', i)
                    task['body']['result'] = []
                self.result_q.task_done()
            else:
                await asyncio.sleep(0.1)



    async def parseUrl(self,url):
        try:
            await self.aiohttp_lib(url)
        except Exception as e:
            print('Failed....', e, url['url'])
            # return page

    async def aiohttp_lib(self,url):  #可用
        result = {'url': '', 'time': '', 'html': '', 'retry': 0, 'sucess': False}  # url字段对应了的内容包含所有内容
        headers = {}
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36 vulners.com/bot'})
        # guid代表父任务id,count代表该任务总共有多少页
        method = 'get'
        data = None
        html = None
        list = url.keys()
        all_list = ['data', 'header', 'method']
        for item in all_list:
            if item in list:
                if item == 'method':
                    method = url['method']
                elif item == 'data':
                    data = url['data']
                elif item == 'header':
                    headers = url['header']

        conn = aiohttp.TCPConnector(verify_ssl=False,
                                    limit=100,  # 连接池在windows下不能太大, <500
                                    use_dns_cache=True)
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
                            break
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
                #print ( url['task_count'],'****',self.count,'---------',self.result_q.qsize())



def catcher():
    print ('catcher')
    t = excutor_cls()
    t.run()

if __name__ =='__main__':
    t = excutor_cls()
    #t.test()
    t.run()
    #task = t.Access_to_task('get_task','',count=1)[0]
    #print (task)
    #t.catcher_interface(task)#抓取任务接口，因为本地任务是相同类型任务的集合，所以此接口内部一次只取一个任务，然后分解并发
    #t.parsing_interface(task)

    """
    for i in task_list:
        t.excutor_interface(i)
    """