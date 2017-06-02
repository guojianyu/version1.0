#0可以被扫描加入到工作队列中，1是可以被执行的，2是正在执行，3是超时，4是删除，5是完成。根据不同类型的任务操作也不一样
import datetime,zmq
import logging
from client_doc import setting
from bson import ObjectId
import json
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import *
from client_doc import request_server


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='ERROR.txt',
                    filemode='a')

class mongo_scan:
    def __init__(self):
        conn = MongoClient('localhost', 27017,connect=False)
        self.db = conn[setting.DATABASES]
        job_db = conn[setting.JOB_DB]
        self.job_tb = job_db[setting.JOB_COLL]
        self.scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

        """存储数据库"""
        data_db = conn[setting.DATA_DB]
        self.data_tb = data_db[setting.DATA_TB]

    def connect_push_zmq(self):
        context = zmq.Context()
        #  Socket to talk to server
        self.socket = context.socket(zmq.PUSH)  # 向中间层推任务端口
        self.socket.bind("tcp://*:" + setting.PUSH_PORT)
    """操作数据库总任务链表的方法"""
    def add_task_list(self,arg):
        ret = self.db[setting.TASKS_LIST].update(
            {
                 setting.ROW_TOPIC: arg['task'][setting.ROW_TOPIC],
                 setting.ROW_GUID:  arg['task'][setting.ROW_GUID]
            },
            arg['task'],
            True
        )
        ret = {'updatedExisting':ret['updatedExisting'], 'ok':ret[ 'ok']}
        #ret = self.db[setting.TASKS_LIST].insert(arg['task'])
        print ("add_task:")
        return ret
    def del_task_list(self,arg):
        ret = self.db[setting.TASKS_LIST].remove({setting.ROW_GUID:arg[setting.ROW_GUID]})
        return ret
    def update_task_list(self,arg):
        ret = self.db[setting.TASKS_LIST].update({setting.ROW_GUID:arg['content'][setting.ROW_GUID]},{'$set':arg['content'] })
        return ret
    def pop_task_list(self,arg):#目前提供的对外接口只能精确查找
        ret = self.db[setting.TASKS_LIST].find_one({setting.ROW_GUID:arg['pop']})
        if ret:
            ret["_id"] = ObjectId(ret['_id']).__str__()
        return ret
    def operat_task(self,arg):#操作总任务链表的接口
        # 1.'command':'add',”task”:{}
        # 2."command":"del"guid“:’’,
        # 3."command":"update",”content”:{},
        # 4."command":'pop'，topic:'',
        getattr(mongo_scan,arg['command']+'_task_list')(self,arg)#将arg整体传递给相应的操作
    def time_datetime(self, time):  # 将数据库中的time转换成aps识别的datetime
        return datetime.datetime.fromtimestamp(time)

    def scan_task(self):#扫描任务队列为0状态的任务,这个方法会作为一个周期性任务执行

        table = self.db[setting.TASKS_LIST]
        result = table.find_and_modify(query={setting.ROW_STATUS: setting.STATUS_DELAY},
                                           update={'$set': {setting.ROW_STATUS: setting.STATUS_READY}})

        if result:
            self.aadd_job(result)
        #然后将找到为加入工作队列的任务加入工作队列
    def aadd_job(self,task):#增加作业

        id = ':'.join([task[setting.ROW_TOPIC], str(task[setting.ROW_GUID])])
        print ("****add",id)
        if task['topic']:#周期性任务
            print ("周期性任务")
            self.scheduler.add_job(func=aps_test, args=('循环任务',task),trigger='interval',
                                  seconds=3,id=id)
            pass
        elif task['topic'] == 2:#定时性任务
           self.scheduler.add_job(func=aps_test, args=(task,), trigger='cron', start_date=task['time'],
                                   second=task['interval'],id = id )

        elif task['topic'] == 3:#一次性任务
            self.scheduler.add_job(func=aps_test, args=('循环任务',), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12),
                              id=id)  # 每2小时执行一次  周期任务


    def add_job(self, mes):  # 增加作业对外接口
        task = mes['task']
        ret = True

        id = ':'.join([task[setting.ROW_TOPIC],str(task[setting.ROW_GUID])])
        print("****add", id)
        if task[setting.ROW_TOPIC]:  # 周期性任务

            print("周期性任务")
            try:
                self.scheduler.add_job(func=aps_test, args=('循环任务', task), trigger='interval',
                              seconds=3, id=id)
            except:
                ret = False

        elif task[setting.ROW_TOPIC] == 2:  # 定时性任务
            try:
                self.scheduler.add_job(func=aps_test, args=(task,), trigger='cron', start_date=task['time'],
                              second=task['interval'], id=id)
            except:
                ret = False

        elif task[setting.ROW_TOPIC] == 3:  # 一次性任务
            try:
                self.scheduler.add_job(func=aps_test, args=('循环任务',),
                              next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12),
                            id=id)  # 每2小时执行一次  周期任务
            except:
                ret = False
        return ret
    def del_job(self,mes):#删除任务
        #参数为任务id
        ret = True
        try:
            self.scheduler.remove_job(mes['job_id'])
        except:
            ret = False
        return ret
    def pause_job(self,mes):# 暂停作业
        self.scheduler.pause_job(mes['job_id'])
    def resume_job(self,mes):#恢复作业
        self.scheduler.resume_job(mes['job_id'])
    def update_job(self,mes):#更新作业
        #更改触发器
        ret = True
        try:
            self.scheduler.reschedule_job(mes['content']['job_id'], trigger='cron', second='*/5')
        except :
            ret = False

        #修改除了id  的所有属性
        """
        job_id = mes['content']['job_id']
        dat= mes['content'].pop('job_id')
        print (mes['content'])
        ret = scheduler.modify()
        """
        return ret
    def pop_job(self,mes):#查找作业
        ret = None
       # ret = self.job_tb.find_one({"_id":mes['job_id']})
        job = self.scheduler.get_job(mes['job_id'])
        if job:
            ret = {"fuc":job.func_ref,"next_run_time":str(job.next_run_time),"id":job.id}
        return ret
    """接收到上传数据的接口"""
    def upload_data(self,mes):
        format_data = {'sku':'','spu':'',}
        #对上传的数据进行存储，根据不同的类型数据不同的操作
        self.data_tb.insert(mes)
        return 'recv data'



    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
    def clear_local_task(self):#清空作业链表，代码重启就会清空所有的作业
        self.job_tb.remove()#清空
    def add_local_task(self):# 作业链表中增加本地任务

        # 定时上报服务器的任务都会成为启动的周期任务
        # 扫描未加入工作队列的任务作为周期任务
        self.scheduler.add_job(func=scan_task, args=(),
                          trigger='interval', seconds=setting.UPDATE_TASK_LIST_TIME, id=setting.SCAN_TASK)


        for local_id in setting.LOCAL_TASK_LIST:#将与服务器定时交互的任务作为本地任务
            func = getattr(request_server,local_id)
            time = getattr(setting,local_id.upper()+'_TIME')#拼接本地任务的时间
            self.scheduler.add_job(func=func, args=(),
                                  trigger='interval', seconds=time, id=local_id)

        """
         # 定时更新任务列表
        self.scheduler.add_job(func=request_server.update_task_list, args=(),
                          trigger='interval', seconds=setting.UPDATE_TASK_LIST_TIME, id=setting.UPDATE_TASK_LIST)

        # 批量更新任务状态
        self.scheduler.add_job(func=request_server.update_much_taskinfo, args=(),
                          trigger='interval', seconds=setting.UPDATE_MUCH_TASKINFO_TIME,
                          id=setting.UPDATE_MUCH_TASKINFO)

        # 批量上报服务器的设备信息
        self.scheduler.add_job(func=request_server.upload_client_status, args=(),
                          trigger='interval', seconds=setting.UPLOAD_CLIENT_STATUS_TIME,
                          id=setting.UPLOAD_CLIENT_STATUS)
        #批量上报数据
        self.scheduler.add_job(func=request_server.upload_client_data, args=(),
                               trigger='interval', seconds=setting.UPLOAD_CLIENT_DATA_TIME,
                               id=setting.UPLOAD_CLIENT_DATA)



        #更新代理数据
        self.scheduler.add_job(func=request_server.update_proxy_data, args=(),
                               trigger='interval', seconds=setting.UPDATE_PROXY_DATA_TIME,
                               id=setting.UPDATE_PROXY_DATA)
        #更新cookie数据
        self.scheduler.add_job(func=request_server.update_cookie_data, args=(),
                               trigger='interval', seconds=setting.UPDATE_COOKIE_DATA_TIME,
                               id=setting.UPDATE_COOKIE_DATA)
        """

    def check_local_task(self):  # 检查是否添加过本地任务,没有则添加，添加过则跳过
        if not self.job_tb.find({'_id': setting.SCAN_TASK}).count():#扫描任务
            self.scheduler.add_job(func=scan_task, args=(),
                                   trigger='interval', seconds=setting.UPDATE_TASK_LIST_TIME, id=setting.SCAN_TASK)
        for local_id in setting.LOCAL_TASK_LIST:
            if not self.job_tb.find({'_id':local_id}).count():
                func = getattr(request_server,local_id)
                time = getattr(setting,local_id.upper()+'_TIME')#拼接本地任务的时间
                print ('**********',time)
                self.scheduler.add_job(func=func, args=(),
                                      trigger='interval', seconds=time, id=local_id)

    def run(self):
        if setting.PULSE_ON_TYPE == setting.CLEAR:#选择启动方式
            self.clear_local_task()#清空作业链表
            self.add_local_task()#本地任务作为周期任务启动
        elif setting.PULSE_ON_TYPE == setting.CHECK:
            self.check_local_task()#不删除作业，只检查本地作业是否启动完毕
        self.scheduler.start()

