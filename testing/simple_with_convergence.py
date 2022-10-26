#!/usr/bin/env python

from .plot_helpers import correlation_plot, residual_vs_var_plot, compare_prediction_and_target, hist_per_classes
from .analysis_helpers import shape_df_for_predicting
from utils.myprint import myprint
import pandas as pd
import numpy as np
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error


class simple_with_convergence ():

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
        

        self.logger.print_debug ("   loss convergence")

        '''
        let's implement it here at the moment
        '''
        imodel=0
        params = {}
        params [imodel] = self.model ['model_%d' % imodel].get_params ()
        test_score = np.zeros((params [imodel] ["n_estimators"],), dtype=np.float64)
        self.model ['model_%d' % imodel].staged_predict
        for i, y_pred in enumerate(self.model ['model_%d' % imodel].staged_predict( shape_df_for_predicting (self.df['X_test_0']))):
            
            test_score[i] = self.model ['model_%d' % imodel].loss_(np.ravel(self.df['y_test_0']), y_pred)

        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(6, 6))
        plt.subplot(1, 1, 1)
        plt.plot(
            np.arange(params[imodel]["n_estimators"]) + 1,
            self.model ['model_%d' % imodel].train_score_,
            "b-",
            label="Training Set Deviance",
        )
        plt.plot(
            np.arange(params[imodel]["n_estimators"]) + 1, test_score, "r-", label="Test Set Deviance"
        )
        plt.legend(loc="upper right")
        plt.xlabel("Boosting Iterations")
        plt.ylabel("Deviance")
        fig.tight_layout()
        self.plots ['test_loss_evolution'] = fig

        '''
        let's implement it here at the moment
        '''
        self.logger.print_debug ("   feature ranking (MDI)")
        curr_model = self.model ['model_%d' % imodel]
        
        feature_importance = curr_model.feature_importances_
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + 0.5
        fig = plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.barh(pos, feature_importance[sorted_idx], align="center")
        plt.yticks(pos, np.array(self.df['X_test_0'].columns.tolist())[sorted_idx])
        plt.title("Feature Importance (MDI)")


        self.logger.print_debug ("   feature ranking (permutation)")
        result = permutation_importance(
            curr_model,
            shape_df_for_predicting (self.df['X_test_0']),
            self.df['y_test_0'],
            n_repeats=10, random_state=42, n_jobs=2
        )
        sorted_idx = result.importances_mean.argsort()
        plt.subplot(1, 2, 2)
        plt.boxplot(
            result.importances[sorted_idx].T,
            vert=False,
            labels=np.array(self.df['X_test_0'].columns.tolist())[sorted_idx],
        )
        plt.title("Permutation Importance (test set)")
        fig.tight_layout()
        self.plots ['test_feature_importance'] = fig


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
