#!/usr/bin/env python

from training.helpers import decode_settings_to_dict

from keras.models import Sequential
from keras.layers import Dense, Activation, Layer, Lambda

from tensorflow.keras import callbacks
from tensorflow.data import Dataset

from numpy import ravel

def get (model_settings = None, n_input_features = 16):

    model_settings = decode_settings_to_dict (model_settings)

    layers = [30]
    if 'layers' in model_settings.keys():
        layers = model_settings ['layers'].split ("/")
            
    optimizer = 'rmsprop'
    if 'optimizer' in model_settings.keys():
        optimizer = model_settings ['optimizer']

    kernel_init = 'normal'
    if 'kernel_init' in model_settings.keys():
        kernel_init = model_settings ['kernel_init']

    activation = 'relu'
    if 'activation' in model_settings.keys():
        activation = model_settings ['activation']

    loss = 'mean_absolute_error'
    if 'loss' in model_settings.keys():
        loss = model_settings ['loss']


    model = Sequential ()

    model.add(Dense(layers[0],
                    input_dim=n_input_features,
                    kernel_initializer=kernel_init,
                    activation = activation))
    for i in range ( 1, len (layers)):
        model.add(Dense(layers[i],activation=activation))

    model.add (Dense (1))

    model.compile ( loss = loss,
                    optimizer = optimizer)

    return model


def train ( X, y, model_settings = None, X_test = None, y_test = None):
    model= get(model_settings, n_input_features = X.shape[-1])

    #implementing early stopping to not give manual epochs
    max_epochs = 100
    callback = callbacks.EarlyStopping(monitor='loss', patience=3)
    
    
    try:
        testing_df = (X_test.values, y_test.values)
    except:
        testing_df = None
        
    history = model.fit (X,ravel (y), # warinng about the format
                         epochs=max_epochs,
                         batch_size=1, # small dataset, no need of batches
                         callbacks=[callback],
                         validation_data = testing_df)

    
    
    return model, history
    
