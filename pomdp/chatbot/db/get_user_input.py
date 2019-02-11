import pymongo


def get_client():
    return pymongo.MongoClient('10.100.99.85')


def get_conversation_collection(collection="conversations"):
    client = get_client()
    db = client.rasa
    return db.get_collection(collection)


def get_intents_collection(collection="intents"):
    client = get_client()
    db = client.vca
    return db.get_collection(collection)


def get_intents():
    intents_collection = get_intents_collection()
    intents = intents_collection.find()
    intents_dict = {}
    intent_text = set()
    for intent in intents:
        intents_dict[intent['intent']] = intent['text']
        for text in intent['text']:
            intent_text.add(text)

    return intents_dict, intent_text


if __name__ == '__main__':

    user_inputs = []

    collection = get_conversation_collection()
    conversations = collection.find()
    for conversation in conversations:
        for e in conversation['events']:
            if e['event'] == 'user':
                user_inputs.append(e['text'])
    user_inputs = sorted(set(user_inputs))

    intents_dict, intent_text = get_intents()
    # print('text', intent_text)

    for i in user_inputs:
        i = i.lower()
        if i not in intent_text and not i.startswith('*') and not i.startswith(':'):
            print(i)
