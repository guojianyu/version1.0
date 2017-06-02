



EXCUTOR_PORT = "6666"#执行器向中间层申请任务的端口


LOCAL_TASK_PORT = '7777'#向中间层添加本地任务的端口

CENTER_INTERFACE_PORT = 9995#通过中间层对客户端总任务列表和作业修改端口


TOPIC = ['kind','hello','hello1']#任务类型


"""扫描任务进程个数"""

SUM_PROCESS_COUNT = 8#默认开启的总进程数
PUT_PROCESS_COUNT = 1#添加任务队列的进程个数，此参数暂时不可用
############################################################
#负责调用脚本的进程数 = SUM_PROCESS_COUNT- PUT_PROCESS_COUNT
#负责调用脚本的线程数 = （SUM_PROCESS_COUNT-SUM_PROCESS_COUNT）*GET_THREADING_COUNT
#与中间层通信的PUT_PROCESS，使用进程进行添加任务队列，可以得到更多的时间片，建议开启的进程数小等于2，
#因为负责调用脚本的进程相对于添加任务队列的进程耗时要久，应该尽量的将资源分配给调用脚本的进程。
############################################################

GET_THREADING_COUNT = 100#获取任务的线程个数，线程数合理设定，
#######################################################
#GET_THREADING_COUNT是负责调用脚本的进程开启的线程个数
#默认开启800个线程
########################################################

"""抓取的任务类型"""

GET_COUNT = 1 #一次从中间层获取的任务个数,该个数应该合理决定


"""脚本存放目录相关"""
#目录必须要与
SCRIPT_DIR = 'script_doc'#脚本所在的总目录名称

#考虑到脚本的数量问题，将脚本进行分类存储

#脚本归类目录可以通过配置文件设置，也可以在任务属性中增加字段
TYPE01_DIR = 'yyyy'#脚本的归类目录