#!/usr/bin/env python

from plot_helpers import box_vs_var_plot, correlation_plot, scat_plot_diff_classes, hist_per_classes
from analysis_helpers import encode_position
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

        self.logger.print_info (" - reading input DF from %s" % self.input_folder)

        from analysis_helpers import init_input_for_df_analysis
        if init_input_for_df_analysis ( analysis = self):
            self.logger.print_info ("   .. done")
        else:
            self.logger.print_error ("Failed reading the input files: EXIT")
            exit (1)


    def execute (self):


        self.logger.print_info ("starting analysis..")
        
        self.positions = ['G', 'D', 'M', 'F']
        # vote vs. position
        self.logger.print_debug ("   votes vs. position")

        votes_per_position = []
        for pos in self.positions:
            votes_per_position.append (
                self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position(pos) ] ['Punteggio'] 
            )

        self.plots ['votes_vs_role'] = box_vs_var_plot (
            data = votes_per_position, labels =  ['G', 'D', 'M', 'F'],
            xlabel = 'Position', ylabel = 'Vote',
            ylim = [2,12],
            decos = ["All data"]
            
        )

        
        
        # vote vs. goal
        self.logger.print_debug ("   votes vs. goals \t (split by position)")
        
        votes_vs_goal_per_pos = []
        for pos in  self.positions:
            votes_vs_goal_per_pos.append (
                self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position(pos) ] [['Punteggio','Goal']] )
           
        self.plots ['votes_vs_goal_per_pos'] = scat_plot_diff_classes ( votes_vs_goal_per_pos,
                                                                        self.positions,
                                                                        xlabel = 'Goal',
                                                                        ylabel = 'Punteggio',
                                                                        xaxislabel = 'Goal',
                                                                        yaxislabel = 'Vote',
                                                                        xlim = [-0.5,+5.5], ylim = [0,10],
                                                                        do_legend = False)

        # # goalkeeper variable study
        # self.input_variables_for_goalkeeper ()

        # # defender variable study
        # self.input_variables_for_defender ()

        # midfielder variable study
        # self.input_variables_for_midfielder ()

        # # forward variable study
        self.input_variables_for_forward ()

        # general 1D distributions
        # self.input_variables_unidimentional ()


    def input_variables_unidimentional (self):
        '''
         Distribution 1D 
        '''

        from utils.converter import convert_to_axis_label
        
        nbins = 15
        distributions_players = ["Autogoal", "Goal", "Tiri", "Falli_commessi",
		                 "Tiri_in_porta", "Falli_subiti", "Fuorigioco", "Cartellini_gialli", "Cartellini_rossi"]
        distributions_teams = [  "goal_taken", "goal_scored", "this_goals_per90", "opponent_goals_per90",
		                 "this_assists_per90", "opponent_assists_per90", "this_goals_pens_per90",
		                 "opponent_goals_pens_per90", "total_shots_made", "total_shots_taken",
		                 "total_fouls_made", "total_fouls_taken" ]

        for d in distributions_players:
            integer = (d not in ['Minuti_giocati'])
            xlabel = convert_to_axis_label (d)
            self.plots ['hist_%s_per_pos' % d] = hist_per_classes (
                df = self.df['X'],
                classification = 'position',
                variable = d,
                nbins = 20,
                integer = integer,
                xaxislabel = xlabel,
                yaxislabel = 'Fraction of players'
            )

        for d in distributions_teams:
            
            xlabel = convert_to_axis_label (d)
            self.plots ['hist_%s_per_pos' % d] = hist_per_classes (
                df = self.df['X'],
                classification = None,
                variable = d,
                nbins = 10,
                integer = False,
                xaxislabel = xlabel,
                yaxislabel = 'Fraction of players'
            )


    def input_variables_for_forward (self):
        '''
         Forward sensitive  variables
        '''

        # vote vs. goal/shots (F)
        self.logger.print_debug ("   votes vs. goal/shots \t (A)")
        self.df['X']['eff_goal'] = self.df['X']['Goal'] / self.df['X']['Tiri']
        self.df['X']['shot_frac'] = self.df['X']['Tiri'] / self.df['X']['total_shots_made']
        shots_class = 12
        votes_vs_goal_eff_A = [
            
            # self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) & (self.df['X']['shot_frac'] < 0.5) ] [['Punteggio','eff_goal']].sort_values (by = 'eff_goal'),
            # self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) & (self.df['X']['shot_frac'] > 0.5) ] [['Punteggio','eff_goal']].sort_values (by = 'eff_goal')
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) & (self.df['X']['total_shots_made'] < shots_class) ] [['Punteggio','eff_goal']].sort_values (by = 'eff_goal'),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) & (self.df['X']['total_shots_made'] >= shots_class) ] [['Punteggio','eff_goal']].sort_values (by = 'eff_goal')
        ]

        self.plots ['votes_vs_goal_eff_A'] = scat_plot_diff_classes ( votes_vs_goal_eff_A,
                                                                      ['Total shots < %d' % shots_class, 'Total shots $\geq$ %d' % shots_class],
                                                                      # ['< 50% of total shots', '> 50% of total shots' ],
                                                                      xlabel = 'eff_goal',
                                                                      ylabel = 'Punteggio',
                                                                      xaxislabel = 'Goals scored / Shots',
                                                                      yaxislabel = 'Vote',
                                                                      xlim = [-0.2,1.2], ylim = [2.5,10],
                                                                      do_legend = True)
        

    def input_variables_for_midfielder (self):
        '''
         Midfielder sensitive  variables
        '''

                
        # vote vs. goal taken - opponent_goal_per90 (M)
        self.logger.print_debug ("   votes vs. goals taken - opponent_goal_per90 \t (M)")
        votes_vs_goal_taken_sub_opponent_goals_avg_M = []
        self.df['X'] ['goal_wrt_average_opponent'] = self.df['X'] ['goal_taken'] - self.df['X'] ['opponent_goals_per90']
        votes_vs_goal_taken_sub_opponent_goals_avg_M = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('M')) & (self.df['X']['opponent_goals_per90']>1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent") ,
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('M')) & (self.df['X']['opponent_goals_per90']<1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent")
        ]
        
        self.plots ['votes_vs_goal_wrt_avg_opponent_M'] = scat_plot_diff_classes ( votes_vs_goal_taken_sub_opponent_goals_avg_M,
                                                                                   ['> 1 goal exp.', '< 1 goal exp.'],
                                                                                   xlabel = 'goal_wrt_average_opponent',
                                                                                   ylabel = 'Punteggio',
                                                                                   xaxislabel = 'Goals taken - Avg. opponent goals',
                                                                                   yaxislabel = 'Vote',
                                                                                   xlim = [-2.5,2.5], ylim = [2,10],
                                                                                   decos = ['Dataset: Midfielder'],
                                                                                   do_fit = False,
                                                                                   do_legend = True)

        # vote vs. goal (M, F)
        self.logger.print_debug ("   votes vs. goal \t (M,A)")
        votes_vs_goal_MF = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('M')) ] [['Punteggio','Goal']].sort_values (by = 'Goal'),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) ] [['Punteggio','Goal']].sort_values (by = 'Goal')
        ]
        
        self.plots ['votes_vs_goal_MF'] = scat_plot_diff_classes ( votes_vs_goal_MF,
                                                                   ['Midfieler', 'Forward'],
                                                                   xlabel = 'Goal',
                                                                   ylabel = 'Punteggio',
                                                                   xaxislabel = 'Goals scored',
                                                                   yaxislabel = 'Vote',
                                                                   xlim = [-0.5,+3.5], ylim = [2.5,10],
                                                                   do_legend = True)

        # vote vs. shots (M, F)
        self.logger.print_debug ("   votes vs. shots \t (M,A)")
        votes_vs_shots_MF = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('M')) ] [['Punteggio','Tiri']].sort_values (by = 'Tiri'),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('F')) ] [['Punteggio','Tiri']].sort_values (by = 'Tiri')
        ]
        
        self.plots ['votes_vs_shots_MF'] = scat_plot_diff_classes ( votes_vs_shots_MF,
                                                                    ['Midfieler', 'Forward'],
                                                                    xlabel = 'Tiri',
                                                                    ylabel = 'Punteggio',
                                                                    xaxislabel = 'Shots',
                                                                    yaxislabel = 'Vote',
                                                                    xlim = [-0.5,+5.5], ylim = [2.5,10],
                                                                    do_legend = True)

        
        
        

    def input_variables_for_defender (self):
            
        '''
         Defender sensitive  variables
        '''
        
        
        # vote vs. goal taken - opponent_goal_per90 (P)
        self.logger.print_debug ("   votes vs. goals taken - opponent_goal_per90 \t (D)")
        votes_vs_goal_taken_sub_opponent_goals_avg_D = []
        self.df['X'] ['goal_wrt_average_opponent'] = self.df['X'] ['goal_taken'] - self.df['X'] ['opponent_goals_per90']
        votes_vs_goal_taken_sub_opponent_goals_avg_D = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & (self.df['X']['opponent_goals_per90']>1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent") ,
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & (self.df['X']['opponent_goals_per90']<1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent")
        ]
        
        self.plots ['votes_vs_goal_wrt_avg_opponent_D'] = scat_plot_diff_classes ( votes_vs_goal_taken_sub_opponent_goals_avg_D,
                                                                                   ['> 1 goal exp.', '< 1 goal exp.'],
                                                                                   xlabel = 'goal_wrt_average_opponent',
                                                                                   ylabel = 'Punteggio',
                                                                                   xaxislabel = 'Goals taken - Avg. opponent goals',
                                                                                   yaxislabel = 'Vote',
                                                                                   xlim = [-2.5,2.5], ylim = [2,10],
                                                                                   decos = ['Dataset: Defenders'],
                                                                                   do_fit = False,
                                                                                   do_legend = True)
        

        # vote vs. shots  taken (D)
        self.logger.print_debug ("   votes vs. shots  aken \t (D)")
        self.df['X']['eff_shots_on_target'] = self.df['X']['total_shots_on_target_taken'] / self.df['X']['total_shots_taken']
        votes_vs_shots_taken_D = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & (self.df['X']['eff_shots_on_target'] < 0.2)] [['Punteggio','total_shots_taken']].sort_values (by = "total_shots_taken"),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & ((self.df['X']['eff_shots_on_target'] > 0.2) & (self.df['X']['eff_shots_on_target'] < 0.5))] [['Punteggio','total_shots_taken']].sort_values (by = "total_shots_taken"),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & ((self.df['X']['eff_shots_on_target'] > 0.5) & (self.df['X']['eff_shots_on_target'] < 0.7))] [['Punteggio','total_shots_taken']].sort_values (by = "total_shots_taken"),
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('D')) & (self.df['X']['eff_shots_on_target'] > 0.7) ] [['Punteggio','total_shots_taken']].sort_values (by = "total_shots_taken")
            
        ]
        labels = [r'$\epsilon_{oT}$ < 0.2', r'0.2 < $\epsilon_{oT}$ < 0.5', r'0.5 < $\epsilon_{oT}$ < 0.7', r'$\epsilon_{oT}$ > 0.7']
        self.plots ['votes_vs_shots_taken_D'] = scat_plot_diff_classes ( votes_vs_shots_taken_D,
                                                                         labels,
                                                                         xlabel = 'total_shots_taken',
                                                                         ylabel = 'Punteggio',
                                                                         xaxislabel = 'Shots taken',
                                                                         yaxislabel = 'Vote',
                                                                         xlim = [-0.5,20], ylim = [2,11],
                                                                         decos = ['Dataset: Defenders'],
                                                                         do_fit = False,
                                                                         do_legend = True)
        


        
    def input_variables_for_goalkeeper (self):
        
        '''
         Goalkeeper sensitive  variables
        '''
        
        
        # vote vs. goal taken (P)
        self.logger.print_debug ("   votes vs. goals taken \t (P)")
        votes_vs_goal_taken_P = []
        votes_vs_goal_taken_P.append (
            self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position('P') ] [['Punteggio','goal_taken']].sort_values (by = "goal_taken") )
        
        self.plots ['votes_vs_goals_taken_P'] = scat_plot_diff_classes ( votes_vs_goal_taken_P,
                                                                         self.positions,
                                                                         xlabel = 'goal_taken',
                                                                         ylabel = 'Punteggio',
                                                                         xaxislabel = 'Goals taken',
                                                                         yaxislabel = 'Vote',
                                                                         xlim = [-0.5,+5.5], ylim = [2,10],
                                                                         decos = ['Dataset: Goalkeepers'],
                                                                         do_fit = True,
                                                                         do_legend = False)
        
        
        # vote vs. shots taken (P)
        self.logger.print_debug ("   votes vs. shots taken \t (P)")
        votes_vs_shot_taken_P = []
        votes_vs_shot_taken_P.append (
            self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position('P') ] [['Punteggio','total_shots_taken']].sort_values (by = "total_shots_taken") )
        
        self.plots ['votes_vs_shots_taken_P'] = scat_plot_diff_classes ( votes_vs_shot_taken_P,
                                                                         self.positions,
                                                                         xlabel = 'total_shots_taken',
                                                                         ylabel = 'Punteggio',
                                                                         xaxislabel = 'Shots taken',
                                                                         yaxislabel = 'Vote',
                                                                         xlim = [-0.5,20], ylim = [2,10],
                                                                         decos = ['Dataset: Goalkeepers'],
                                                                         do_fit = True,
                                                                         do_legend = False)
        
        # vote vs. shots on target taken (P)
        self.logger.print_debug ("   votes vs. shots on target taken \t (P)")
        votes_vs_shot_on_target_taken_P = []
        votes_vs_shot_on_target_taken_P.append (
            self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position('P') ] [['Punteggio','total_shots_on_target_taken']].sort_values (by = "total_shots_on_target_taken") )
        
        self.plots ['votes_vs_shots_on_target_taken_P'] = scat_plot_diff_classes ( votes_vs_shot_on_target_taken_P,
                                                                                   self.positions,
                                                                                   xlabel = 'total_shots_on_target_taken',
                                                                                   ylabel = 'Punteggio',
                                                                                   xaxislabel = 'Shots on target taken',
                                                                                   yaxislabel = 'Vote',
                                                                                   xlim = [-0.5,20], ylim = [2,10],
                                                                                   decos = ['Dataset: Goalkeepers'],
                                                                                   do_fit = True,
                                                                                   do_legend = False)
        
        
        
        # vote vs. goal taken / shot_on_target_taken (P)
        self.logger.print_debug ("   votes vs. goals taken / shot_on_target_taken \t (P)")
        votes_vs_goal_taken_o_shots_on_target_P = []
        self.df['X'] ['goal_over_shots_on_target'] = self.df['X'] ['goal_taken'] / self.df['X'] ['total_shots_on_target_taken']
        votes_vs_goal_taken_o_shots_on_target_P.append (
            
            self.df['X'].loc [ self.df['X']['Ruolo'] == encode_position('P') ] [['Punteggio','goal_over_shots_on_target']].sort_values (by = "goal_over_shots_on_target") )
        
        self.plots ['votes_vs_goal_over_shots_on_target_P'] = scat_plot_diff_classes ( votes_vs_goal_taken_o_shots_on_target_P,
                                                                                       self.positions,
                                                                                       xlabel = 'goal_over_shots_on_target',
                                                                                       ylabel = 'Punteggio',
                                                                                       xaxislabel = 'Goals / Shot on target taken',
                                                                                       yaxislabel = 'Vote',
                                                                                       xlim = [-0.2,1.2], ylim = [2,10],
                                                                                       decos = ['Dataset: Goalkeepers'],
                                                                                       do_fit = False,
                                                                                       do_legend = False)

        # vote vs. goal taken / shot_on_target_taken (P)
        self.logger.print_debug ("   votes vs. goals taken / shot_on_target_taken \t (P)")
        votes_vs_goal_taken_o_shots_on_target_P = [
            
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('P')) & (self.df['X'] ['total_shots_on_target_taken']<6) ] [['Punteggio','goal_over_shots_on_target']].sort_values (by = "goal_over_shots_on_target") ,
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('P')) & (self.df['X'] ['total_shots_on_target_taken']>=6) ] [['Punteggio','goal_over_shots_on_target']].sort_values (by = "goal_over_shots_on_target") 
        ]
        self.plots ['votes_vs_goal_over_shots_on_target_2_P'] = scat_plot_diff_classes ( votes_vs_goal_taken_o_shots_on_target_P,
                                                                                       [r'Shots on target $\leq$ 5',r'Shots on target > 5'],
                                                                                       xlabel = 'goal_over_shots_on_target',
                                                                                       ylabel = 'Punteggio',
                                                                                       xaxislabel = 'Goals / Shot on target taken',
                                                                                       yaxislabel = 'Vote',
                                                                                       xlim = [-0.2,1.2], ylim = [2,10],
                                                                                       decos = ['Dataset: Goalkeepers'],
                                                                                       do_fit = False,
                                                                                        do_legend = True)

        # vote vs. goal taken - opponent_goal_per90 (P)
        self.logger.print_debug ("   votes vs. goals taken - opponent_goal_per90 \t (P)")
        votes_vs_goal_taken_sub_opponent_goals_avg_P = []
        self.df['X'] ['goal_wrt_average_opponent'] = self.df['X'] ['goal_taken'] - self.df['X'] ['opponent_goals_per90']
        votes_vs_goal_taken_sub_opponent_goals_avg_P = [
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('P')) & (self.df['X']['opponent_goals_per90']>1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent") ,
            self.df['X'].loc [ (self.df['X']['Ruolo'] == encode_position('P')) & (self.df['X']['opponent_goals_per90']<1.)] [['Punteggio','goal_wrt_average_opponent']].sort_values (by = "goal_wrt_average_opponent")
        ]
        
        self.plots ['votes_vs_goal_wrt_avg_opponent_P'] = scat_plot_diff_classes ( votes_vs_goal_taken_sub_opponent_goals_avg_P,
                                                                                   ['> 1 goal exp.', '< 1 goal exp.'],
                                                                                   xlabel = 'goal_wrt_average_opponent',
                                                                                   ylabel = 'Punteggio',
                                                                                   xaxislabel = 'Goals taken - Avg. opponent goals',
                                                                                   yaxislabel = 'Vote',
                                                                                   xlim = [-2.5,2.5], ylim = [2,10],
                                                                                   decos = ['Dataset: Goalkeepers'],
                                                                                   do_fit = False,
                                                                                   do_legend = True)
                


        
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
