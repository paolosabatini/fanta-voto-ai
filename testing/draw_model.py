#!/usr/bin/env python

from .plot_helpers import plot_model_scheme
from utils.myprint import myprint
import pandas as pd
import numpy as np


class draw_model ():

    plots = {}
    
    def __init__ (self, debug, input_folder):
        self.debug = debug
        self.input_folder = input_folder
        self.init()
        
    
    def init (self):
        self.logger = myprint ("simple   ", self.debug)
        self.logger.print_info ("initializing..")

        self.logger.print_info (" - reading input from %s" % self.input_folder)

        from .analysis_helpers import init_input_for_analysis
        if init_input_for_analysis ( analysis = self):
            self.logger.print_info ("   .. done")
        else:
            self.logger.print_error ("Failed reading the input files: EXIT")
            exit (1)

   
    def execute (self):

        self.logger.print_info ("starting analysis..")
        arrays = {}

        self.logger.print_debug ("   draw model scheme")


        imod = 0
        features = self.df ['X_train_0'].columns.tolist()
        self.plots ['model_scheme_%d' % 0] = plot_model_scheme ( self.model ['model_%d' % imod], model_name = self.model_name, features = features )

        ## deal with the output in case of keras_visualizer
        if 'tfnn' in self.model_name:
            self.plots.pop ('model_scheme_%d' % 0)
            


        
    def save ( self, output_label ):

        output_folder = 'output'
        self.logger.print_info ("saving output..")
        self.logger.print_info (" - output label:\t %s" % output_label)
        from utils.management import check_folder_and_create, is_this_folder_there
        check_folder_and_create (output_folder)
        output_subfolder = "%s/%s" % (output_folder, output_label)
        check_folder_and_create (output_subfolder)

        for plot_name in self.plots.keys():
            self.logger.print_debug ("   saving %s" % plot_name)
            ext = 'png' if 'scheme' not in plot_name else 'pdf'
            plot_path = "%s/%s.%s" % (output_subfolder, plot_name, ext)
            self.plots [plot_name].savefig (plot_path)

        if 'tfnn' in self.model_name:
            import os
            if 'graph.pdf' in os.listdir (os.getcwd()):
                os.system ('mv graph.pdf %s/model_scheme_0.pdf' % output_subfolder)
            
        self.logger.print_info (" ...done ")
