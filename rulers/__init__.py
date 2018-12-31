import os

from importlib import import_module

def calculate_score(module=None, essay_title=None, essay_text=None):
    files = ['rulers/'+module+'/'+name for name in os.listdir('./rulers/'+module)]
    for fname in files:
        if fname.endswith('.pyc'):
            os.remove(fname)

    score = 1.0
    for filename in files:
        if '.py' not in filename or '__' in filename:
            continue

        module_name = filename.split('/')[-1].split('.')[0]
        class_module = import_module('rulers.' + module +'.' + module_name)
        feature = getattr(class_module, 'Ruler')
        ruler = feature(essay_title, essay_text)
        score = score * ruler.run()

    return score
