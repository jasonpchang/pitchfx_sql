import numpy as np
import pandas as pd

def split_data(X, y, percent_train, random_seed):
    """Split data into training and test sets
    
    Inputs:
        X: features numpy or pandas array (n_observations, n_features)
        y: response numpy or pandas array (n_observations, n_responses)
        percent_train: percent of observations taken to be the training set
        random_seed: seed for random selection of training observations
        
    Outputs:
        X_train: training features numpy or pandas array (percent_train*n_observations, n_features)
        X_test: test features numpy or pandas array ((1-percent_train*n_observations), n_features)
        y_train: training response or pandas numpy array (percent_train*n_observations, n_responses)
        y_test: test features numpy or pandas array ((1-percent_train*n_observations), n_responses)
        
    Notes:
        - data type in is the same as data type out
    """
    # check that X and y are same lengths
    if X.shape[0]!=y.shape[0]:
        print("Lengths of features and responses do no match")
        return
    
    # set parameters
    np.random.seed(random_seed)
    ndata = X.shape[0]
    rand_indices = np.random.choice([True, False], size=ndata, p=[percent_train, 1-percent_train])
    
    # get data
    try:
        X_train = X[rand_indices, :]
        X_test = X[~rand_indices, :]
    except:
        X_train = X.iloc[rand_indices, :]
        X_test = X.iloc[~rand_indices, :]
        
    if len(y.shape)==1:
        try:
            y_train = y[rand_indices]
            y_test = y[~rand_indices]
        except:
            y_train = y.iloc[rand_indices]
            y_test = y.iloc[~rand_indices]
    else:
        try:
            y_train = y[rand_indices, :]
            y_test = y[~rand_indices, :]
        except:
            y_train = y.iloc[rand_indices, :]
            y_test = y.iloc[~rand_indices, :]
    
    # clean up
    return X_train, X_test, y_train, y_test