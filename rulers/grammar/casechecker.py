import numpy as np
import nltk
from nltk.corpus import wordnet
import resources as res

# koliko rijeci se koristi

class Ruler(object):

    title = None
    text = None

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def run(self):
        counter = 0
        valid = 0

        def all_lower(word):
            for letter in word:
                if letter.isupper():
                    return False

            return True

        def first_capital(word):
            for letter in word[1:]:
                if letter.isupper():
                    return False

            return word[0].isupper()

        for sentence in nltk.sent_tokenize(self.text):
            i = 0
            for word in nltk.word_tokenize(sentence):
                if not word[0].isalpha():
                    continue

                if i == 0 and first_capital(word):
                    valid += 1
                elif i > 0 and all_lower(word):
                    valid += 1
                elif i > 0 and word.lower() in res.__names__ and first_capital(word):
                    valid += 1

                counter+=1
                i += 1

        return float(valid/counter)
