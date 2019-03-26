"""
finds the paragraph most likely to contain the answer to the first question in the set, based on word overlap
creates a bag of words vocabulary for the set; words are stemmed, punctuation and stopwords are removed
for each paragraph (also the question), creates a bag of words vector, indicating which vocab words are
present in the paragraph
uses inner product to compare how many words from the question appear in the paragraph
prints paragraph with highest overlap
"""
import decode
import sys
import bag_of_words as bow


MAX_PARAGRAPHS = 100

if __name__ == '__main__':
    # if len(sys.argv) != 2 or sys.argv[1] != 'dev-v2.0.json':
    #     raise Exception('Usage: driver dev-v2.0.json')

    # create lists of paragraphs and questions
    context, q_list = decode.unpack('../../dev-v2.0.json')
    # retrieve index of most like paragraph
    index = bow.find_paragraph(bow.generate(context[0:MAX_PARAGRAPHS], q_list[0]))
    print('The answer most likely can be found in the following paragraph', context[index], sep="\n")

