# 相当于执行器的中间层，主要负责接受所有类型的任务，并且存储到不同的队列，
#关于zmq 传递数据：
#zmq接受到的数据如果与调度中心完全隔离就应该传递的是整个任务属性，如果不隔离只需要传递guid即可，但是会重复查询数据库
#综合考虑zmq传递的数据为整个任务属性

#aps存在的问题，
# 同一时间可以入队的任务受aps设置的最大进程数制约，也就是说
# 同一时间执行的任务不可以大于aps的进程数，大于部分无法入队将得不到执行

#解决方案，该执行的任务都为周期性任务，任务入zmq的时候改变

import zmq,asyncio
import queue,json
from center_layer import center_setting
import threading
from center_layer import interface#操作客户端作业和总列表的文件



class work:
    def __init__(self):
        #创建操作作业和总任务列表的接口对象
        #对客户端操作的接口对象
        self.client_inter = interface.oprate_task_job(center_setting.CLIENT_INTERFACE_PORT)#它的端口指向客户端

        """中间层链接到调度中心"""
        context = zmq.Context()
        self.socket = context.socket(zmq.PULL)
        self.socket.connect("tcp://localhost:"+center_setting.CENTER_PORT)

        """本地任务进入中间层的端口"""
        self.socket_local = context.socket(zmq.REP)
        self.socket_local.bind("tcp://*:"+center_setting.LOCAL_TASK_PORT)
        """绑定执行器"""
        self.socket_excutor = context.socket(zmq.REP)
        self.socket_excutor.bind("tcp://*:"+center_setting.EXCUTOR_PORT)

        """外部通过中间层修改客户端作业和总任务列表的端口"""
        self.socket_inter = context.socket(zmq.REP)
        self.socket_inter.bind("tcp://*:"+center_setting.CENTER_INTERFACE_PORT)
        #用于接受数据

    async def operate_client_inter(self):# 抓取器通过中间层对客户端上传数据，总任务列表，和作业操作的中间接口,转发
        while True:
            await asyncio.sleep(0)
            try:
                mes = self.socket_inter.recv(zmq.NOBLOCK).decode('utf-8')  # 接受到的请求数据，接受到是json格式的内容
            except zmq.ZMQError:
                await asyncio.sleep(0.1)
                continue
            mes = json.loads(mes)
            ret = getattr(self.client_inter,'send')(mes)  # 将arg整体传递给功能函数，发送到客户端
            self.socket_inter.send_json(ret)

    async def get_task(self):#从调度中心获取任务
        while True:
            await asyncio.sleep(0)
            try:
                task = self.socket.recv(zmq.NOBLOCK).decode('utf-8')  # 接受到的请求数据，接受到是json格式的内容
            except zmq.ZMQError:
                await asyncio.sleep(0.1)
                continue
            task = json.loads(task)
            self.queue(task)#队列操作
    async def get_local_task(self):
        while True:
            await asyncio.sleep(0)
            try:
                task = self.socket_local.recv(zmq.NOBLOCK).decode('utf-8')  # 接受到的请求数据，接受到是json格式的内容
            except zmq.ZMQError:
                await asyncio.sleep(0.1)
                continue
            task = json.loads(task)
            self.queue(task)  # 队列操作
            self.socket_local.send_json({"ret":'ok'})
    def queue(self,task):
        #将各个类型任务放入不同的就绪队列
        queue_name = task['topic']+"_ready_list"# 拼接就绪队列，相当于表
        self.cache_insert(queue_name,task)#存储接口

    def cache_insert(self,collection,data):#中间层数据存储
        #collection集合名（表），data存储的数据
        """queue"""
        try:
            queue_name = getattr(self,collection)
        except:
            setattr(self,collection,queue.Queue(0))#没有队列就创建
            queue_name = getattr(self, collection)
        finally:
            queue_name.put(data)#添加数据
    def cache_pop(self,collection,count):
        #collection集合名称， count个数
        task_list = []
        task_count = 0
        try:
            queue_name = getattr(self,collection)
        except:
            pass
            #没有该类型的任务
        while True:
            try:
                if count == task_count:
                    break
                else:
                    task = queue_name.get(block=False)

                    if not queue_name.qsize():#如果队列为空，则删除该队列属性
                        pass
                        #delattr(self,collection)
                    task_list.append(task)  # 将任务追加到返回列表中
                    task_count +=1
            except:
                break

        return task_list#任务列表
    def excutor_req(self,request):#执行器请求任务接口 需要提供任务类型和希望得到的个数，应该返回到执行器的中间层，执行器中间层负责任务的并发
        #1.根据类型得到就绪队列
        #2.根据个数决定返回的任务个数，如果就绪队列的任务小于请求个数则返回全部
        #3.返回格式 链表【task1，task2】
        queue_name = request['topic']+"_ready_list"#得到就绪队列
        count = request['count']
        ret = self.cache_pop(queue_name,count)
        return ret
    def send(self,content):#回复执行器的接口
        self.socket_excutor.send_json(content)

    def get_qsize(self,topic):# 查询队列长度的接口
        queue_name =topic + "_ready_list"  # 得到就绪队列
        try:
            queue_name = getattr(self, queue_name)
        except:
            return 'invalide queue'
            # 没有该类型的任务
        return queue_name.qsize()
    async def recv(self):#得到执行器的请求
        while True:
            await asyncio.sleep(0)
            #request = self.socket_excutor.recv_json()
            try:
                request = self.socket_excutor.recv(zmq.NOBLOCK).decode('utf-8')  # 接受到的请求数据，接受到是json格式的内容
            except zmq.ZMQError:
                await asyncio.sleep(0.1)
                continue
            request = json.loads(request)
            #result 的格式：{'topic':'','count':}
            if request['type'] == 'get_task':
                task_list = self.excutor_req(request)#得到就绪任务
                self.send(task_list)#回复
            elif request['type'] == 'get_size':
                self.send(self.get_qsize(request['topic']))#得到队列长度
    def run(self):#中间层的启动方法
        #与调度中心拉取任务和得到执行的请求为两个独立的任务,多进程实现或多线程实现

        """异步实现"""
        loop = asyncio.get_event_loop()
        tasks = []
        tasks.append(self.get_task())
        tasks.append(self.get_local_task())
        tasks.append(self.recv())
        tasks.append(self.operate_client_inter())
        f = asyncio.wait(tasks)
        loop.run_until_complete(f)


def main():
    obj = work()
    obj.run()
if __name__ == "__main__":
    obj = work()
    obj.run()
