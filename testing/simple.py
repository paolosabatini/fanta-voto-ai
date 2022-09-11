#!/usr/bin/env python

from utils.myprint import myprint
import pandas as pd

class simple ():

    def __init__ (self, debug, input_folder):
        self.debug = debug
        self.input_folder = input_folder
        self.init()
        
    
    def init (self):
        self.logger = myprint ("simple   ", self.debug)
        self.logger.print_info ("initializing..")

        self.logger.print_info (" - reading input from %s" % self.input_folder)

        from analysis_helpers import init_input_for_analysis
        if init_input_for_analysis ( analysis = self):
            self.logger.print_info ("   .. done")
        else:
            self.logger.print_error ("Failed reading the input files: EXIT")
            exit (1)


    
    def execute (self):
        print self.df['X_train_0'].head ()
