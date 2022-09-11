#!/usr/bin/env python

import pandas as pd
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
        
def get_list_of_datasets ( analysis ):
    reference_name = 'X_train'
    wildcard = "%s/%s_*.pkl" % (analysis.input_folder, reference_name)
    import glob
    return len ( glob.glob (wildcard) ) 

            

def get_list_of_models ( analysis ):
    
    import glob
    analysis.model_name = [ name for name in glob.glob ("%s/*_0.pkl" % analysis.input_folder) if name.split("/")[-1][:2] not in ['X_', 'y_'] ] [0].split ("/")[-1].replace ('_0.pkl','')
    wildcard = "%s/%s_*.pkl" % (analysis.input_folder, analysis.model_name)
    return (len (glob.glob (wildcard)))
    
        
