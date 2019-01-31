import pymongo


def get_client_collection(collection="qanda"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(collection)


def load_to_db():
    import json

    paragraphs = []

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/qanda.txt') as f:
        collection = get_client_collection()
        collection.remove({})

        p = None
        while True:
            line = f.readline()
            if not line:
                break
            if line == '\n':
                continue
            elif line.startswith('*'):
                if p is not None:
                    paragraphs.append(p)
                p = {'text': ''}
                continue
            else:
                p['text'] = p['text'] + line

        print(paragraphs)

        data = {
            'paragraphs': paragraphs
        }

        collection.insert_one(data)


if __name__ == '__main__':
    load_to_db()
    # r = find_one_from_info("what_is", "waf")
    # print(r)
