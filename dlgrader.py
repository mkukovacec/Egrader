from gensim.models import KeyedVectors
from keras.models import load_model
import tensorflow as tf
import numpy as np
import nltk
import re
import resources as res
from gensim.models import Word2Vec

class DLGrader:
    def __init__(self, path_to_word2vec, path_to_keras_model):
        print('Loading W2V')
        self.embeddings_index = self.load_w2v(path_to_word2vec)
        print('Loading Keras Model')
        self.model = self.load_keras_model(path_to_keras_model)
        self.graph = tf.get_default_graph()

    def load_w2v(self, path_to_word2vec):
        embeddings_index = {}
        wv_from_bin = KeyedVectors.load_word2vec_format(path_to_word2vec, binary=True)
        for word, vector in zip(wv_from_bin.vocab, wv_from_bin.vectors):
            coefs = np.asarray(vector, dtype='float32')
            embeddings_index[word] = coefs
        return embeddings_index

    def load_keras_model(self, path_to_keras_model):
        return load_model(path_to_keras_model)

    def essay_to_wordlist(self, essay_v, remove_stopwords):
        essay_v = re.sub("[^a-zA-Z]", " ", essay_v)
        words = essay_v.lower().split()
        if remove_stopwords:
            words = [w for w in words if not w in res.__stop_words__]
        return (words)

    def essay_to_sentences(self, essay_v, remove_stopwords):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        raw_sentences = tokenizer.tokenize(essay_v.strip())

        sentences = []
        for raw_sentence in raw_sentences:

            if len(raw_sentence) > 0:
                sentences += (self.essay_to_wordlist(raw_sentence, remove_stopwords))
        return sentences

    def process(self, text):
        x = self.essay_to_sentences(text, remove_stopwords = True)
        x_n = []
        for w in x:
            try:
                x_n.append(self.embeddings_index[w])
            except KeyError:
                pass
        a = np.array(x_n)
        return a.reshape((1, a.shape[0], a.shape[1]))

    def grade(self, text):
        if len(text) == 0 or text.isspace():
            return 0.0

        text_x = self.process(text)
        result = 0.0
        with self.graph.as_default():
            result = round(abs(self.model.predict(text_x)[0][0]) * 100)
        return result
