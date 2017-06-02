import time,threading,zmq,uuid
from multiprocessing import Process,Queue
import multiprocessing
import setting
import _interface

q = Queue()  #创建列队，不传数字表示列队不限数量
class  system_fun:
    def __init__(self):
        context = zmq.Context()
        self.socket_excutor = context.socket(
            zmq.REQ)  # 向中间层获取任务端口
        self.socket_excutor.connect("tcp://localhost:" + setting.EXCUTOR_PORT)

        self.socket_add = context.socket(
            zmq.REQ)  # 向中间层添加本地任务端口
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
                print("重连")
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


    def interface(self,dict):#参数必须是一个字典
        next_topic = str(uuid.uuid1())#根据时间戳生成随机的uuid
        task = {'topic': 'JM_Crawl',
                'guid': dict['guid'],  # 沿用服务器下发的任务id
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
                        'callback': {'topic':next_topic},
                    }
                }
        task.update(dict)#有值则更新，没值则默认
        self.send(task)
        while True:
            # 从中间层获得topc = 'JM_Crawl_Result'+'guid' 的任务
            task = self.Access_to_task('get_task', next_topic + 'guid')
            if task:
                return task
            else:
                time.sleep(0.1)

if __name__ == '__main__':
    arg = {

        'urls':[],'guid':1
        }


    obj = system_fun()
    obj.interface(arg)#接口参数为字典