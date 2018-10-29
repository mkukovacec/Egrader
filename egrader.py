from flask import Flask, request, render_template
from util import transform, load_model
import numpy as np
app = Flask(__name__)

model = load_model('models/features_model')

@app.route('/')
def index():
    return render_template("index.html", score=predictor(), title='', essay='')

@app.route('/', methods=['POST'])
def my_form_post():
    essay_title = request.form['title']
    essay_text = request.form['essay']
    return render_template("index.html", score=predictor(essay_title, essay_text), title=essay_title, essay=essay_text)

def predictor(essay_title = None, essay_text = None):
    if empty(essay_title) or empty(essay_text):
        return '0'
    return "{0}/1".format(round(model.predict(transform(np.array([essay_text])))[0][0], 3))

def empty(variable):
    if variable is None or len(variable)==0:
        return True
    return False

if __name__ == '__main__':
    app.run()
