import zmq,time
import json,socket
import logging


class oprate_task_job:
    def __init__(self,port = 9000):
        self.port = str(port)
        context = zmq.Context()
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
        return self.recv()
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

if __name__ == "__main__":
    level = ['info','debug','warning','error']
    task = {"device":
                {'type': "", 'version': '127.22', 'id': ''},
            'guid': 13, 'time': time.time(), 'timeout': 4000, 'topic': 'sku',
            'interval': 6000,  # 任务执行周期间隔时间
            'suspend': 0,  # 暂停标识
            'status': 0,

            'body': {
                "url": "https://list.jd.com/list.html?",
                "maxpage": 0,
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



