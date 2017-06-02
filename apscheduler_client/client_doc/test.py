from pymongo import MongoClient
conn = MongoClient('localhost', 27017, connect=False)
db = conn['test']
tb = db['gg']

data = tb.find()

print (data.count())
tb.remove()
for i in data:

    print (i)