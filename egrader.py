from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from util import transform, load_model, rule_score
from dlgrader import DLGrader
import numpy as np
import copy
import nltk
from nltk.corpus import wordnet
import resources as res
from math import sqrt
app = Flask(__name__)
CORS(app)

modules = {}
modules['content'] = load_model('models','content')
modules['grammar'] = load_model('models','grammar')
dlmodel = DLGrader('models/GoogleNews-vectors-negative300.bin', 'models/best_model.h5')

@app.route('/grade', methods=['POST'])
def my_form_post():
    essay_title = request.json['title']
    essay_text = request.json['text']
    content_score=predictor(essay_title, essay_text, "content")
    grammar_score=rule_out(essay_title, essay_text, "grammar")
    relevance_score=rule_out(essay_title, essay_text, "relevance")
    dl_score=grader(essay_title, essay_text)
    return jsonify(dlscore=dl_score, mlscore=content_score, grammar=grammar_score, relevance=relevance_score)

def predictor(essay_title = None, essay_text = None, module=None):
    if empty(essay_title) or empty(essay_text) or empty(module):
        return '0.0'

    result = modules[module].predict(transform(np.array([essay_text]), module))
    return "{0}".format(round(adjust_score(result[0], essay_text), 2))

def adjust_score(result, text):
    words = nltk.word_tokenize(text)
    result = adjust_score_text_length(result, words)
    result = adjust_score_unique_words(result, words)

    return result * 100.0

def adjust_score_unique_words(result, words):
    unique_words = {}
    for word in words:
        if (wordnet.synsets(word.lower()) or word.lower() in res.__words__):
            unique_words[word.lower()] = ''

    divisor = float(len(unique_words) / len(words))

    if divisor >= 0.3:
        return result

    return result * sqrt(divisor)


def adjust_score_text_length(result, words):
    text_length = len(words)
    if text_length < 100:
        divisor = 1.01 ** (100 - text_length)
        return result / divisor
    if text_length > 800:
        divisor = 1.01 ** (text_length - 800)
        return result / divisor

    if result > 1.0:
        result = 1.0 / result

    return result


def rule_out(essay_title, essay_text, module = None):
    if empty(essay_title) or empty(essay_text) or empty(module):
        return '0.0'

    result = rule_score(module, essay_title, essay_text)
    result *= 100.0
    return "{0}".format(round(result, 2))

def grader(essay_title, essay_text):
    if empty(essay_title) or empty(essay_text):
        return '0.0'

    result = dlmodel.grade(essay_text)
    return "{0}".format(result)

def empty(variable):
    if variable is None or len(variable)==0:
        return True
    return False

if __name__ == '__main__':
    app.run()
