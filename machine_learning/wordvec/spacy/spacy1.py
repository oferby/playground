import spacy
from scipy import spatial
f = open("../data.text", "r")

nlp = spacy.load('en')
doc = nlp(f.read())

# for token in doc:
#     print(token.text, token.idx)
#
#
print('#### sentences ####')
for s in doc.sents:
    print(s)

print('### NER ###')
for e in doc.ents:
    print(e.text, e.label_)


aws = nlp.vocab['AWS'].vector
huawei = nlp.vocab['Huawei'].vector
cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)
print(cosine_similarity(aws, huawei))

print('vm-server: ', cosine_similarity(nlp.vocab['vm'].vector,nlp.vocab['server'].vector))
print('vocab len:', len(aws))

text = 'I need virtual machine with ubuntu os'
doc = nlp(text)
for e in doc.ents:
    print(e.text, e.label_)
