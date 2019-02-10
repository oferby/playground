import pymongo


def get_client_collection(coll="info"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(coll)


def find_all_from_info(type, topic):
    collection = get_client_collection()
    results = collection.find({"type": type, "topic": topic})
    result = []
    for r in results:
        result.append(r)
    return result


def find_one(value, coll="info"):
    collection = get_client_collection(coll)
    return collection.find_one({"intent": value})


def add_one(value, coll="info"):
    collection = get_client_collection(coll)
    collection.insert_one(value)


def remove_all(coll=None):
    if not coll is None:
        collection = get_client_collection(coll)
        collection.remove({})


def load_to_db():
    import json

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/data.txt') as f:
        data = json.load(f)
        collection = get_client_collection("info")
        collection.remove({})
        result = collection.insert_many(data['q'])
        print(result.inserted_ids)


intents = [
    {"intent": 'confirm',
     "examples": [
         "yes", "sure", "good"
     ]
     },
    {"intent": 'deny',
     "examples": [
         "no", "nop", "never"
     ]
     }
]

if __name__ == '__main__':
    coll = "intents"
    remove_all(coll)
    for intent in intents:
        add_one(intent, coll)
    r = find_one("confirm", coll)
    print(r)
    # remove_all(coll)
