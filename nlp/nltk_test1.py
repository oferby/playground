import os
import nltk

# from nltk.book import *
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize
from nltk import ne_chunk
from nltk.corpus import movie_reviews

# print(brown.words())
# print(os.listdir(nltk.data.find("corpora")))

lss = LancasterStemmer()

# for word in sent9:
#     print(word + ":" + lss.stem(word=word))

news = """
The projections vary substantially — with the most pessimistic forecasting a total death toll of 120,000 by June 6, and the most optimistic forecasting 103,000 deaths by that date. But the models have been inching closer to each other. Over the last several weeks, the distance between the highest and lowest estimates has halved from a gap of 36,000 deaths two weeks ago, to a gap of 17,000 deaths in the most recent update released Tuesday.
Still, says Reich, that remains a large difference. Also, he says, some of the models are gyrating fairly significantly from week to week.
"The most pessimistic model a few weeks ago was the model from Los Alamos National Laboratory," notes Reich. "Now Los Alamos is one of the most optimistic." Meanwhile the models produced by IHME and University of Texas at Austin respectively have substantially increased their projected deaths tolls — becoming among the most pessimistic.
There are a range of reasons for these changes: The scientists are getting new data; they are updating their methods as they calibrate their models against the reality to date; and lastly, Americans have stopped social distancing to the same degree as they had been in March and April — requiring models that assumed a longer stay-at-home period to adjust their forecasts upward.
But how do we make sense of these COVID-19 projections if the models can see-saw so abruptly from week-to-week? That's where Reich's "ensemble" model may be helpful. It's a strategy that forecasters use regularly to model not just disease outbreaks, but other phenomena ranging from weather to electoral outcomes.
"""

tokens = word_tokenize(news)

tags = nltk.pos_tag(tokens)

print("************   tags  **************************")
for t in tags[:10]:
    print(t)

print(ne_chunk(tags[:10]))

print("************   sent **************************")
for s in nltk.sent_tokenize(news):
    print(s)
    tks = word_tokenize(s)
    print(tks)

print(movie_reviews.categories())
