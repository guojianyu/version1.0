
#解析服务器下发的任务，然后批量生成本地任务
import zmq
import setting
import requests

context = zmq.Context()
socket_excutor = context.socket(zmq.REQ)
socket_excutor.connect("tcp://localhost:"+setting.EXCUTOR_PORT)
context = zmq.Context()
socket = context.socket(zmq.REQ)#中间层端口
socket.connect("tcp://localhost:"+setting.LOCAL_TASK_PORT)

task = {"topic":'crawl','method':'get','url':'http://www.jd.com'}
def send(task):
    socket.send_json(task)
    socket.recv_json()

def Resolving_server_tasks(topic,count=1):
    req = {'topic': topic, 'count':count}
    while True:
        socket_excutor.send_json(req)
        data = socket_excutor.recv_json()
        url_list = []
        print (data)
        for task in data:
            #解析服务器下发的任务
            obj = jd_task_kind.jd_task_kind()
            url_list = obj.get_urls(task)#得到解析后批量生成的url,是一个链表


        for index, item in enumerate(url_list):
            urlTask = {'topic':'kind', 'url': item}
            send(urlTask)#将得到的本地任务添加到中间层
            print (urlTask)
            print ('----------------')


if __name__ =='__main__':
    a = send({'topic':'hello','value':111112222})
    print (a)
    #Resolving_server_tasks('kind', count=1)#解析服务器任务，批量生成本地任务
    req = {'type':'get_size','topic': 'hello', 'count':4}
    socket_excutor.send_json(req)
    data = socket_excutor.recv_json()
    print (data)
