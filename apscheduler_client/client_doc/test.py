

from pymongo import MongoClient
import setting
conn = MongoClient('localhost', 27017 ,connect=False)
db = conn['piiewrewrwerwe']
tb = db['ggggggggg']

#tb.remove()
task = {'guid':15,'status':0}

tb.insert({'guid':16,'status':0})



#{'updatedExisting': False, 'n': 1, 'upserted': ObjectId('593a25eb7412daf383b3244b'), 'ok': 1.0, 'nModified': 0}
#{'nModified': 1, 'ok': 1.0, 'updatedExisting': True, 'n': 1}