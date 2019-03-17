from elasticsearch import Elasticsearch

es = Elasticsearch([
    {'host': '10.100.99.85'}
])

print(es.info())


def get_paragraphs():

    paragraphs = []

    with open('/home/stack/PycharmProjects/playground/pomdp/chatbot/db/qanda.txt') as f:
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
                    i+=1
                p = {'text': ''}
                continue
            else:
                p['text'] = p['text'] + ' ' + line.rstrip()

        return paragraphs

paragraphs = get_paragraphs()
assert paragraphs is not None

i = 1
for p in paragraphs:
    es.index(index='qa', doc_type='question', id=i, body=p)
    i+=1

