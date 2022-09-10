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
        
        if not self.is_xvalidation_available ():
            exit(1)

        if self.input_is_valid ():
            self.logger.print_info (" - input label:\t %s" % self.input)
            self.init_input ()
        else:
            self.logger.print_error ("Input %s not valid: EXIT" % self.input)
            exit(1)
        
    def init_input (self):
        pkl_file = "pkl/%s/df/df.pkl" % self.input
        self.logger.print_debug ("     reading from %s as 'initial'" % pkl_file)
        self.df = {}
        self.df ["initial"] = pd.read_pickle (pkl_file)
            
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
            return
        self.logger.print_error ("No x-validation given: EXIT")
        self.logger.print_error ("Choose among: 50-50, 80-20, kfold:k (k = number of k-folds)")
        return False

    def input_is_valid (self):
        pkl_file = "pkl/%s/df/df.pkl" % self.input
        from utils.management import is_this_file_there
        return is_this_file_there (pkl_file)
