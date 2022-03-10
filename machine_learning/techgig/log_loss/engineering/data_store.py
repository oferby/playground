# https://www.techgig.com/practice/question/log-loss-multi-class-log-loss/MmRpN1d4NE1iNTVURktjdzAySS9iaXpVYkgvWk9DdnZEWVM4TWRDTkJZdml6aUJkcDhkVzA2R3Vnb3Nhdy9uTw==/1


import json

event_dict = {}

lines = []
with open('../data/_train.csv') as f:
    lines = f.readlines()


for line in lines:
    tags = line.split(",")
    # event_dict[]
    print(tags)
