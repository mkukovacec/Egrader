import numpy as np
import nltk

class Feature(object):

    dataset = None

    def __init__(self, dataset):
        self.dataset = dataset

    def run(self):

        array = []
        #TODO implement
        for text in self.dataset:

            array.append(0.0)

        return np.matrix(array)
