import os

from importlib import import_module

def get_all_features(module=None):
    all_values = []
    files = ['features/'+module+'/'+name for name in os.listdir('./features/'+module)]
    for fname in files:
        if fname.endswith('.pyc'):
            os.remove(fname)

    for filename in files:
        if '.py' not in filename or '__' in filename:
            continue

        module_name = filename.split('/')[-1].split('.')[0]
        class_module = import_module('features.' + module +'.' + module_name)
        all_values.append(getattr(class_module, 'Feature'))

    return all_values
