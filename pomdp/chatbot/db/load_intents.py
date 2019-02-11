import json

import pymongo


def get_client_collection(collection="intents"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(collection)


def load_to_db():
    with open('../data/nlu_data.json', encoding='utf-8-sig',
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
        return intents_dict


def write_to_file(intents_dict):
    intents_arr = []
    for v in intents_dict.values():
        intents_arr.append(v)
    to_file = {"intents": intents_arr}
    with open('../data/intents.json', encoding='utf-8-sig',
              mode='w') as f:
        f.write(json.dumps(to_file))


def read_from_file():
    with open('../data/intents.json', encoding='utf-8-sig',
              mode='r') as f:
        return json.load(f)


def write_to_db(intents_dict, remove=False):
    intents_collection = get_client_collection()
    if remove:
        intents_collection.remove()
    intents_collection.insert_many(intents_dict['intents'])


if __name__ == '__main__':
    # intents_dict = load_to_db()
    # write_to_file(intents_dict)

    intents_dict = read_from_file()
    write_to_db(intents_dict, remove=True)
    intents = get_client_collection().find()
    for intent in intents:
        print(intent)
