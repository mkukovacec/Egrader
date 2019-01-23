import numpy as np
import nltk
import math
import gensim
import resources as res

class Ruler(object):

    title = None
    text = None
    model = None
    seen_words = {}

    def __init__(self, title, text):
        self.title = [tit.lower() for tit in title.split(' ')]
        self.text = text
        #self.model = gensim.models.KeyedVectors.load_word2vec_format('resources/model.bin', binary=True)
        self.model = gensim.models.Word2Vec.load('resources/w2v.model')

    def run(self):
        counter = 0
        similar = 0

        def put_word(seen_words, word):
            if word not in seen_words:
                seen_words[word] = 0.0
            seen_words[word] += 1.0

        for word in nltk.word_tokenize(self.text):
            if not word[0].isalpha() or word in res.__words__ :
                continue

            counter+=1
            try:
                put_word(self.seen_words, word.lower())
                similarity = np.max(self.model.similarity(self.title, word.lower()))
                if similarity > 0.2:
                    similar += math.sqrt(float(1.0/self.seen_words[word.lower()]))

            except KeyError as e:
                print ("Error for word: {0}".format(word))
                continue

        if (float(similar/counter) > 0.5):
            return 1.0

        return math.sqrt(math.sqrt(float(similar/counter)))
