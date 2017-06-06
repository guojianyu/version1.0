
# 此脚本是负责和中间层同心，修改客户端的任务列表和作业

import zmq,time
import json,socket
import logging


class oprate_task_job:
    def __init__(self,port = 9995):#端口要与本地setting。OUT_PORT 一致
        context = zmq.Context()
        self.port = str(port)
       # print('connect to server')
        self.socket = context.socket(zmq.REQ)
        self.socket.connect('tcp://localhost:'+self.port)
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)
        """日志"""
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='a')
        #################################################################################################
        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        #################################################################################################

    def _port_is_free(self,port):#检查端口是否被占用,可用返回true
        s = socket.socket()
        s.settimeout(0.5)
        try:
            # s.connect_ex return 0 means port is open
            return s.connect_ex(('localhost', port)) != 0
        finally:
            s.close()
    def add_task(self,task): #成功返回的是——id
        mes = {'command':'add',"task":task,'type':'task'}
        self.send(mes)
        return self.recv()
    def del_task(self,id):# 'content': {'ok': 1.0, 'n': 1}}
        mes = {'command':'del',"guid":id,'type':'task'}
        self.send(mes)
        return self.recv()
    def update_task(self,arg):#content': {'nModified': 1, 'n': 1, 'ok': 1.0, 'updatedExisting': True} content': {'ok': 1.0, 'updatedExisting': False, 'n': 0, 'nModified': 0}
        #arg = {"guid":14,"device.id":"guojianyu"}#arg的格式
        mes = {'command': 'update', "content": arg, 'type': 'task'}
        self.send(mes)
        return self.recv()
    def pop_task(self,arg):#支持精确查找返回一个查找结果，只支持精确查找
        #arg = {"guid": 12, "device.id": "guojianyu"}#查找任务的格式
        mes = {'command': 'pop', "pop":arg, 'type': 'task'}
        self.send(mes)
        return self.recv()

    def add_job(self,task):#添加作业
        #需要传递整个任务属性，服务器会根据topic来确定任务类型，同过任务属性来确定生成的作业的周期等信息
        mes = {'command': 'add', "task": task, 'type': 'job'}
        self.send(mes)
        return self.recv()
    def del_job(self,id):#删除作业   只关心success的标示
        mes = {'command': 'del', "job_id": id, 'type': 'job'}
        self.send(mes)
        return self.recv()
    def update_job(self,arg):#更新作业   只关心success的标示
        mes = {'command': 'update', "content":{}, 'type': 'job'}
        mes['content'] = {'job_id':'sku131',' seconds':6}
        self.send(mes)
        return self.recv()
    def pop_job(self,id):#查找作业
        mes = {'command': 'pop', "job_id": id, 'type': 'job'}
        self.send(mes)
        return self.recv()
    def pause_job(self,id):#暂停作业   不需要关心返回值
        mes = {'command': 'pause', "job_id": id, 'type': 'job'}
        self.send(mes)
        return self.recv()
    def resume_job(self,id):#回复作业   不需要关心返回值
        mes = {'command': 'resume', "job_id": id, 'type': 'job'}
        self.send(mes)
        return self.recv()

    def send(self,mes):
        self.socket.send(json.dumps(mes).encode('utf-8'))
        while True:#服务器中断会一直尝试重连
            socks = dict(self.poll.poll(3000))
            if socks.get(self.socket) == zmq.POLLIN:
                break
            else:
                self.socket.setsockopt(zmq.LINGER, 0)
                self.socket.close()
                self.poll.unregister(self.socket)
                context = zmq.Context()
                self.socket = context.socket(zmq.REQ)
                self.socket.connect('tcp://localhost:'+self.port)
                self.poll.register(self.socket, zmq.POLLIN)
                self.socket.send(json.dumps(mes).encode('utf-8'))

    def recv(self):
        return self.socket.recv_json()

    def write_log(self,arg):#写日志 arg的格式 {'level':,'content':....}level是写扫描类型的日志，content是日志内容
        level= arg['level']#得到日志等级
        content = arg['content']# 日志内容
        if level == 'info':
            logging.info(content)
        elif level == 'debug':
            logging.debug(content)
        elif level == 'warning':
            logging.warning(content)
        elif level == 'error':
            logging.error(content)


    def upload_data(self,content):#上传数据接口
        mes = {'command': 'upload', "content": content, 'type': 'data'}
        self.send(mes)
        return self.recv()
if __name__ == "__main__":
    level = ['info','debug','warning','error']

    task = {"device":
                {'type': "", 'version': '127.22', 'id': ''},
            'guid': 14, 'time': time.time(), 'timeout': 40, 'topic': 'jd_task_kind',
            'interval': 6000,  # 任务执行周期间隔时间
            'suspend': 0,  # 暂停标识
            'status': 0,

            'body': {
                'kind': '9987,830,866', 'platform': 'jd_app', 'sort': None,
                "url": "https://list.jd.com/list.html?",
                "maxpage": 0,
                'shopid':1,
                "cookie_type": "jd_web",
                'key_search': 0,
                "data": {
                    'key_word': '',
                    "cat": "670,671,672",
                    "sort": "sort_rank_asc",
                    "trans": "1",
                    "page": "1",
                    "JL": "6_0_0"
                }
            }}

    obj = oprate_task_job(9995)
    arg = {'level':'info','content':'aps_all_copy'}
    ret = obj.add_task(task)
    print (ret)


