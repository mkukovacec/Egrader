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
            valid = 0
            for sentence in nltk.tokenize.sent_tokenize(text):
                if sentence.startswith('"') and sentence.endswith('"'):
                    continue
                for word in nltk.word_tokenize(sentence):
                    if (word.startswith('$')):
                        continue

                    counter+=1
                    if (wordnet.synsets(word.lower())):
                        valid+=1
            array.append(float(valid/counter))

        return np.matrix(array)
