from allennlp.predictors.predictor import Predictor
import numpy as np
import math
import scipy.stats as sts

predictor = Predictor.from_path(
    # "https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz"
    "../../pomdp/chatbot/data/bidaf-model-2017.09.15-charpad.tar.gz"
)

with open('../data/qanda.txt', 'r') as f:
    context = f.read()

query = 'how many vehicles were in the convoy?'


p = predictor.predict(
    passage=context,
    question=query
)

print(p)
print('\n\n\nanswer: {}'.format(p['best_span_str']))

