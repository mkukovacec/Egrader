from flask import Flask, request, render_template
from util import transform, load_model
import numpy as np
app = Flask(__name__)

modules = {}
modules['content'] = load_model('models','content')
modules['development'] = load_model('models','development')
modules['grammar'] = load_model('models','grammar')
modules['organization'] = load_model('models','organization')
modules['style'] = load_model('models','style')

@app.route('/')
def index():
    return render_template("index.html",
            content_score=predictor('', '', "content"),
            development_score=predictor('', '', "development"),
            grammar_score=predictor('', '', "grammar"),
            organization_score=predictor('', '', "organization"),
            style_score=predictor('', '', "style"),
            title='', essay='')

@app.route('/', methods=['POST'])
def my_form_post():
    essay_title = request.form['title']
    essay_text = request.form['essay']
    return render_template("index.html",
            content_score=predictor(essay_title, essay_text, "content"),
            development_score=predictor(essay_title, essay_text, "development"),
            grammar_score=predictor(essay_title, essay_text, "grammar"),
            organization_score=predictor(essay_title, essay_text, "organization"),
            style_score=predictor(essay_title, essay_text, "style"),
            title=essay_title, essay=essay_text)

def predictor(essay_title = None, essay_text = None, module=None):
    if empty(essay_title) or empty(essay_text) or empty(module) or empty(modules[module]):
        return '0'
    return "{0}/1".format(round(modules[module].predict(transform(np.array([essay_text]), module))[0][0], 3))

def empty(variable):
    if variable is None or len(variable)==0:
        return True
    return False

if __name__ == '__main__':
    app.run()
