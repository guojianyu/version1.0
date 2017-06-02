"""数据库与数据表，服务器的数据存储共用一库"""
DATABASES = 'jame_server'  #数据库

TASKS_LIST = 'task_main'  #总任务列表

RECODE_LIST = "recode_list"  #记录超时任务的id和该任务上次分配的设备id，任务重新分配以后提醒客户端删除该任务

CLIENT_CPU_DATA = 'cpu_data'#存储客户端的硬件信息数据表{'time':time,'system_info':sys_info,'device_id':device_id}

JOB_COLL = 'server_job'#aps储存作业的集合

JOB_DB = 'aps_all_copy'#aps储存作业的数据库名称



TASK_STATUS  = {'WAIT':0,'READY':1,'EXCUTE':2,'TIMEOUT':3,'DELETE':4,'FINISH':5}#0等待，1：进入就绪队列，2：执行中，3：超时，4：删除 5：完成

DOWN_LOGO = {'down':["kind",'sku1'],'notdown':['sku2',]}

DOWN_COUNT = {'down':100,'notdown':200}



"""本地任务id"""
SCAN_TASK = "scan_task"
SCAN_TASK_TIME = 1 #扫描总任务队列的间隔时间
INTERFACE = 'excutor_process'
INTERFACE_TIME = 0.1#对外zmq交互的间隔时间

#本地任务作业id
LOCAL_TASK_LIST = [SCAN_TASK,INTERFACE]

"""任务属相关"""
ROW_GUID = 'guid'
ROW_TOPIC = 'topic'
ROW_TIME = 'time'
ROW_TIMEOUT = 'timeout'
ROW_BODY = 'Body'
ROW_STATUS = 'status'


"""外部端口"""
OUT_PORT = '9002'



