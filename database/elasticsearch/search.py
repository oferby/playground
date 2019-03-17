from elasticsearch import Elasticsearch

es = Elasticsearch([
    {'host': '10.100.99.85'}
])

print(es.info())

doc = es.get(index='qa', doc_type='question', id=1)
print('search by id:',doc)


body = {
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "text": "new text"
          }
        },
        {
          "match": {
            "question": "second"
          }
        }
      ]
    }
  }
}

docs = es.search(index='qa', doc_type='question', body=body)
print(docs)
