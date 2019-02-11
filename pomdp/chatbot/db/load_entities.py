import json

import pymongo


def get_client_collection(collection="entities"):
    client = pymongo.MongoClient('10.100.99.85')
    db = client.vca
    return db.get_collection(collection)


def load_from_file():
    with open('../data/nlu_data.json', encoding='utf-8-sig',
              mode='r') as f:
        entities_dict = dict()

        data = json.load(f)

        for example in data['rasa_nlu_data']['common_examples']:
            entities = example['entities']
            for e in entities:
                if e["entity"] in entities_dict:
                    entities_dict[e['entity']].add(e['value'])
                else:
                    set_ = set()
                    set_.add(e['value'])
                    entities_dict[e['entity']] = set_

        for e in entities_dict.keys():
            entities_dict[e] = list(entities_dict[e])

        print(entities_dict.values())
        return entities_dict


def write_to_file(entities_dict):
    entities_arr = []
    for k in entities_dict:

        entity = {
            "entity": k
        }
        values = []
        text = entities_dict[k]
        for t in text:
            values.append({
                'value': t,
                'text': [
                    t
                ]
            })
        entity['values'] = values
        entities_arr.append(entity)

    to_file = {"entities": entities_arr}
    with open('../data/entities.json', encoding='utf-8-sig',
              mode='w') as f:
        f.write(json.dumps(to_file))


def get_from_file():
    with open('../data/entities.json', encoding='utf-8-sig',
              mode='r') as f:
        return json.load(f)


def write_to_db(remove=False):
    entities_dict = get_from_file()
    entities_collection = get_client_collection()
    if remove:
        entities_collection.remove()
    entities_arr = entities_dict['entities']
    entities_collection.insert_many(entities_arr)


if __name__ == '__main__':
    # entities_dict = load_from_file()
    # print(entities_dict)
    # write_to_file(entities_dict)
    write_to_db(remove=True)
