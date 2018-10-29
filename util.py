import numpy as np
import features as all_features
import pickle

def transform(data):
    matrix = np.empty((data.shape[0], 1))

    features = [getattr(all_features, name)
                for name in all_features.__all__]

    for feature in features:

        feature = feature(data)
        feature_values = feature.run()
        matrix = np.concatenate((matrix, feature_values.T), axis=1)

    return np.array(matrix)

def preprocess_text(text):

    pass

def load_model(filename):
    return pickle.load(open(filename, 'rb'))
