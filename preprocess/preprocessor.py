#!/usr/bin/env python

from dataprep.conf import _PKL_FOLDER_, _DATA_FOLDER_
from utils.myprint import myprint
import os
import pandas as pd


class preprocessor ():
    setting_path = '%s/preprocess/settings' % os.getcwd()
       
    def __init__ ( self, setting, debug):
        self.debug = debug
        self.setting = setting
        self.init ()

    def init (self):
        self.logger = myprint ("preprocessor", self.debug)
        self.logger.print_info ("initializing..")
        
        from utils.management import read_json_to_dict
        conf_file = '%s/%s.json' % (self.setting_path, self.setting)
        self.configuration = read_json_to_dict (conf_file)
        

        self.logger.print_info (" - reading from %s" % conf_file)
        self.logger.print_debug ("   target: \t %s" % self.configuration['label'])
        
        try:
            self.logger.print_debug ("   n. features\t players\t %d" % len (self.configuration['features']['players']))
        except:
            self.logger.print_debug ("   n. features\t players\t 0")

        try:
            self.logger.print_debug ("   n. features\t fixtures\t %d" % len (self.configuration['features']['fixtures']))
        except:
            self.logger.print_debug ("   n. features\t fixtures\t 0")

        try:
            self.logger.print_debug ("   n. features\t performance\t %d" % len (self.configuration['features']['performance']))
        except:
            self.logger.print_debug ("   n. features\t performance\t 0")




    def get_all_pandas (self):
        self.logger.print_info ("retrieving all data..")
        from utils.management import get_availaible_matchdays 
        self.matchdays = get_availaible_matchdays (_DATA_FOLDER_)
        datasets_to_read = self.get_datasets_to_read ()
        self.logger.print_debug (" - n. matchdays:\t %d" % len (self.matchdays))
        self.logger.print_debug (" - ds to read:  \t %s" % ", ".join(datasets_to_read))

        self.import_all_json_to_pandas ( list_of_datasets = datasets_to_read )

        

        
    def get_datasets_to_read (self):
        ds_to_read = []
        key_ds = self.configuration['label'].split ("/")[0]
        ds_to_read = [key_ds]

        label_ds = self.configuration['key'].split ("/")[0]
        if label_ds not in ds_to_read: ds_to_read.append (label_ds)

        for ds in ['players', 'fixtures', 'performance', 'votes']:
            if ds not in ds_to_read and ds in self.configuration['features'].keys(): ds_to_read.append (ds)

        return ds_to_read


    def get_cols (self):
        cols = [ self.configuration['label'].split ("/")[-1] ]
        for ds in ['players', 'fixtures', 'performance', 'votes']:
            if ds not in self.configuration['features'].keys(): continue
            for feat in self.configuration['features'][ds]:
                if feat in cols: continue
                cols.append (feat)

        return cols

    def get_augmented_cols (self):
        cols = self.configuration['transformer']['augment']
        return cols

    def import_all_json_to_pandas (self, list_of_datasets = []):
        import copy
        self.pandas = {}
        for md in self.matchdays:
            self.pandas [md] = {}
            for ds in list_of_datasets:
                dsname = "%s/Matchday_%d/%s.json" % (_DATA_FOLDER_, md, ds)
                orient = 'index' if ds in ['players','votes'] else 'records'
                self.pandas [md] [ds] = pd.read_json (dsname, orient = orient)
                
        
    def connect_and_select ( self, ds_to_connect = {} ):
        
        if 'votes' in ds_to_connect.keys():
            ds_merged = ds_to_connect['votes']
            
        if 'players' in ds_to_connect.keys():

        
            ds_merged = pd.merge ( left = ds_merged,
                                   right = ds_to_connect['players'],
                                   how= "left",
                                   left_index=True, right_index=True)
            ds_merged ['Squadra'] = ds_merged ['Squadra_x']
            ds_merged = ds_merged.drop (['Squadra_x','Squadra_y'], axis=1)
            
        if 'fixtures' in ds_to_connect.keys():
            ds_home = ds_merged.reset_index().merge (  ds_to_connect['fixtures'],left_on = ["Squadra"], right_on = ["home"]).set_index('index')
            ds_away = ds_merged.reset_index().merge (  ds_to_connect['fixtures'],left_on = ["Squadra"], right_on = ["away"]).set_index('index')
            ds_merged = pd.concat ([ds_home, ds_away])

        if 'performance' in ds_to_connect.keys():
            ds_merged = ds_merged.reset_index().merge (  ds_to_connect['performance'], left_on = "home",right_on = "team").set_index('index')
            ds_merged = ds_merged.reset_index().merge (  ds_to_connect['performance'], left_on = "away",right_on = "team", suffixes = ['','_away']).set_index('index')



        # in case of nam: remove them
        ds_merged = ds_merged.dropna ()
        return ds_merged [ self.get_cols() ] 


    def concatenate ( self, key_to_concatenate ):
        return pd.concat ( [self.pandas[md][key_to_concatenate] for md in self.matchdays], axis = 0 )


    def transform ( self, key_to_transform ):
        ds = self.pandas [key_to_transform]


        # augment
        if 'augment' in self.configuration['transformer']:
            import preprocess.augmenter as augmenter
            self.logger.print_debug ("   augmenting now:")
            
            for var_aug in  self.configuration['transformer']['augment']:
                self.logger.print_debug ("    ++ %s" % var_aug)
                getattr (augmenter, var_aug) (ds)


        # gaussian scaler on the "continuous" variables
        from sklearn.preprocessing import scale
        std_scale_list = self.configuration['transformer']['std']
        
        cols_to_scale = [x for x in std_scale_list if x in self.get_cols()+self.get_augmented_cols()  ]
        self.logger.print_debug ("   std scaler to %s" % ", ".join (cols_to_scale))
        if cols_to_scale != []: ds [ cols_to_scale ] = scale ( ds [ cols_to_scale ] )

        # linear scale on the other variables
        lin_scale_list = self.configuration['transformer']['linear']
        cols_to_scale = [x for x in lin_scale_list if x in self.get_cols()+self.get_augmented_cols()   ]
        self.logger.print_debug ("   linear scaler to %s" % ", ".join (cols_to_scale))
        if cols_to_scale != []: ds [ cols_to_scale ] = self.linear_scale ( ds [ cols_to_scale ] )

        # role transformer
        if 'Ruolo' in self.get_cols():
            step_role = 1
            ds = ds.replace ("Attaccante", 3*step_role).replace ("Centrocampista", 2*step_role).replace ("Difensore", 1*step_role).replace ("Portiere", 0*step_role)
            self.logger.print_debug ("   role transformer (A : %d, C : %d, D : %d, P : %d)" % (3*step_role, 2*step_role, 1*step_role, 0*step_role))

           
        # clean
        if 'clean' in self.configuration['transformer']:
            list_to_clean = self.configuration['transformer']['clean']
            self.logger.print_debug ("   cleaning %s" % ", ".join (list_to_clean))
            ds = ds.drop(list_to_clean, axis=1)

        return ds

    def linear_scale (self, df):
        df_norm = df.copy()
        for column in df_norm.columns:
            col_min = df_norm[column].min()
            col_max = df_norm[column].max()
            if col_max != col_min:
                df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        
        return df_norm

        
    def preprocess (self):
        self.logger.print_info ("pre-process..")
        
        # connect datasets for each matchday
        self.logger.print_debug (" - connect datasets info for each matchday")
        for md in self.matchdays:
            ds_to_connect = self.pandas [md]
            self.pandas [md] ['conn_and_sel'] = self.connect_and_select (ds_to_connect)

        # concatenate multiple matchdays
        self.logger.print_debug (" - concatenate all matchdays")
        self.pandas ['concatenate_raw'] = self.concatenate ( key_to_concatenate = "conn_and_sel")
    
        # now transform
        self.logger.print_debug (" - preprocessing")
        self.pandas ['preprocessed'] = self.transform ('concatenate_raw')


        

    
    def save (self, label):
        self.logger.print_info ("storing to pickle..")
        from utils.management import check_folder_and_create
        check_folder_and_create (_PKL_FOLDER_)
        version_folder = '%s/%s' % (_PKL_FOLDER_, label)
        check_folder_and_create (version_folder)
        data_folder = '%s/df' % (version_folder)
        check_folder_and_create (data_folder)
        pkl_file = "%s/df.pkl" % data_folder
        self.logger.print_debug ("   to %s" % pkl_file)
        try:
            self.pandas ['preprocessed'].to_pickle (pkl_file)
        except:
            mp.print_error ("no preprocessed dataframe found!")

