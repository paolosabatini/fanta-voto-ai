#!/usr/bin/env python

from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn import ensemble
from numpy import ravel

def get ():
    
    params = {
    "n_estimators": 500,
    "max_depth": 4,
    "min_samples_split": 5,
    "learning_rate": 0.01,
    "loss": "squared_error",
    }    
    model = ensemble.GradientBoostingRegressor(**params)

    return model


def train ( X, y, model_settings = None):
    model= get()
    model.fit (X,ravel (y)) # warinng about the format
    return model, None
    
