#该脚本是负责操作客户端的数据接口
import zmq,json,time
from client_doc import setting
from client_doc import aps_client

class interface():
    def __init__(self):
        context = zmq.Context()
        self.inter_socket = context.socket(zmq.REP)  # 外部接口
        self.inter_socket.bind("tcp://*:" + setting.OUT_PORT)
        self.obj = aps_client.mongo_scan()
    def interface_job_task(self):#对外提供的接口
        #周期性接受数据
        #此接口主要负责操作本地任务列表和作业
        # 1.'command':'add',”task”:{} ，type= "task/job"  任务操作／作业操作
        # 2."command":"del"id“:’’,type= "task/job"
        # 3."command":"update",”content”:{},type= "task/job"
        # 4."command":'pop',”find”:’’,type= "task/job"
        response = {

            'success': True ,
            'error': "error reason",
            'content': 'value'

        }
        while True:
            try:
                mes = self.inter_socket.recv(zmq.NOBLOCK).decode('utf-8')# 接受到的请求数据，接受到是json格式的内容
            except zmq.ZMQError:
                time.sleep(0.1)
                continue
            mes = json.loads(mes)
            if mes['type'] == 'task':
                ret = getattr(self.obj, mes['command'] +'_task_list')(mes)  # 将arg整体传递给相应的操作
                response['content'] = ret
                if not ret:
                    response['success'] = False
            elif mes['type'] == 'job':
                ret = getattr(self.obj, mes['command'] + '_job')(mes)#作业操作
                if mes['command'] == 'pop':
                    response['content'] = ret
                    if not ret:
                        response['success'] = False
                else:
                    response['success'] = ret
            elif mes['type'] == 'data':#上传数据
                ret = getattr(self.obj, mes['command'] + '_data')(mes)  # 作业操作
                response['content'] = ret

            self.inter_socket.send(json.dumps(response).encode('utf-8'))


def run():
    inter_obj = interface()
    inter_obj.interface_job_task()
