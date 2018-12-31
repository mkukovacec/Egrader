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
            appeared = {}
            for word in nltk.word_tokenize(text):
                if (not wordnet.synsets(word.lower()) or len(word)<2 and not word[0].isalpha()) or word.startswith('$'):
                    continue

                counter+=1
                appeared[word] = ''

            if counter == 0:
                array.append(0.0)
            else:
                array.append(float(len(word)/counter))

        return np.matrix(array)
