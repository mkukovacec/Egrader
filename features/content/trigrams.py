import resources as res
import numpy as np
import nltk

class Feature(object):

    dataset = None

    def __init__(self, dataset):
        self.dataset = dataset

    def run(self):

        array = []

        for text in self.dataset:
            trigrams = 0
            counter = 0
            words = nltk.word_tokenize(text)

            if len(words) < 3:
                array.append(0.0)
                continue

            for i in range(0, len(words) - 2):
                counter+=1
                if words[i].lower() in res.__trigrams__ and words[i + 1].lower() in res.__trigrams__[words[i].lower()] and words[i + 2].lower() in res.__trigrams__[words[i].lower()][words[i+1].lower()]:
                    trigrams += 1

            if counter == 0:
                array.append(0.0)
            else:
                array.append(float(trigrams/counter))

        return np.matrix(array)
