#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
import pandas as pd
import os


class Trainer():

    _parquet_path = "./data/parquet"
    _pkl_path = "./data/pkl"
    
    def __init__ (self, model, input, xvalidation):
        self.model = model
        self.input = input
        self.model_settings = None
        self.xvalidation = xvalidation
        self.init()
        
    def init(self):
        logging.info ("initializing..")
        if not self.model:
            logging.error ("ERROR: No model in input: EXIT")
            exit(1)
        else:
            self.init_model ()

        self.init_input ()

        if not self.is_xvalidation_available ():
            exit(1)
        else:
            self.init_train_test ()
            
    def init_model(self):
        from importlib import import_module
        try:
            mymodel = import_module ('.models.%s' % self.model, package = 'utils.training')
            self.mdl = mymodel
        except:
            logging.error ("ERROR: Model %s not found: EXIT" % self.model)
            exit(1)

    def init_input(self):
        parquet_file = "%s/%s/data.parquet" % (self._parquet_path,self.input)

        if not os.path.exists( parquet_file):
            logging.error("ERROR: Input file %s not found: EXIT" % self.input)
            exit(1)
            
        logging.info("Reading input file %s as 'initial'" % self.input)
        self.df = {}
        self.df ["initial"] = pd.read_parquet (parquet_file)
        # init X, y
        target = 'Mark'
        features = [x for x in self.df['initial'].columns.tolist() if x != target]

        # Some final touches: set indices as int and remove names
        self.df ['X'] = self.df ["initial"] [ features ].reset_index ().drop(["index"], axis =1) 
        self.df ['y'] = self.df ["initial"] [ target ].reset_index ().drop(["index"], axis =1 )

    def is_xvalidation_available (self):
        if not self.xvalidation:
            logging.error ("ERROR: No x-validation given: EXIT")
            logging.error ("Choose among: 50-50, 80-20, kfold:k (k = number of k-folds)")
            return False
        elif self.xvalidation == '50-50':
            logging.info (" X-validation:\t train/test = 50%/50%" )
            return True
        elif self.xvalidation == '80-20':
            logging.info (" X-validation:\t train/test = 80%/20%" )
            return True
        elif 'kfold' in self.xvalidation:
            self.kfold = int (self.xvalidation.split (":")[-1])
            logging.info ("X-validation:\t K-folding (K = %d)"% self.kfold)
            return True
        logging.error ("No valid x-validation given: EXIT")
        logging.error ("Choose among: 50-50, 80-20, kfold:k (k = number of k-folds)")
        return False

    def init_train_test (self):
        logging.debug ("   \tinit. train/test samples")
        
        if self.xvalidation in ['50-50', '80-20']:
            # in this case we get a list of 1 element of dataframes for each X_train/test, Y_train/test
            self.df['X_train'], self.df['X_test']  = [None], [None]
            self.df['y_train'], self.df['y_test']  = [None], [None]
            frac_train = float (self.xvalidation.split ("-")[0]) / 100 # fraction given as %
            self.df['X_train'][0], self.df['X_test'][0], self.df ['y_train'][0], self.df['y_test'][0] = self.get_frac_train_test ( frac_train )
        elif 'kfold' in self.xvalidation:
            from sklearn.model_selection import KFold
            kf = KFold(n_splits=self.kfold, shuffle = True, random_state = 1) # this generates kf splitter (shuffle it because is ordered)
            # in this case we get a list of dataframes for each X_train/test, Y_train/test
            self.df['X_train'], self.df['X_test']  = [], []
            self.df['y_train'], self.df['y_test']  = [], []
            
            for index_train, index_test in kf.split (self.df['X']): # this splits the indices of X
                self.df['X_train'].append ( self.df['X'].iloc[ index_train ] )
                self.df['y_train'].append ( self.df['y'].iloc[ index_train ] )
                self.df['X_test'].append ( self.df['X'].iloc[ index_test ] )
                self.df['y_test'].append ( self.df['y'].iloc[ index_test ] )

        logging.debug ("   \t\t ..done")



    def train (self):

        logging.info ("training..")
        n_training_sets = len (self.df['X_train'])
        self.trained_models = []
        self.trained_model_histories = []
        for itrain in range (n_training_sets):
            logging.info ("\t - set %d/%d" % (itrain+1, n_training_sets))
            if 'tfnn' in self.model:
                thismodel, thishistory = self.mdl.train ( self.df['X_train'][itrain], self.df['y_train'][itrain],
                                                          model_settings = self.model_settings,
                                                          X_test = self.df['X_test'][itrain], y_test = self.df['y_test'][itrain] )
            else:
                thismodel, thishistory = self.mdl.train ( self.df['X_train'][itrain], self.df['y_train'][itrain], self.model_settings)
            self.trained_models.append (thismodel)
            self.trained_model_histories.append (thishistory)
        logging.info ("\t..done.")

    def save (self, label):
        import pickle

        n_trained_models = len (self.trained_models)
        path_for_models = '%s/%s/model' % (self._pkl_path, self.input)
        from utils.system.SystemHelper import check_and_create_folder
        check_and_create_folder (path_for_models)
        path_for_thismodel = '%s/%s' % (path_for_models, label)
        check_and_create_folder (path_for_thismodel)
        logging.info ("saving the trained model in %s" % path_for_thismodel)

        for imodel in range (n_trained_models):
            logging.info ("\t - model (with history), test & train %d/%d" % (imodel+1, n_trained_models))
            
            model_pkl_name = "%s/%s_%d.pkl" % (path_for_thismodel, self.model, imodel)
            pickle.dump (self.trained_models[imodel], open (model_pkl_name, 'wb'))
            logging.debug ("\t   saved model to %s" % (model_pkl_name))

            history_pkl_name = "%s/history_%d.pkl" % (path_for_thismodel, imodel)
            if self.trained_model_histories [imodel]:
                pickle.dump ( self.trained_model_histories [imodel],  open (history_pkl_name, 'wb'))
                logging.debug ("   saved history to %s" % (history_pkl_name))
            
            for ds_name in ['X_train', 'y_train', 'X_test', 'y_test']:
                df_pkl_name = "%s/%s_%d.pkl" % (path_for_thismodel, ds_name, imodel)
                self.df[ds_name][imodel].to_pickle (df_pkl_name)
                logging.debug ("\t   saved %s to %s" % (ds_name,df_pkl_name))

        logging.info ("   ..done")
