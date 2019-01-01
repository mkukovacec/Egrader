import features.content.resources as res
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
            uncommon = 0
            for sentence in nltk.tokenize.sent_tokenize(text):
                if sentence.startswith('"') and sentence.endswith('"'):
                    continue
                for word in nltk.word_tokenize(sentence):
                    if not wordnet.synsets(word.lower()) or not word[0].isalpha():
                        continue

                    counter+=1

                    if (word.lower() not in res.__words__):
                        uncommon+=1
            if counter == 0:
                array.append(0.0)
            else:
                array.append(float(uncommon/counter))

        return np.matrix(array)
