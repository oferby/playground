import pymongo
from pymongo import ReturnDocument
from bson.objectid import ObjectId
import numpy as np


def get_client_collection(collection="conversations"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.rasa
    return db.get_collection(collection)


if __name__ == '__main__':

    user_inputs = []

    collection = get_client_collection()
    conversations = collection.find()
    for conversation in conversations:
        for e in conversation['events']:
            if e['event'] == 'user':
                user_inputs.append(e['text'])

    for i in sorted(set(user_inputs)):
        print(i)
