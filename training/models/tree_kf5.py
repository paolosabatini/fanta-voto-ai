#!/usr/bin/env python

from sklearn import tree

def get ():
    max_depth = 4
    model = tree.DecisionTreeRegressor( max_depth = max_depth )

    return model


def train ( X, y):
    model= get()
    model.fit (X,y)
    return model
    
