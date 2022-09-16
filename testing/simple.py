#!/usr/bin/env python

from plot_helpers import correlation_plot, residual_vs_var_plot
from utils.myprint import myprint
import pandas as pd
import numpy as np


class simple ():

    plots = {}
    
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


    def augment_df (self):
        n_models =  len (self.model.keys())
        for imod in range (n_models):
            for dataset in ['train', 'test']:

                self.df ['X_%s_%d' % (dataset,imod)] ['prediction'] = self.model ['model_%d' % imod].predict (self.df [ 'X_%s_%d' % (dataset,imod) ])
                self.df ['X_%s_%d' % (dataset,imod)] ['target'] = self.df [ 'y_%s_%d' % (dataset,imod) ]
                self.df ['X_%s_%d' % (dataset,imod)] ['residual'] = self.df['X_%s_%d' % (dataset,imod)] ['prediction'] - self.df['X_%s_%d' % (dataset,imod)] ['target'] 
            
    
    def execute (self):

        self.logger.print_info ("starting analysis..")
        arrays = {}

        self.logger.print_debug ("   augmenting variables in the df")
        self.augment_df ()
        
        from analysis_helpers import get_array_from_series 
        arrays ['y_train'] = get_array_from_series (self.df, 'y_train')
        arrays ['y_test'] = get_array_from_series (self.df, 'y_test')

        n_models = len (self.model.keys())
        # arrays ['pred_train'] = np.concatenate ( [ self.model ['model_%d' % imod].predict ( self.df['X_train_%d' % imod] ) for imod in range (n_models) ], axis=0)
        # arrays ['pred_test'] = np.concatenate ( [ self.model ['model_%d' % imod].predict ( self.df['X_test_%d' % imod] ) for imod in range (n_models) ], axis=0)
        arrays ['pred_train'] = np.concatenate ( [ self.df['X_train_%d' % imod]['prediction'] for imod in range (n_models) ], axis=0)
        arrays ['pred_test'] = np.concatenate ( [ self.df['X_test_%d' % imod]['prediction'] for imod in range (n_models) ], axis=0)
        
        self.logger.print_debug ("   correlation plot y/prediction corr.")
        self.plots ['test_y_vs_pred'] = correlation_plot (
            xarray = arrays ['y_test'], yarray = arrays ['pred_test'],
            xlabel = 'Actual vote', ylabel = 'Predicted vote',
            xlim = [4,10], ylim = [4,10],
            labels = ["Test dataset", "Model: %s" % self.model_name])

        self.plots ['train_y_vs_pred'] = correlation_plot (
            xarray = arrays ['y_train'], yarray = arrays ['pred_train'],
            xlabel = 'Actual vote', ylabel = 'Predicted vote',
            xlim = [4,10], ylim = [4,10],
            labels = ["Train dataset", "Model: %s" % self.model_name])


        self.logger.print_debug ("   residual per ruolo")
        from analysis_helpers import encode_position
        all_data = []
        for pos in  ['G', 'D', 'M', 'F']:
            all_data.append (
                np.concatenate ([ self.df['X_test_%d' % imod].loc [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ] ['residual'] for imod in range (n_models) ])
            )

        self.plots ['test_res_vs_role'] = residual_vs_var_plot (
            data = all_data, labels =  ['G', 'D', 'M', 'F'],
            xlabel = 'Position', ylabel = 'Residual (predicted - target) vote',
            ylim = [-2,4],
            decos = ["Train dataset", "Model: %s" % self.model_name]
            
        )
        






        
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
            plot_path = "%s/%s.png" % (output_subfolder, plot_name)
            self.plots [plot_name].savefig (plot_path)

        self.logger.print_info (" ...done ")
