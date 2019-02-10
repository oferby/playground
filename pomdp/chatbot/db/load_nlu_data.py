import pymongo
from pymongo import ReturnDocument
from bson.objectid import ObjectId
import numpy as np


def get_client_collection(collection="intents"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(collection)


def load_to_db():
    import json

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/data/nlu_data.json', encoding='utf-8-sig',
              mode='r') as f:
        intents_dict = dict()

        data = json.load(f)

        for example in data['rasa_nlu_data']['common_examples']:
            intent = example['intent']
            text = example['text']
            if intent in intents_dict.keys():
                intents_dict[intent]['text'].append(text)
            else:
                rec = {
                    'intent': intent,
                    'text': [text]
                }
                intents_dict[intent] = rec

        print(intents_dict.values())

        intents_arr = []
        for v in intents_dict.values():
            intents_arr.append(v)
        to_file = {"intents": intents_arr}
        with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/data/intents.json', encoding='utf-8-sig', mode='w') as f:
            f.write(json.dumps(to_file))


if __name__ == '__main__':
    # pass
    load_to_db()

    # update_one()
