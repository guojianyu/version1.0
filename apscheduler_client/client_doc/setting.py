#总任务链表数据库相关
DATABASES = 'jame_bd'  #数据库
TASKS_LIST = 'task_main'  #总任务列表
TOPIC = ['kind','jd_task_kind','hello1']#任务类型
COMPLETE = "complete" #存储自上次更新任务后的完成任务数总数的表 , {'topic': 类型，'count':个数}

#作业存储数据库相关
JOB_COLL = 'job'#aps储存作业的集合
JOB_DB = 'aps_all_copy'#aps储存作业的数据库名称

#数据存储的数据库相关
DATA_DB = 'data_db'
DATA_TB = 'data_tb'


"""任务属相关"""
ROW_GUID = 'guid'
ROW_TOPIC = 'topic'
ROW_TIME = 'time'
ROW_TIMEOUT = 'timeout'
ROW_BODY = 'body'
ROW_STATUS = 'status'
DEVICE_TYPE = 'pc' #设备类型
DEVICE_ID = 'jame001'  #设备id

#属性状态码含义
STATUS_DELAY = 0  # 任务处于等待状态
STATUS_READY = 1  # 任务处于就绪状态，可以执行
STATUS_EXCUTING = 2  # 任务正在执行
STATUS_TIMEOUT = 3  # 任务超时
STATUS_DELETED = 4  # 任务处于删除状态，不再被扫描
STATUS_FINISH = 5  # 任务完成，控制权交回队列

#0等待，1：进入就绪队列，2：执行中，3：超时，4：删除 5：完成

"""客户端启动对作业的处理方式"""
CLEAR = 'clear'#客户端启动将作业列表清空然后只添加本地作业
CHECK= 'update'#保留所有的作业，检查本地作业，本地作业没有则添加，有则跳过。
PULSE_ON_TYPE =CLEAR

"""本地任务生成作业的id"""
#特殊的本地任务
SCAN_TASK = "scan_task"


#############################################################################################################
UPDATE_TASK_LIST = "update_task_list"
UPDATE_MUCH_TASKINFO = "update_much_taskinfo"
UPLOAD_CLIENT_STATUS = "upload_client_status"
UPLOAD_CLIENT_DATA =  "upload_client_data"
UPDATE_PROXY_DATA = "update_proxy_data"
UPDATE_COOKIE_DATA = "update_cookie_data"
#这个列表关联的是与服务器进行交互的任务类型
LOCAL_TASK_LIST = (UPDATE_TASK_LIST,UPDATE_MUCH_TASKINFO,UPLOAD_CLIENT_STATUS,
                   UPLOAD_CLIENT_DATA,UPDATE_PROXY_DATA,UPDATE_COOKIE_DATA)
#############################################################################################################



"""本地任务时间的设定"""
SCAN_TASK_TIME = 1 #扫描总任务队列的时间
UPDATE_TASK_LIST_TIME = 5# 更新任务列表的时间单位是秒
UPDATE_MUCH_TASKINFO_TIME = 600 #客户端回报任务信息的时间,这个时间不应该小于任务的超时时间
UPLOAD_CLIENT_STATUS_TIME = (3600*12) #客户端更新设备信息的时间，12h更新一次
UPLOAD_CLIENT_DATA_TIME = 8 # 客户端回报数据的时间
UPDATE_PROXY_DATA_TIME = 9 #更新proxy的时间
UPDATE_COOKIE_DATA_TIME = 10#更新coolkie 时间


"""外部端口"""
OUT_PORT = '9000'
PUSH_PORT = '5599'#客户端向中间层推任务的端口


SERVER_PORT = '8989'
