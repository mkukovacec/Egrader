import os

import pkgutil
import inspect

def get_all_features(module=None):

    files = ['features/'+module+'/'+name for name in os.listdir('./features/'+module)]
    for fname in files:
        if fname.endswith('.pyc'):
            os.remove(fname)

    for loader, orig_name, is_pkg in pkgutil.walk_packages(__path__):
        module = loader.find_module(orig_name).load_module(orig_name)

        for name, value in inspect.getmembers(module):
            if name != 'Feature':
                continue
            if name.startswith('__'):
                continue
            globals()[orig_name] = value
            __all__.append(orig_name)
