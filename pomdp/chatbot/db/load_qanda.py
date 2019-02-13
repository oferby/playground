import pymongo
from bson.objectid import ObjectId
from pymongo import ReturnDocument


def get_client_collection(collection="qanda"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(collection)


def load_to_db():
    paragraphs = []

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/qanda.txt') as f:
        collection = get_client_collection()
        collection.remove({})

        i = 0
        p = None
        while True:
            # if i > 3:
            #     break
            line = f.readline()
            if not line:
                break
            if line == '\n':
                continue
            elif line.startswith('*'):
                if p is not None:
                    p['text'] = p['text'].lstrip()
                    paragraphs.append(p)
                    i += 1
                p = {'text': ''}
                continue
            else:
                p['text'] = p['text'] + ' ' + line.rstrip()

        print(paragraphs)


def update_one():
    id = '5c52eb161ac8c015db46d591'
    collection = get_client_collection('qanda')
    qanda = collection.find_one({'_id': ObjectId(id)})
    print(qanda)

    if 'questions' in qanda:
        qanda['questions'].append('q2')
    else:
        qanda['questions'] = ['q2']

    qanda = collection.find_one_and_update({'_id': ObjectId(id)}, {"$set": qanda},
                                           upsert=False, return_document=ReturnDocument.AFTER)
    print('after', qanda)


def get_qanda():

    id_array = []
    questions = []

    collection = get_client_collection()
    qanda_col = collection.find()
    for qanda in qanda_col:
        if 'questions' in qanda:
            id_array.append(str(qanda['_id']))
            questions.append(qanda['questions'])
            print(qanda['_id'],qanda['questions'])



if __name__ == '__main__':
    get_qanda()
