#!/usr/bin/env python

from sklearn.neighbors import KNeighborsRegressor

def get ():
    nneighours = 5
    weights = 'distance'
    
    model = KNeighborsRegressor ( n_neighbors = nneighours,
                                  weights = weights)

    return model
