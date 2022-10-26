#!/usr/bin/env python

import pandas as pd
import numpy as np

def init_input_for_analysis ( analysis ):
    if not analysis: return False
    
    n_datasets = get_list_of_datasets ( analysis )
    n_models = get_list_of_models ( analysis )

    analysis.df = {}
    analysis.model = {}
        
    analysis.logger.print_debug ("   \tget input datasets (%d)" % n_datasets)
    for df_name in ['X_train', 'X_test', 'y_train', 'y_test']:
        for i_df in range (n_datasets):
            pkl_file= "%s/%s_%d.pkl" % (analysis.input_folder, df_name, i_df)
            analysis.df [df_name + "_" + str(i_df)] = pd.read_pickle(pkl_file)
                

    analysis.logger.print_debug ("   \tget input models (%d)" % n_models)
    for i_mod in range (n_datasets):
        pkl_file= "%s/%s_%d.pkl" % (analysis.input_folder, analysis.model_name, i_mod)
        analysis.model [ "model_" + str(i_mod)] = pd.read_pickle(pkl_file)

    return True

def init_history_for_analysis ( analysis ):
    if not analysis: return False
    
    n_datasets = get_list_of_datasets ( analysis )
    n_models = get_list_of_models ( analysis )
    n_histories = get_list_of_histories ( analysis )
    
    analysis.histories = {}
        
    analysis.logger.print_debug ("   \tget history (%d)" % n_datasets)
    for i_df in range (n_datasets):
        pkl_file= "%s/history_%d.pkl" % (analysis.input_folder, i_df)
        analysis.histories [str(i_df)] = pd.read_pickle(pkl_file)

    return True

def init_input_for_df_analysis ( analysis ):
    if not analysis: return False
    
    analysis.df = {}
    analysis.model = {}

    pkl_file= "%s/df.pkl" % (analysis.input_folder)
    analysis.logger.print_debug ("   \tget input dataset:\t %s" % pkl_file)
    analysis.df ['X'] = pd.read_pickle(pkl_file)

    return True


def get_list_of_datasets ( analysis ):
    reference_name = 'X_train'
    wildcard = "%s/%s_*.pkl" % (analysis.input_folder, reference_name)
    import glob
    return len ( glob.glob (wildcard) ) 


def get_list_of_histories ( analysis ):
    reference_name = 'history'
    wildcard = "%s/%s_*.pkl" % (analysis.input_folder, reference_name)
    import glob
    return len ( glob.glob (wildcard) ) 

            

def get_list_of_models ( analysis ):
    
    import glob
    analysis.model_name = [ name for name in glob.glob ("%s/*_0.pkl" % analysis.input_folder) if name.split("/")[-1][:2] not in ['X_', 'y_'] ] [0].split ("/")[-1].replace ('_0.pkl','')
    wildcard = "%s/%s_*.pkl" % (analysis.input_folder, analysis.model_name)
    return (len (glob.glob (wildcard)))


        

def get_array_from_series (df_coll, col_name):
    n_models = len ([ x for x in df_coll.keys() if col_name in x])
    return np.concatenate ( [ df_coll['%s_%d' % (col_name, i)].to_numpy() for i in range (n_models) ], axis=0  )




def decode_position (val):
    step = 10
    if val == 0: return 'G' #'P'
    elif val == step: return 'D'
    elif val == 2*step: return 'M' # 'C'
    elif val == 3*step: return 'F' # 'A'
    return 'UNKNOWN'


def encode_position (pos):
    step = 10
    if pos == 'G' or pos == 'P': return 0 
    if pos == 'D': return step 
    if pos == 'C' or pos == 'M': return 2*step 
    if pos == 'A' or pos == 'F': return 3*step 
    return 'UNKNOWN'



def shape_df_for_predicting (df):
    features = df.columns.tolist()
    to_be_removed = ['prediction', 'target', 'residual']
    for feat in to_be_removed: features.remove (feat)
    return df[features]

