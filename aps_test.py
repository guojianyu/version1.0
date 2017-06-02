import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
host = '127.0.0.1'
port = 27017
client = MongoClient(host, port,connect=False)

jobstores = {
    #'mongo': MongoDBJobStore(collection='job', database='aps_all_copy', client=client),
    'default': MongoDBJobStore(collection='job2222', database='aps_all_copy', client=client),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def aps_test(x,task):#
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
tm = datetime.datetime.now()
print (tm)
scheduler.add_job(func=aps_test, args=('定时任务',),
                          trigger='interval', seconds=1, id='ddd')
#scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron',start_date= tm,second='1',id='cron_task')#每分2秒的时候会执行，定时任务