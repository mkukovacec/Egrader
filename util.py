import numpy as np
import features as all_features
import os.path
import pickle

def transform(data, module=None):
    matrix = np.empty((data.shape[0], 1))

    features = [getattr(all_features, name)
                for name in all_features.get_all_features(module)]

    for feature in features:

        feature = feature(data)
        feature_values = feature.run()
        matrix = np.concatenate((matrix, feature_values.T), axis=1)

    return np.array(matrix)

def preprocess_text(text):

    pass

def load_model(folder_name, module):
    filename = folder_name+'/'+module+'_module'
    if os.path.isfile(filename):
        return pickle.load(open(folder_name+'/'+module+'_module', 'rb'))

    return None
