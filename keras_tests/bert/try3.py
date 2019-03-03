import os
import json
from keras_bert.loader import load_trained_model_from_checkpoint
from keras_bert.bert import *

BERT_PRETRAINED_DIR = 'uncased_L-12_H-768_A-12'

config_file = os.path.join(BERT_PRETRAINED_DIR, 'bert_config.json')
checkpoint_file = os.path.join(BERT_PRETRAINED_DIR, 'bert_model.ckpt')
model = load_trained_model_from_checkpoint(config_file, checkpoint_file, training=True)

model.summary(line_length=120)

