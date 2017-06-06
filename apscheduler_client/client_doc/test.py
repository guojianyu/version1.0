

from pymongo import MongoClient
import setting
conn = MongoClient('localhost', 27017 ,connect=False)
db = conn['piiewrewrwerwe']
tb = db['ggggggggg']
tb.insert({'guid':15,'status':0})
tb.find_and_modify(query={setting.ROW_GUID:15},
                              update={'$set': {setting.ROW_STATUS: setting.STATUS_FINISH}})

a = tb.find_one()
print (a)