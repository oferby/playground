from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import xml.etree.ElementTree as ET
import nltk

tree = ET.parse("../../data/blog.xml")

# get root element
root = tree.getroot()

# iterate post items
posts = []
for post in root.findall('post'):
    posts.append(post.text.lower().replace('\n', ' '))

sentences = []
for p in posts:
    tkn = nltk.sent_tokenize(p)
    for t in tkn:
        s = t.strip()
        sentences.append(s)
        print(s)

tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
print(word_index)
