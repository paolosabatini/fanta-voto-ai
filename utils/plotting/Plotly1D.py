#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.json.JsonHelper import get_dict_from_json_file
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
from utils.system.SystemHelper import check_and_create_folder
from utils.plotting.PlotStyles import get_style
import utils.plotting.PlotConfig as pconf

class Plotly1D:

    _output_folder = "./data/plots/"
    
    def __init__ (self, config, df):
        self.config = config
        self.init ()
        self.df = df

    def init (self):
        self.name = self.config["name"] if "name" in self.config.keys() else "NONE"
        self.selection = self.config["selection"] if "selection" in self.config.keys() else "NONE"
        self.variable = self.config["variable"] if "variable" in self.config.keys() else "NONE"
        self.group_by = self.config["group_by"] if "group_by" in self.config.keys() else dict()
        self.xtitle = self.config["xtitle"] if "xtitle" in self.config.keys() else self.name
    def setup_bins (self):
        if "bins" in self.config.keys():
            return self.config["bins"]

        min_value = self.df [ self.variable ].min( axis = 0,
                                                   numeric_only = True)
        max_value = self.df [ self.variable ].max( axis = 0,
                                                   numeric_only = True)
        n_entries = len(self.df.index)
        n_bins = int ( float (n_entries)**0.5 )
        bin_size = float(max_value - min_value) / n_bins
        
        return [min_value+i*bin_size for i in range (n_bins+1)]


    def write (self, label):
        output_folder = self._output_folder + label
        check_and_create_folder (output_folder)
        outfile_name =  output_folder + "/" + self.name + ".png"
        self.fig.write_image(outfile_name)

    def draw (self, bins):

        if len (self.group_by.keys()) == 0:
            self.draw_single(bins)
        else:
            self.draw_multiple(bins)

    def select(self):
        selected_df =self.df.query(self.selection) if self.selection != "NONE" else self.df
        logging.info ("[1D] > [#events = %d]" % ( len(selected_df.index)))
        return selected_df
        
    def draw_single (self, bins):
        base_selected_data=self.select()
        self.draw_fig (base_selected_data,bins, 0)

    def draw_multiple (self, bins):
        igroup = 0
        base_selected_data=self.select()
        for group_name, group_selection in self.group_by.items():
            
            data = base_selected_data.query(group_selection) [ self.variable ]
            logging.warning("[1D]\t> Group %s has %d events" % (group_name, len(data.index)))
            self.draw_fig ( data, bins, igroup, group_name)
            igroup += 1 

    def draw_fig (self,data, bins,  style_id, label = str()):
        num_samples = len( self.df[ self.variable ].index )
        hist_data, bin_edges = np.histogram(data, bins=bins, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        uncertainties = np.sqrt(hist_data / num_samples)

        # Add line histogram
        self.fig.add_trace(go.Scatter(
            x=bin_centers,
            y=hist_data,
            mode='lines',
            line=dict(color=pconf._LINE_COLORS_[style_id], width=2, dash=pconf._LINE_STYLES_[style_id]),
            name=label if label != str() else self.variable,
            showlegend=(label != str())
        ))

        # Add filled uncertainty region
        self.fig.add_trace(go.Scatter(
            x=np.concatenate([bin_centers, bin_centers[::-1]]),
            y=np.concatenate([hist_data - uncertainties, (hist_data + uncertainties)[::-1]]),
            fill='toself',
            fillcolor=pconf._FILL_COLORS_[style_id],
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False,
        ))
            
    def plot (self, label):
        logging.info ("[1D] Plotting %s" % (self.name))
        bins = self.setup_bins ()
        self.fig = go.Figure()
        self.draw( bins )
        self.fig.update_layout (
            xaxis_title=self.xtitle,
            yaxis_title='Density [1/N]',
            template='plotly_white'
        )
        
        self.write (label)
        
