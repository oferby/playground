import json
from pprint import pprint

with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/data.txt') as f:
    data = json.load(f)

pprint(data)