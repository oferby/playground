import nltk.stem
import nltk.tokenize
import numpy as np


def tokenize(paragraphs):
    """
    Extracts all words from sentences (ignoring stopwords), stems words, returns as sorted list with no duplicates
    :param paragraphs: paragraphs and question as strings
    :return: words: sorted list of all words in sentences
    """
    ps = nltk.stem.PorterStemmer()
    words = []
    for paragraph in paragraphs:    # gather all words
        w = nltk.word_tokenize(paragraph)
        words.extend(w)
    # stem; remove duplicates, stopwords, and punctuation
    if words:
        vocab = [ps.stem(w.lower()) for w in words if w not in nltk.corpus.stopwords.words('english') and w.isalpha()]
    else:
        raise Exception('Nothing to tokenize')
    return set(vocab)


def generate(paragraphs, questions):
    """
    generates overall vocabulary and builds bag of words vectors for each paragraph and the question
    :param paragraphs: strings
    :param questions: strings
    :return: matrix of word count vectors (one per sentence), answer is last column
    """
    ps = nltk.stem.PorterStemmer()
    paragraphs.extend(questions)
    vocab = tokenize(paragraphs)
    mat = np.zeros([len(vocab), len(paragraphs)], dtype=int)
    # build vectors for each paragraph
    for index, paragraph in enumerate(paragraphs):
        words = nltk.word_tokenize(paragraph)
        bag_vector = np.zeros(len(vocab), dtype=int)
        # for each word in the paragraph, increment vector element if word appears in vocab
        for w in words:
            for i, word in enumerate(vocab):
                if word == ps.stem(w):  # compare stem to stem
                    bag_vector[i] += 1
        mat[:, index] = bag_vector  # pack into matrix
    return mat


def find_paragraph(mat):
    """
    finds paragraph with highest number of words also found in the question
    :param mat: matrix of bag of words vectors
    :return: index of paragraph with highest inner product (ie highest num of matching words)
    """
    # separate out question from paragraphs
    q_vector = mat[:, -1]
    mat = mat[:, :-1]
    # compute inner product between paragraphs and question with matrix multiplication
    return np.argmax(mat.transpose().dot(q_vector))
