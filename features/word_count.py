import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer

class Feature(object):

    dataset = None

    def __init__(self, dataset):
        self.dataset = dataset

    def run(self):

        array = []
        tokenizer = RegexpTokenizer(r'\w+')

        for text in self.dataset:
            array.append(len(tokenizer.tokenize(text)))

        divisor = max(max(array), 1)
        counts = [float(count/divisor) for count in array]

        return np.matrix(counts)
