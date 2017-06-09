#该脚本负责将任务添加到作业，和对作业操作的功能方法
from apscheduler.schedulers.blocking import BlockingScheduler
import setting,log
from apscheduler.jobstores.mongodb import MongoDBJobStore
import datetime
from pymongo import MongoClient
import logging,json,zmq
from bson import ObjectId
import logging
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import *
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='ERROR.txt',
                    filemode='a')
host = '127.0.0.1'
port = 27017
client = MongoClient(host, port,connect=False)

jobstores = {
    #'mongo': MongoDBJobStore(collection='job', database='aps_all_copy', client=client),
    'default': MongoDBJobStore(collection=setting.JOB_COLL, database=setting.JOB_DB, client=client),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 3,
    'misfire_grace_time': 30
}

class task_opt:  #数据库操作的类
    #超时任务的数据库操作逻辑
    def timeout_query(self,obj,task):
        table = obj.db[setting.TASKS_LIST]  # 进入总任务队列表
        task1 = table.find_and_modify(query={'guid': task['guid']},update={'$set': {'status': 3}})  #将任务状态更改为3（超时状态   ）
        timeout_name = task['topic'] + '_timeout_list'#拼接超时队列
        queued_name = task['topic'] + '_ready_list'  # 表      根据类型拼接到自己类型所在的就绪任务队列
        obj.db[queued_name].remove({'guid': task['guid']})  # 删除就绪列表的id
        obj.db[timeout_name].update(
            {
                setting.ROW_GUID: task[setting.ROW_GUID]
            },
            {'guid':task[setting.ROW_GUID]},
            True
        )
        #obj.db[timeout_name].insert({'guid':task['guid']})#将id加入到超时队列中
        if task1['device']['id']:#将被分配过的任务记录，为了被剥夺任务的客户端删除任务
            obj.db[setting.RECODE_LIST].insert({'id':task['guid'],'device_id':task['device']['id']})#将任务id和该任务上次分配设备id存储到记录列表中#将任务置为暂停
            #这样在客户端更新任务列表时，当其他设备执行了该超时任务时，服务器会通知客户端删除该任务
        pass
    #扫描总任务列表将任务转变为作业
    def task_job(self,obj):
        table = obj.db[setting.TASKS_LIST]
        task = table.find_and_modify(query={'status': 0, "device.id": ""},
                              update={'$set': {'status': 1}})
        if task:
            queue_set = task['topic'] + "_ready_list"  # 根据任务的topic标识+ready_list 拼接成各个任务属性的就绪队列名称
            ID = task['guid']
            if not obj.db[queue_set].find({'guid': ID}).count():
                task_opt.insert_table(obj.db, queue_set, {'guid': ID})  # 将各种任务id添加到相应的任务就绪列表
        return task#返回找到的任务，没有则为none
    @staticmethod
    def insert_table(db, table, data):  # 将数据插入任务列表
        tb = db[table]
        tb.update(
            {
                setting.ROW_GUID: data[setting.ROW_GUID]
            },
            data,
            True
        )
        #tb.insert(data)


def timeout_cute(task):#超时时间到了，任务开始执行，然后将任务放入超时队列中3
    c_task = job.db[setting.TASKS_LIST].find_one({'guid':task['guid']})
    #job.write_log({'level':'info','content':'ok'}) 写日志操作。
    if c_task['status'] < 3:# 任务超时
        # 将超时的任务添加到超时队列
        print ('超时')
        data_opt.timeout_query(job,task) # 对数据库的操作,任务状态变为3
        #暂停任务，防止重复扫描
    elif c_task['status'] == 3:#上次已经超时
        #删除该任务，或者更改作业的执行时间
        pass
        #status = 3，表示上次已经分配过了，error_count +=1 ,超时次数+1，当达到某一个值时，将任务删除或者写日志。
        """
        task['timeout_count'] += 1
        if task['timeout_count'] >=5:
            job.db[setting.RECODE_ERROR_LIST].insert(task)#将超时次数达到最大超时次数的任务写入记录表中
            job.db[setting.TASKS_LIST].remove(task)#将任务从总任务列表删除
        """
    elif c_task['status'] == 4:#一次性任务，执行完成，删除
        job.db[setting.TASKS_LIST].remove({'guid':task['guid']})
        pass
    elif c_task['status'] == 5:#周期性任务，完成状态,将状态置为1，等待执行状态
        job.db[setting.TASKS_LIST].find_and_modify(query={'guid': task['guid'],},
                              update={'$set': {'status': 1}})

