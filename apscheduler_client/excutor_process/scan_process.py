

#说明：负责从中间层获取任务填充到队列的线程其实可以去掉，但是考虑到如果开启获取线程过多，必然增加了zmq的连接数，这样并不合理。
#而从中间层获取任务和填充队列的功能独立出来，而其他的线程只需要从队列得到任务即可，不需要连接zmq


import time,threading,zmq,sys
from multiprocessing import Process,Queue
import multiprocessing,os
from excutor_process import setting
from excutor_process import _interface
q = Queue()  #创建列队，不传数字表示列队不限数量，填充服务器任务的队列


class  system_fun:
    def __init__(self):
        self.context = zmq.Context()
        self.socket_excutor = self.context.socket(
            zmq.REQ)  # 向中间层获取任务端口
        self.socket_excutor.connect("tcp://localhost:" + setting.EXCUTOR_PORT)

        self.socket_add = self.context.socket(zmq.REQ)  # 向中间层添加本地任务端口
        self.socket_add.connect("tcp://localhost:" + setting.LOCAL_TASK_PORT)
        self.poll = zmq.Poller()
        self.poll.register(self.socket_excutor, zmq.POLLIN)
        self.poll1 = zmq.Poller()
        self.poll1.register(self.socket_add, zmq.POLLIN)
        self.inter_obj = _interface.oprate_task_job(setting.CENTER_INTERFACE_PORT)  # 通过中间层对客户端操作的对象,该对象提供对客户端操作的所有接口

    def send(self,
             task):  # 将任务添加到中间层的接口
        self.socket_add.send_json(task)
        while True:  # 服务器中断会一直尝试重连
            socks = dict(self.poll1.poll(3000))
            if socks.get(self.socket_add) == zmq.POLLIN:
                break
            else:  # 尝试重连
                print ('尝试重连中间层')
                self.socket_add.setsockopt(zmq.LINGER, 0)
                self.socket_add.close()
                self.poll1.unregister(self.socket_add)
                context = zmq.Context()
                self.socket_add = context.socket(zmq.REQ)
                self.socket_add.connect("tcp://localhost:" + setting.LOCAL_TASK_PORT)
                self.poll1.register(self.socket_add, zmq.POLLIN)
                self.socket_add.send_json(task)
        self.socket_add.recv_json()
        # 获取任务
    def Access_to_task(self, type='get_task', topic='test',count=1): # 从中间层获取任务，和查询某个类型的队列长度接口，type的类型决定
        req = {'type': type, 'topic': topic,
               'count': count}  # topic代表任务类型， count代表期望申请的任务个数,type :'get_task'（得到任务）/'get_size'（得到队列长度）不关心count

        req1 = {'type': 'get_size', 'topic': topic,
                'count': count}  # 得到队列的长度
        self.socket_excutor.send_json(req)
        while True:  # 服务器中断会一直尝试重连
            socks = dict(self.poll.poll(3000))
            if socks.get(self.socket_excutor) == zmq.POLLIN:
                break
            else:  # 尝试重连
                print("执行器尝试重连中间层")
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
        return task_list  # 申请到的任务链表
    def load_module(self):
        curdir = os.path.abspath(os.path.dirname(__file__))
        curdir = os.path.join(curdir, setting.SCRIPT_DIR)
        sys.path.append(curdir)

    def process(self):  #进程负责和中间层进行交互，开启线程
        self.load_module()# 加载脚本所在目录到系统目录
        process_list = []
        for i in range(setting.SUM_PROCESS_COUNT):#开启执行队列任务的进程，该进程会开启线程
            process_list.append(multiprocessing.Process(target=self.process_demo, args=(i,)))
        for process in process_list:
            process.start()  # 开启进程

        self.put_queue()

    def process_demo(self,pid):#开启线程的进程
        for i in range(setting.GET_THREADING_COUNT):
            t = threading.Thread(target=self.threading_get,
                                 args=(pid,i))  # 开启固定的线程，并将该进程所属的对象传递进去
            t.start()
        t.join()
    def threading_get(self,pid,i):  # 进程开启的线程,该线程只是从队列获取任务，得到任务调用脚本
        #线程负责调用相应的脚本,判断任务类型调用不同的脚本
        # 线程动态加载模块可能导致模块加载失败
        while True:
            try:
                result = q.get()  # 得到具体的任务，调用相应的脚本
                print(result, 'get task********', 'pid:', pid, 'tid:', i)
                topic = 'jd_task_kind'
                module_name = '.'.join((setting.SCRIPT_DIR, topic))
                m1 = __import__(module_name)  # 找到了脚本所在的目录
                script = getattr(m1, topic)  # 根据类型找到脚本
                cls = getattr(script, topic)()  # 根据类型找到脚本中的类，实例话
                #将任务的状态更改为执行状态2
                #self.inter_obj.update_task({setting.ROW_GUID:result['guid'],setting.ROW_STATUS:setting.STATUS_EXCUTING})
                cls.run(result)

            except Exception as e:
                print(e)

    def put_queue(self):#负责与中间层通信的进程，获取任务添加到队列
        #将轮询setting文件中的topic 依次获取任务
        obj = system_fun()
        while True:
            task_list = obj.Access_to_task(type='get_task', topic='jd_task_kind', count=setting.GET_COUNT)
            if task_list:
                for task in task_list:
                    q.put(task)
            else:
                time.sleep(0.2)

            """
            for topic in setting.TOPIC：
                task_list = obj.Access_to_task(type='get_task', topic=topic, setting.GET_COUNT)
                if task_list:
                    for task in task_list:
                        q.put(task)
            """

def process_main():#开启进程和线程的逻辑代码入口
    obj = system_fun()
    obj.process()

if __name__ == '__main__':
    obj = system_fun()
    # obj.threading_put()
    #obj.send({'topic': 'hello', 'value': 1})
   # obj.process()
    while True:
        for i in range(5):
            obj.send({'topic': 'hello', 'value': 1})

