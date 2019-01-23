import numpy as np
import nltk
from nltk.corpus import wordnet
import resources as res

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
            if not word[0].isalpha():
                continue

            counter+=1
            if (wordnet.synsets(word.lower()) or word.lower() in res.__words__ or word.lower() in res.__names__):
                valid+=1
        return float(valid/counter)
