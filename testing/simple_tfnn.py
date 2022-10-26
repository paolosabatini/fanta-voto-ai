#!/usr/bAin/env python

from .plot_helpers import plot_permutation_feature_importance, plot_loss, correlation_plot, residual_vs_var_plot, compare_prediction_and_target, hist_per_classes
from utils.myprint import myprint
import pandas as pd
import numpy as np


class simple_tfnn ():

    plots = {}
    
    def __init__ (self, debug, input_folder):
        self.debug = debug
        self.input_folder = input_folder
        self.init()
        
    
    def init (self):
        self.logger = myprint ("simple-tfnn   ", self.debug)
        self.logger.print_info ("initializing..")

        self.logger.print_info (" - reading input from %s" % self.input_folder)

        from .analysis_helpers import init_input_for_analysis
        if init_input_for_analysis ( analysis = self):
            self.logger.print_info ("   .. done")
        else:
            self.logger.print_error ("Failed reading the input files: EXIT")
            exit (1)

        self.logger.print_info (" - reading history from %s" % self.input_folder)
        from .analysis_helpers import init_history_for_analysis
        if init_history_for_analysis ( analysis = self):
            self.logger.print_info ("   .. done")
        else:
            self.logger.print_error ("Failed reading the history files: EXIT")
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
        
        from .analysis_helpers import get_array_from_series 
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
        from .analysis_helpers import encode_position
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
        
        
        self.logger.print_debug ("   prediction & target vs events")
        all_data = {} 
        all_data ['prediction'] = np.concatenate ([ self.df['X_test_%d' % imod].sort_values( by = 'target') ['prediction'] for imod in range (n_models) ])
        all_data ['target'] = np.concatenate ([ self.df['X_test_%d' % imod].sort_values( by = 'target') ['target'] for imod in range (n_models) ])
        all_data ['index'] = np.concatenate ([ self.df['X_test_%d' % imod].sort_values( by = 'target').index for imod in range (n_models) ])
        all_data ['fake_index'] = np.arange ( all_data ['target'].size )
        self.plots ['test_pred_and_tar_per_event'] = compare_prediction_and_target (
            y1 = all_data ['target'],
            y2 = all_data ['prediction'],
            x = all_data ['fake_index'],
            xaxislabel = 'Raw player index', yaxislabel = 'Vote',
            ylim = [3,10],
            y1label = 'Measured', y2label = 'Predicted',
            decos = ['Test dataset']
        )


        for pos in ['G', 'D', 'M', 'F']:
            self.logger.print_debug ("     > Position: %s "% pos)
            all_data = {} 
            all_data ['prediction'] = np.concatenate ([ self.df['X_test_%d' % imod].loc [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ].sort_values( by = 'target') ['prediction'] for imod in range (n_models) ])
            all_data ['target'] = np.concatenate ([ self.df['X_test_%d' % imod].loc [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ].sort_values( by = 'target') ['target'] for imod in range (n_models) ])
            all_data ['index'] = np.concatenate ([ self.df['X_test_%d' % imod].loc [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ].sort_values( by = 'target').index for imod in range (n_models) ])
            all_data ['fake_index'] = np.arange ( all_data ['target'].size )
            self.plots ['test_pred_and_tar_per_event__%s' % pos] = compare_prediction_and_target (
                y1 = all_data ['target'],
                y2 = all_data ['prediction'],
                x = all_data ['fake_index'],
                xaxislabel = 'Raw player index', yaxislabel = 'Vote',
                ylim = [3,10],
                y1label = 'Measured', y2label = 'Predicted',
                decos = ['Test dataset', 'Position: %s' % pos]
        )


        self.logger.print_debug ("   votes distribution (meas. vs. pred.)")
        
        
        self.plots ['test_votes_hist_pred_and_tar'] = hist_per_classes (
            df = pd.concat ( [ self.df['X_test_%d' % imod] for imod in range (n_models) ] ),
            classification = 'pred_vs_meas',
            xlim = [3,10],
            integer = False,
            xaxislabel = 'Voto',
            yaxislabel = 'Fraction of players'
        )
        


        '''
         Loss convergence plot
        '''
        self.plots ['loss_convergence'] = plot_loss (
            histories = self.histories
        )


        '''
         Feature importance plot
        '''
        self.plots ['permutation_ranking'] = plot_permutation_feature_importance (
            models = self.model,
            data = self.df
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
