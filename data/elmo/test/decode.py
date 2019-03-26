import json


def unpack(filename):
    """
    unpacks dev-v2 json file and loads data into lists
    :param filename:
    :return: list of paragraphs, list of questions
    """
    #
    with open(filename) as jfile:
        dataset = json.load(jfile)
        context = []
        qas = []
        for article in dataset['data']:   # for each article
            for paragraph in article['paragraphs']:          # for each paragraph in given article
                context.append(paragraph['context'])
                qas.append(paragraph['qas'])
        # separate each question from block of questions
        q_list = []
        for qa in qas:  # for each block
            for q in qa:    # for each question
                q_list.append(q['question'])

    return context, q_list
