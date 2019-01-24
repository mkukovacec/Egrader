import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
import features as all_features
import rulers as ruler_score
import os.path
import pickle

def transform(data, module=None):
    matrix = np.empty((data.shape[0], 1))

    features = [feat for feat in all_features.get_all_features(module)]
    for feature in features:
        feat = feature(data)
        feature_values = feat.run()
        print ("{0} {1}".format(feature, feature_values))
        matrix = np.concatenate((matrix, feature_values.T), axis=1)
    return np.array(matrix, dtype=np.float64)

def rule_score(module, essay_title, essay_text):
    score = ruler_score.calculate_score(module, essay_title, essay_text)

    return score

def preprocess_data(data):
    toReturn = pd.DataFrame([])
    for i in range(1,9):
        set_i = data[data['essay_set'] == i]
        rating_columns = set_i.columns.values[3:].tolist()
        set_i['avg_score']=set_i[rating_columns].mean(axis=1)
        set_i['avg_score']=((set_i[rating_columns]-set_i[rating_columns].min())/(set_i[rating_columns].max()-set_i[rating_columns].min())).mean(axis=1)
        toReturn=toReturn.append(set_i)

    return toReturn

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
    parameters = {'alpha':[x*1.0/20 for x in range(20, 0, -1)]}
    ridge = Ridge()

    grid = GridSearchCV(estimator=ridge, param_grid=parameters, cv=5, scoring = 'neg_mean_squared_error', )
    grid.fit(xs, ys)
    print ("---best parameters: {0}".format(grid.best_params_))
    print ("---best score: {0}".format(str(grid.best_score_)))
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
    lr = Ridge(**params)
    lr.fit(xs, ys)

    return lr
