"""数据库与数据表，服务器的数据存储共用一库"""
DATABASES = 'jame_server'  #数据库

TASKS_LIST = 'task_main'  #总任务列表

RECODE_LIST = "recode_list"  #记录超时任务的id和该任务上次分配的设备id，任务重新分配以后提醒客户端删除该任务

CLIENT_CPU_DATA = 'cpu_data'#存储客户端的硬件信息数据表{'time':time,'system_info':sys_info,'device_id':device_id}

RECODE_ERROR_LIST = 'error_task'#记录任务的超时次数大于任务默认的最大超时次数的表


TMP_DB = 'tmp_db'
TMP_TB = 'tmp_tb'

JOB_DB = 'aps_all_copy'#aps储存作业的数据库名称
JOB_COLL = 'server_job'#aps储存作业的集合



#属性状态码含义
STATUS_DELAY = 0  # 任务处于等待状态
STATUS_READY = 1  # 任务处于就绪状态，可以执行
STATUS_EXCUTING = 2  # 任务正在执行
STATUS_TIMEOUT = 3  # 任务超时
STATUS_DELETED = 4  # 任务处于删除状态，不再被扫描
STATUS_FINISH = 5  # 任务完成，控制权交回队列




DOWN_LOGO = {'down':["jd_task_kind",'sku1'],'notdown':['sku2',]}

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

SERVER_PORT = '8989'

