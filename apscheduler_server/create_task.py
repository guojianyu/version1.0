
from pymongo import MongoClient
import time,uuid
import setting
class jd_task_kind:

    def __init__(self):
        conn = MongoClient('localhost', 27017, connect=False)
        self.db = conn[setting.DATABASES]

    @classmethod
    def updateDict(cls, args):
        basic_task = {'device': {'type': '', 'version': '127.22', 'id': ''},
                      'guid': args['guid'],
                      'time': args['time'],  # time.time(),
                      'timeout': 1200,
                      'topic': 'jd_task_kind',
                      'interval': 86400,  # 任务执行周期间隔时间
                      'suspend': 0,  # 暂停标识
                      'status': 0,
                      'body': {
                          'kind': args['body']['kind'], 'platform': args['body']['platform'],
                          'sort': args['body']['sort'],
                      }
                      }
        return basic_task

    @classmethod
    def generateTask(cls):
        tasks = []
        kinds = []
        allKindId = {"portablePower": "9987,830,13658", "dataLine": "9987,830,13661", "phoneCase": "9987,830,866",
                     "flatAccessories": "670,671,5146", "padPasting": "9987,830,867", "mobilePhone": "9987,653,655",
                     "carAccessories": "9987,830,864", "charger": "9987,830,13660",
                     "mobilephoneBattery": "9987,830,13657", "accessoriesOfAppleProducts": "9987,830,13659",
                     "smartBracelet": "652,12345,12347", "healthMonitoring": "652,12345,12351",
                     "mobileMemoryCard": "9987,830,1099", "mobilePhoneEarphone": "9987,830,862",
                     "creativeAccessories": "9987,830,868", "mobileAccessories": "9987,830,11302",
                     "bluetoothHeadset": "9987,830,863", "mobileBracket": "9987,830,12811",
                     "cameraAccessories": "9987,830,12809", "smartWatch": "652,12345,12348",
                     "smartGlasses": "652,12345,12349", "intelligentRobot": "652,12345,12806",
                     "motionTracker": "652,12345,12350", "intelligentAccessories": "652,12345,12352",
                     "smartHome": "652,12345,12353", "inmotion": "652,12345,12354",
                     "unmannedAerialVehicle": "652,12345,12807",
                     "otherEquipmentOfIntelligentDevice": "652,12345,12355"}
        for index, item in enumerate(allKindId):
            kinds.append(allKindId[item])
        basic_task = {'device': {'type': '', 'version': '127.22', 'id': ''},
                      'guid': '',
                      'time': '',  # time.time(),
                      'timeout': 1200,
                      'topic': 'jd_task_kind',
                      'interval': 86400,  # 任务执行周期间隔时间
                      'suspend': 0,  # 暂停标识
                      'status': 0,
                      'body': {
                          'kind': '', 'platform': '', 'sort': '',
                      }
                      }
        sortlist = ['sort_totalsales15_desc', 'sort_rank_asc', 1, None]  # pc/mobile
        #   platformlist = ['jd_app','jd_web']
        for i in range(len(kinds)):
            for index2, item2 in enumerate(sortlist):
                guid = str(uuid.uuid1())  # 根据时间戳生成随机的uuid
                if item2 == 'sort_totalsales15_desc':
                    dictUpdate = {'guid': guid, 'time': time.time(),
                                  'body': {'kind': kinds[i], 'platform': 'jd_web', 'sort': item2}}
                    basic_task = cls.updateDict(dictUpdate)
                    tasks.append(basic_task)
                elif item2 == 'sort_rank_asc' and (
                            kinds[i] == '9987,830,867' or kinds[i] == '9987,830,866' or kinds[i] == '9987,653,655'):
                    dictUpdate = {'guid': guid, 'time': time.time(),
                                  'body': {'kind': kinds[i], 'platform': 'jd_web', 'sort': item2}}
                    basic_task = cls.updateDict(dictUpdate)
                    tasks.append(basic_task)
                elif item2 == 1:
                    dictUpdate = {'guid': guid, 'time': time.time(),
                                  'body': {'kind': kinds[i], 'platform': 'jd_app', 'sort': item2}}
                    basic_task = cls.updateDict(dictUpdate)
                    tasks.append(basic_task)
                elif item2 is None:
                    dictUpdate = {'guid': guid, 'time': time.time(),
                                  'body': {'kind': kinds[i], 'platform': 'jd_app', 'sort': item2}}
                    basic_task = cls.updateDict(dictUpdate)
                    tasks.append(basic_task)
        return tasks

    def insert_db(self):
        task_list = self.generateTask()
        for task in task_list:

            self.db[setting.TASKS_LIST].insert(
               task
            )
if __name__ =='__main__':
    obj = jd_task_kind()
    obj.insert_db()
