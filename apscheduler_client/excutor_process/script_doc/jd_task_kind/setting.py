"""端口配置"""
EXCUTOR_PORT = "6666"#执行器向中间层申请任务的端口

CENTER_PORT = '5599'#调度中心向中间层添加任务的端口

LOCAL_TASK_PORT = '7777'#向中间层添加本地任务的端口


CENTER_INTERFACE_PORT = 9995#通过中间层对客户端总任务列表和作业修改端口

CLIENT_INTERFACE_PORT = '9000'#中间层对客户端操作的接口



"""执行器代码相关"""

TOPIC_FUNC = {'jm_crawl':'catcher_interface','parsing':'parsing_interface','send':'send_data_interface'}#抓取，解析，发送所对应的入口方法

PROCESS_COUNT={'jm_crawl':1,'parsing':1,'send':1}# 本地任务对应开启进程个数

TOPIC = ('kind','shop','product','keyword')#设置执行器解析服务器下发的任务类型

DATABASES = 'data_base'#数据存储数据库

TABLE = 'data_table'#数据存储表


"""抓取器相关"""

MaxClients = 200#抓取器异步抓取数的设置