def scan_task():#周期性任务，将未加入工作队列和没有被分配的的任务添加到工作队列（就绪列表）

    result = data_opt.task_job(job)
    #得到未添加到工作队列的任务
    if result:
        print("scan>>>", result, bool(result))
        job.aadd_job(result)#将任务添加到工作队列
    #print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),result)
    #添加作业的任务执行开始时间是time+timeout

def aps_test(x):
      #x是任务属性
    #此处将任务状态置为2（正在执行）f aps_one(task):#一次性任务
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    #对task的操作
    pass

def aps_time(task):#定时任务
    #对task的操作
    pass
def aps_interval(task):#周期性任务
    #对task的操作
    pass
def aps_pause(obj):
    #print (1/0)
    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), obj)
class server_job:
    def __init__(self):
        """日志相关"""
        self.log = log.log()
        #链接总任务链表数据库
        conn = MongoClient('localhost', 27017,connect=False)
        self.db = conn[setting.DATABASES]
        #链接作业数据库
        self.job_db = conn[setting.JOB_DB]
        context = zmq.Context()
        self.inter_socket = context.socket(zmq.REP)
        self.inter_socket.bind("tcp://*:" + setting.OUT_PORT)


    def add_task_list(self, arg):

        ret = self.db[setting.TASKS_LIST].update(
            {
                setting.ROW_TOPIC: arg['task'][setting.ROW_TOPIC],
                setting.ROW_GUID: arg['task'][setting.ROW_GUID]
            },
            arg['task'],
            True
        )
        ret = {'updatedExisting': ret['updatedExisting'], 'ok': ret['ok']}

        #ret = self.db[setting.TASKS_LIST].insert(arg['task'])
        #print("add_task:", ret)

        return ret
    def del_task_list(self, arg):
        ret = self.db[setting.TASKS_LIST].remove({'guid': arg['guid']})
        return ret

    def update_task_list(self, arg):
        ret = self.db[setting.TASKS_LIST].update({'guid': arg['content']['guid']}, {'$set': arg['content']})
        return ret

    def pop_task_list(self, arg):  # 目前提供的对外接口只能精确查找
        ret = self.db[setting.TASKS_LIST].find_one({'guid': arg['pop']})
        if ret:
            try:
                ret["_id"] = ObjectId(ret['_id']).__str__()
            except:
                pass
        return ret

    def operat_task(self, arg):  # 操作总任务链表的接口
        # 1.'command':'add',”task”:{}
        # 2."command":"del"guid“:’’,
        # 3."command":"update",”content”:{},
        # 4."command":'pop'，topic:'',
        getattr(server_job, arg['command'] + '_task_list')(self, arg)  # 将arg整体传递给相应的操作
    """以上和总任务列表相关"""


    def time_datetime(self,time):# 将数据库中的time转换成aps识别的datetime
        return datetime.datetime.fromtimestamp(time)
    def aadd_job(self, task):  # 增加作业
        print ("*****************add_task")
        # 通过task 的topic确定任务需要调用
        # 添加的任务id是由任务类型和任务id拼接而成的
        # trigger的触发类型根据topic类型来选择
       # id = task['topic'] + str(task['guid'])
        id = ':'.join([task[setting.ROW_TOPIC], str(task[setting.ROW_GUID])])
        task['time'] = self.time_datetime(task['time'])
        if task['topic']:  # 一次性任务
            print ('addd_job')
            """
            scheduler.add_job(func=timeout_cute, args=(task,), trigger='cron', second='*/5',
                                                 id=id)  # 每5s执行一次
            """
            try:
                scheduler.add_job(func=timeout_cute, args=(task,),trigger='interval',seconds=task['interval'],
                                  next_run_time=task['time'],id=id)
            except:
                pass
        elif task['topic'] == 2:  # 定时性任务
            try:
                scheduler.add_job(func=timeout_cute, args=(task,), trigger='cron', hours=2,
                               id=id)  # 每2小时执行一次  定时任务任务
            except:
                pass
        elif task['topic'] == 3: # 周期性任务
            try:
                scheduler.add_job(func=timeout_cute, args=(task,), trigger='interval', start_date=task['time']+task['timeout'],
                              seconds=task['interval'], id=id)
            except:
                pass
    """start操作作业的外部接口"""
    def add_job(self, mes):  # 增加作业对外接口

        task = mes['task']
        ret = True
        # 通过task 的topic确定任务需要调用
        # 添加的任务id是由任务类型和任务id拼接而成的
        # trigger的触发类型根据topic类型来选择

        # 将任务放到zmq中，抓取器只要从zmq中取任务就可以，解耦合，抓取器可以高并发。
        # 执行作业只是将任务属性添加到zmq即可。
        #id = task['topic'] + ':' + str(task['guid'])
        id = ':'.join([task[setting.ROW_TOPIC],str(task[setting.ROW_GUID])])
        print("****add", id)
        print("周期性任务")
        if task[setting.ROW_TOPIC]:  # 周期性任务
            try:
                scheduler.add_job(func=timeout_cute, args=(task,), trigger='interval',
                              seconds=task['interval'], id=id)
            except:
                pass

            """
            try:

                scheduler.add_job(func=aps_test, args=('循环任务', id), trigger='interval',
                              seconds=3, id=id)
            except:
                ret = False
            """

        elif task[setting.ROW_TOPIC] == 2:  # 定时性任务
            try:
                scheduler.add_job(func=aps_test, args=(task,), trigger='cron', start_date=task['time'],
                              second=task['interval'], id=id)
            except:
                ret = False

        elif task[setting.ROW_TOPIC] == 3:  # 一次性任务
            try:
                scheduler.add_job(func=aps_test, args=('循环任务',),
                              next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12),
                            id=id)  # 每2小时执行一次  周期任务
            except:
                ret = False
        return ret
    def del_job(self,mes):#删除任务
        #参数为任务id

        ret = True
        try:
            scheduler.remove_job(mes['job_id'])
        except:
            ret = False
        return ret
    def pause_job(self,mes):# 暂停作业
        scheduler.pause_job(mes['job_id'])
    def resume_job(self,mes):#恢复作业
        scheduler.resume_job(mes['job_id'])
    def update_job(self,mes):#更新作业
        #更改触发器
        ret = True
        try:
            scheduler.reschedule_job(mes['content']['job_id'], trigger='cron', second='*/5')
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
        job = scheduler.get_job(mes['job_id'])
        if job:
            ret = {"fuc":job.func_ref,"next_run_time":str(job.next_run_time),"id":job.id}
        return ret

    """end"""

    def start(self):
        scheduler.start()

    def stop(self):
        scheduler.shutdown()

    def check_local_task(self):#检查是否添加过本地任务,没有则添加，添加过则跳过
        for local_id in setting.LOCAL_TASK_LIST:
            if not self.job_db[setting.JOB_COLL].find({'_id':local_id}).count():
                if local_id  == setting.SCAN_TASK:
                    scheduler.add_job(func=scan_task, args=(),
                          trigger='interval', seconds=setting.SCAN_TASK_TIME, id=setting.SCAN_TASK)
                elif local_id  == setting.INTERFACE:
                    scheduler.add_job(func=interface_job_task, args=(),
                                      trigger='interval', seconds=setting.INTERFACE_TIME, id="excutor_process")

    def run(self):
        self.check_local_task()
        """本地任务
        # 扫描未加入工作队列的任务作为周期任务
        if 1:#本地任务只是服务器第一次的时候需要添加
            #将扫描任务就绪任务和超时任务作为本地任务
            scheduler.add_job(func=scan_task, args=(), trigger='cron',second='*/5',id='scan_task') #5秒扫描一次就绪任务
            #防止宕机以后任务重复添加的报错

        """
        scheduler.start()
def interface_job_task():#对外提供的接口
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

    try:
        mes = job.inter_socket.recv(zmq.NOBLOCK).decode('utf-8')# 接受到的请求数据，接受到是json格式的内容
    except zmq.ZMQError:
        return
    mes = json.loads(mes)
    if mes['type'] == 'task':
        ret = getattr(job, mes['command'] +'_task_list')(mes)  # 将arg整体传递给相应的操作
        response['content'] = ret
        if not ret:
            response['success'] = False
    elif mes['type'] == 'job':
        ret = getattr(job, mes['command'] + '_job')(mes)#作业操作
        if mes['command'] == 'pop':
            response['content'] = ret
            if not ret:
                response['success'] = False
        else:
            response['success'] = ret
    job.inter_socket.send(json.dumps(response).encode('utf-8'))

data_opt=''
scheduler=''
job = ''
def main():
    global data_opt,scheduler,job
    data_opt = task_opt()  # 对数据库操作的类
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    job = server_job()
    job.run()

if __name__ == '__main__':
    data_opt = task_opt()  #对数据库操作的类
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    job = server_job()
    job.run()