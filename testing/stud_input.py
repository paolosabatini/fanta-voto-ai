#!/usr/bin/env python

from plot_helpers import residual_vs_var_plot, correlation_plot, scat_plot_diff_classes
from utils.myprint import myprint
import pandas as pd
import numpy as np


class stud_input ():

    plots = {}
    
    def __init__ (self, debug, input_folder):
        self.debug = debug
        self.input_folder = input_folder
        self.init()
        
    
    def init (self):
        self.logger = myprint ("stud_input   ", self.debug)
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
            
    
    def execute (self):
        from analysis_helpers import encode_position
        
        self.logger.print_info ("starting analysis..")
        arrays = {}

        self.logger.print_debug ("   augmenting variables in the df")
        self.augment_df ()

        n_models =  len (self.model.keys())
        positions = ['G', 'D', 'M', 'F']
        # vote vs. position
        self.logger.print_debug ("   votes vs. position")

        all_data = []
        for pos in  positions:
            all_data.append (
                np.concatenate ([ self.df['X_test_%d' % imod].loc [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ] ['target'] for imod in range (n_models) ])
            )

        self.plots ['vote_vs_role'] = residual_vs_var_plot (
            data = all_data, labels = positions,
            xlabel = 'Position', ylabel = 'Vote',
            ylim = [4,10],
            decos = ["All dataset"]
            
        )

        
        # # vote vs. goal
        # self.logger.print_debug ("   votes vs. goals \t (split by position)")
        # positions =  ['G', 'D', 'M', 'F']
        # votes_vs_goal_per_pos = []
        # for pos in positions:
        #     votes_vs_goal_per_pos.append (
        #         pd.concat ( [ self.df ['X_test_%d' % imod] [ self.df['X_test_%d' % imod]['Ruolo'] == encode_position(pos) ] for imod in range(n_models) ] )
        #     )
        # self.plots ['votes_vs_goal_per_pos'] = scat_plot_diff_classes ( votes_vs_goal_per_pos, positions, xlabel = 'Goal', ylabel = 'target',
        #                                                                 xaxislabel = 'Goals', yaxislabel = 'Vote',
        #                                                                 xlim = [-3,+5], ylim = [0,10])

        # print votes_vs_goal_per_pos [-1]





        
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
