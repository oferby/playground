from allennlp.predictors.predictor import Predictor
import numpy as np
import math
import scipy.stats as sts

predictor = Predictor.from_path(
    # "https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz"
    "../../pomdp/chatbot/data/bidaf-model-2017.09.15-charpad.tar.gz"
)


# context_1 = 'ECSs integrate Virtual Private Cloud (VPC), virtual firewalls, and multi-data-copy capabilities to create an efficient, reliable, and secure computing environment. This ensures stable and uninterrupted operation of services.'
context_1 = 'Application Operations Management (AOM) helps you detect faults timely and master the real-time running statuses of applications, resources, and services.'

# context_2 = 'A stack is a collection of applications and cloud service resources. The applications and cloud services in a stack are treated as a whole when they are being created, upgraded, or deleted.'
# context_2 = 'Using templates to describe and orchestrate applications and related cloud services, Application Orchestration Service (AOS) facilitates automatic application deployment, cloud service creation, and E2E application lifecycle management.'
context_2 = 'An Elastic Cloud Server (ECS) is a computing server consisting of vCPUs, memory, image, and Elastic Volume Service (EVS) disks that allow on-demand allocation and elastic scaling.'

query = 'what is aom?'

p1 = predictor.predict(
    passage=context_1,
    question=query
)

p2 = predictor.predict(
    passage=context_2,
    question=query
)

len(p1['span_start_logits'])

p1_max = np.argmax(p1['span_start_probs'])
p2_max = np.argmax(p2['span_start_probs'])

p1_str = p1['span_start_probs']
p1_end = p1['span_end_probs']
p2_str = p2['span_start_probs']
p2_end = p2['span_end_probs']

print('******   p1_max > p2_max:', max(p1_str) > max(p2_str))
print('******   p1 > p2:', (max(p1_str) * max(p1_end)) > (max(p2_str) * max(p2_end)))
print('******   p1_max_logits > p2_max_logits:', p1['span_start_logits'][p1_max] > p2['span_start_logits'][p2_max])


def get_loss(p1, p2):
    p1_log = [math.log(x) for x in p1]
    p2_log = [math.log(x) for x in p2]
    p12 = [a + b for a, b in zip(p1_log, p2_log)]
    return - sum(p12) / len(p1)


loss_1 = get_loss(p1_str, p1_end)
loss_2 = get_loss(p2_str, p2_end)

print('loss 1:', loss_1, 'loss 2:', loss_2)

print('entropy p1 start:', sts.entropy(p1_str))
print('entropy p1 end:', sts.entropy(p1_end))

print('entropy p2 start:', sts.entropy(p2_str))
print('entropy p2 end:', sts.entropy(p2_end))

print('entropy P1: ', (sts.entropy(p1_str) + sts.entropy(p1_end))/2)
print('entropy P2: ', (sts.entropy(p2_str) + sts.entropy(p2_end))/2)

print('answer 1:', p1['best_span_str'])
print('answer 2:', p2['best_span_str'])


# print('**************** ', p['best_span_str'], ' **************')
# print('keys:', p.keys())
# print('span_start_logits:', len(p['span_start_logits']))
#
# print('passage_tokens:', len(p['passage_tokens']))
#
# print('\n\nall:', p, '\n\n')
