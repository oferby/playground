import pymongo


def get_client_collection(collection="info"):
    client = pymongo.MongoClient()
    db = client.vca
    return db.get_collection(collection)


def find_all_from_info(type, topic):
    collection = get_client_collection()
    results = collection.find({"type": type, "topic": topic})
    result = []
    for r in results:
        result.append(r)
    return result


def load_to_db():
    import json

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/data.txt') as f:
        data = json.load(f)
        collection = get_client_collection("info")
        collection.remove({})
        result = collection.insert_many(data['q'])
        print(result.inserted_ids)


if __name__ == '__main__':
    load_to_db()
    r = find_all_from_info("what-is", "rds")
    print(r)
