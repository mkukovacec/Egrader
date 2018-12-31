import numpy as np
import nltk
from nltk.corpus import wordnet

class Ruler(object):

    title = None
    text = None

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def run(self):

        counter = 0
        valid = 0
        for word in nltk.word_tokenize(self.text):
            if (len(word) < 2 and not word[0].isalpha()) or word.startswith('$'):
                continue

            counter+=1
            if (wordnet.synsets(word.lower())):
                valid+=1
        return float(valid/counter)
