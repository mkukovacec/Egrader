from flask import Flask, request, render_template
from util import transform, load_model, rule_score
import numpy as np
import nltk
app = Flask(__name__)

modules = {}
modules['content'] = load_model('models','content')
modules['grammar'] = load_model('models','grammar')

@app.route('/')
def index():
    return render_template("index.html",
            content_score=predictor('', '', "content"),
            grammar_score=predictor('', '', "grammar"),
            title='', essay='')

@app.route('/', methods=['POST'])
def my_form_post():
    essay_title = request.form['title']
    essay_text = request.form['essay']
    return render_template("index.html",
            content_score=predictor(essay_title, essay_text, "content"),
            grammar_score=rule_out(essay_title, essay_text, "grammar"),
            title=essay_title, essay=essay_text)

def predictor(essay_title = None, essay_text = None, module=None):
    if empty(essay_title) or empty(essay_text) or empty(module):
        return '0'

    result = modules[module].predict(transform(np.array([essay_text]), module))
    return "{0}/1".format(round(adjust_score(result[0], essay_text), 3))

def adjust_score(result, text):
    text_length = len(nltk.word_tokenize(text))
    if text_length < 200:
        divisor = 1.01 ** (200 - text_length)
        return result / divisor
    if text_length > 800:
        divisor = 1.01 ** (text_length - 200)
        return result / divisor

    return result

def rule_out(essay_title, essay_text, module = None):
    result = rule_score(module, essay_title, essay_text)

    return "{0}/1".format(round(result, 3))


def empty(variable):
    if variable is None or len(variable)==0:
        return True
    return False

if __name__ == '__main__':
    app.run()
