import pymongo


client = pymongo.MongoClient()
db = client.vca
info_collection = db.info

infos = info_collection.find()

for info in infos:
    print(info)


inf = info_collection.find_one({"type":"what-is"})

print(inf)
