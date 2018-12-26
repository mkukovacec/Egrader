import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
import features as all_features
import os.path
import pickle

def transform(data, module=None):
    matrix = np.empty((data.shape[0], 1))

    features = [feat for feat in all_features.get_all_features(module)]
    for feature in features:
        feat = feature(data)
        feature_values = feat.run()
        print (feature_values)
        matrix = np.concatenate((matrix, feature_values.T), axis=1)

    return np.array(matrix, dtype=np.float64)

def preprocess_text(text):

    pass

def load_model(folder_name, module):
    filename = folder_name+'/'+module+'_module'
    if os.path.isfile(filename):
        return pickle.load(open(folder_name+'/'+module+'_module', 'rb'))

    return None

def dump_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
        print ("Model dumped into: {}".format(filename))

def tune_parameters(xs, ys):
    parameters = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}
    lr = LinearRegression()

    grid = GridSearchCV(estimator=lr, param_grid=parameters, cv=5, scoring = 'neg_mean_squared_error', )
    grid.fit(xs, ys)
    print ("---best parameters: {0}".format(grid.best_params_))
    return grid.best_params_

def get_trained_model(xs, ys, module=None):
    print("MODULE: {0}".format(module))
    print("---Transforming module data")
    x_transformed = transform(xs, module)
    print("---Tuning parameters")
    params = tune_parameters(x_transformed, ys)
    print("---Training module on whole dataset")
    model = train_model(x_transformed, ys, params)
    print("---Dumping module")
    dump_model(model, "models/"+module+"_module")
    print("---------------------------------")

def train_model(xs, ys, params):
    lr = LinearRegression(**params)
    lr.fit(xs, ys)

    return lr
