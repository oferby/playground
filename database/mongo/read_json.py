import json
from pprint import pprint

with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/data.json') as f:
    data = json.load(f)

pprint(data)