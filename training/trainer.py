#!/usr/bin/env python

from utils.myprint import myprint
import pandas as pd

class trainer ():

    def __init__ (self, debug, model, input, xvalidation):
        self.debug = debug
        self.model = model
        self.input = input
        self.xvalidation = xvalidation
        self.init ()


    def init (self):
        
        self.logger = myprint ("trainer", self.debug)
        self.logger.print_info ("initializing..")

        if not self.model:
            self.logger.print_error ("No model in input: EXIT")
            exit(1)
        else:
            self.logger.print_info (" - model:\t\t %s" % self.model)
            self.init_model ()
            
        if self.input_is_valid ():
            self.logger.print_info (" - input label:\t %s" % self.input)
            self.init_input ()
        else:
            self.logger.print_error ("Input %s not valid: EXIT" % self.input)
            exit(1)


        if not self.is_xvalidation_available ():
            exit(1)
        else:
            self.init_train_test ()

    def init_model (self):
        model_file = 'training/models/%s.py' % self.model
        model_import_str = "import models.%s as mymodel" % (self.model)
        exec (model_import_str)
        self.mdl = mymodel.get()

        
    def init_input (self):
        pkl_file = "pkl/%s/df/df.pkl" % self.input
        self.logger.print_debug ("  \treading from %s as 'initial'" % pkl_file)
        self.df = {}
        self.df ["initial"] = pd.read_pickle (pkl_file)
        # init X, y
        target = 'Punteggio'
        features = [x for x in self.df['initial'].columns.tolist() if x != target]
        self.df ['X'] = self.df ["initial"] [ features ].reset_index () # useful to have int index here
        self.df ['y'] = self.df ["initial"] [ target ].reset_index () # useful to have int index here


    def init_train_test (self):
        self.logger.print_debug ("   \tinit. train/test samples")
        
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

        self.logger.print_debug ("   \t\t ..done")
        
        

    def get_frac_train_test ( self, frac_train ):
        from sklearn.model_selection import train_test_split
        return train_test_split (self.df['X'],self.df['y'], test_size = frac_train, random_state = 1)
            
    def is_xvalidation_available (self):
        if not self.xvalidation:
            self.logger.print_error ("No x-validation given: EXIT")
            self.logger.print_error ("Choose among: 50-50, 80-20, kfold:k (k = number of k-folds)")
            return True
        elif self.xvalidation == '50-50':
            self.logger.print_info (" - x-validation:\t train/test = 50%/50%" )
            return True
        elif self.xvalidation == '80-20':
            self.logger.print_info (" - x-validation:\t train/test = 80%/20%" )
            return True
        elif 'kfold' in self.xvalidation:
            self.kfold = int (self.xvalidation.split (":")[-1])
            self.logger.print_info (" - x-validation:\t K-folding (K = %d)"% self.kfold)
            return True
        self.logger.print_error ("No x-validation given: EXIT")
        self.logger.print_error ("Choose among: 50-50, 80-20, kfold:k (k = number of k-folds)")
        return False

    def input_is_valid (self):
        pkl_file = "pkl/%s/df/df.pkl" % self.input
        from utils.management import is_this_file_there
        return is_this_file_there (pkl_file)
