import pymongo


def get_client():
    client = pymongo.MongoClient('10.100.99.85')
    return client.vca


def get_entities_collection(collection="entities"):
    db = get_client()
    return db.get_collection(collection)


def get_intents_collection(collection="intents"):
    db = get_client()
    return db.get_collection(collection)


def create_data(intents, entities):
    data = {
        "rasa_nlu_data": {
            "regex_features": [],
            "entity_synonyms": [],
            "common_examples": []
        }
    }

    common_examples = []
    for intent in intents:
        for text in intent['text']:
            row = {
                "text": text,
                "intent": intent['intent'],
                "entities": []
            }
            common_examples.append(row)

    data['rasa_nlu_data']['common_examples'] = common_examples
    return data


def write_to_file(data):
    import json
    with open('../data/nlu-test.json', encoding='utf-8-sig',
              mode='w') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    intents = get_intents_collection().find()
    entities = get_entities_collection().find()
    data = create_data(intents, entities)
    write_to_file(data)
