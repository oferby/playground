import pymongo
import tensorflow as tf
import keras
from keras.layers import Embedding


client = pymongo.MongoClient('10.100.99.85')
db = client.vca
collection = db.get_collection("qanda")

qanda = collection.find()

for q in qanda:
    if 'questions' in q:
        print(q)




