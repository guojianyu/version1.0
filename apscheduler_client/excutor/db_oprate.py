
import motor.motor_asyncio,asyncio
class oprate_db:
    def __init__(self):
        conn = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = conn['pasrsing_data']
        self.tb = self.db['pasrsing_tb']

    async def db_insert(self, task):  # 插入数据
       # await self.tb.insert(task,upsert =True)
        self.tb.update(
           {
               'value': task['value'],
           },
           task,
           True
       )

    async def db_find(self, topic='JM_Crawl'):  # 只返回查找的第一条数据
        return await self.tb.find_one({'topic': topic})

    async def db_delete(self, arg):  # 删除数据
        await self.tb.remove(arg)

    def run(self):
        tasks = []
        # 将同一任务分解的单个抓取任务得到的数据拼接为一个解析任务
        tasks.append(self.get_crawltask())  # 将任务分解为单个抓取任务
        tasks.append(self.create_parstask())
        f = asyncio.wait(tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f)

    async def get_crawltask(self):
        print('ggggg')
        while True:
            task = await self.tb.find_one({'topic':'JM_Crawl'}) # 从数据库查找一个抓取任务
            if task:
                print (task,'********')
                #await self.db_delete({'_id': task['_id']})#删除任务
                print ('删除任务')
            else:
                await asyncio.sleep(0.1)


    async def create_parstask(self):
        i = 0
        task = {'topic':'JM_Crawl','value':i,'ww':'gggg'}
        while True:
            if i <5:
                await asyncio.sleep(0.1)
                i += 1
                task['value'] = str(i)
                await self.db_insert(task)  # 插入数据库
                print(task, '插入数据库***********')




if __name__ == '__main__':
    a = oprate_db()
    a.run()