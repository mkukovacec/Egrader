from flask import Flask, request, render_template
from util import transform, load_model, rule_score
import numpy as np
import nltk
from nltk.corpus import wordnet
import features.content.resources as res
from math import sqrt
app = Flask(__name__)

modules = {}
modules['content'] = load_model('models','content')
modules['grammar'] = load_model('models','grammar')

@app.route('/')
def index():
    return render_template("index.html",
            content_score=predictor('', '', "content"),
            grammar_score=rule_out('', '', "grammar"),
            relevance_score=rule_out('', '', "relevance"),
            title='', essay='')

@app.route('/', methods=['POST'])
def my_form_post():
    essay_title = request.form['title']
    essay_text = request.form['essay']
    return render_template("index.html",
            content_score=predictor(essay_title, essay_text, "content"),
            grammar_score=rule_out(essay_title, essay_text, "grammar"),
            relevance_score=rule_out(essay_title, essay_text, "relevance"),
            title=essay_title, essay=essay_text)

def predictor(essay_title = None, essay_text = None, module=None):
    if empty(essay_title) or empty(essay_text) or empty(module):
        return '0/100'

    result = modules[module].predict(transform(np.array([essay_text]), module))
    return "{0}/100".format(round(adjust_score(result[0], essay_text), 2))

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
    if text_length < 200:
        divisor = 1.01 ** (200 - text_length)
        return result / divisor
    if text_length > 800:
        divisor = 1.01 ** (text_length - 800)
        return result / divisor

    if result > 1.0:
        result = 1.0 / result

    return result


def rule_out(essay_title, essay_text, module = None):
    if empty(essay_title) or empty(essay_text) or empty(module):
        return '0/100'

    result = rule_score(module, essay_title, essay_text)
    result *= 100.0
    return "{0}/100".format(round(result, 2))


def empty(variable):
    if variable is None or len(variable)==0:
        return True
    return False

if __name__ == '__main__':
    app.run()