def aps_test(x,task):#
    #x是任务属性
    #此处将任务状态置为2（正在执行）TASK_STATUS['EXCUTE']
    """
    table = obj.db[setting.TASKS_LIST]
    table.find_and_modify(query={'guid': task['guid']},
                          update={'$set': {'status': setting.STATUS_EXCUTING}})
    """
    #从作业队列中删错
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    try:
        task['_id'] = ObjectId(task['_id']).__str__()
    except:
        pass
    obj.socket.send_json(task)


def scan_task():
    obj.scan_task()

def aps_pause():
    #print (1/0)
    #scheduler.pause_job('interval_task')
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '一次性任务')

def aps_resume(obj):
     #scheduler.resume_job('interval_task')
     print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '一次性任务1')
     #obj.scheduler.add_job(func=aps_resume, args=(obj,),
                          # next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=24), id='resume_task')



#从mongo中获取任务，因为要指定任务的开始执行时间，和id已经从mongo中得到任务的具体内容，args把整体任务传递进去，避免了在func中再次查询
#


host = '127.0.0.1'
port = 27017
client = MongoClient(host, port,connect=False)

jobstores = {
    #'mongo': MongoDBJobStore(collection='job', database='aps_all_copy', client=client),
    'default': MongoDBJobStore(collection='job', database='aps_all_copy', client=client),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

obj = ''
def main():
    print ('aps_client')
    global  obj
    obj = mongo_scan()
    obj.connect_push_zmq()
    obj.run()
if __name__ == '__main__':
    obj = mongo_scan()
    obj.connect_push_zmq()
    obj.run()







#obj.scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron',start_date= tm+datetime.timedelta(seconds=5),second='*/5',id='cron_task')#每分

#scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron',start_date= tm,second='2',id='cron_task')#每分2秒的时候会执行，定时任务
#scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', hours=2, id='interval_task')#每2小时执行一次  周期任务
#obj.scheduler.add_job(func=aps_resume, args=('b',), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=24), id='resume_task')
#scheduler.add_job(func=aps_test, args=('循环任务',), trigger='interval', seconds=3, id='interval_task')
