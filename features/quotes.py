import numpy as np
import nltk
from nltk.corpus import wordnet

class Feature(object):

    dataset = None

    def __init__(self, dataset):
        self.dataset = dataset

    def run(self):

        array = []

        for text in self.dataset:
            counter = 0
            sentence_count = 0
            for sentence in nltk.tokenize.sent_tokenize(text):
                if sentence.startswith('"') and sentence.endswith('"') or sentence.startswith("'") and sentence.endswith("'"):
                    sentence_count += 1

                counter += 1

            array.append(float(sentence_count/counter))

        return np.matrix(array)
