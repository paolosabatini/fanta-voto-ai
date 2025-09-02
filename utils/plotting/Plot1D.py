#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.json.JsonHelper import get_dict_from_json_file
import pandas as pd
import matplotlib.pyplot as plt
from utils.system.SystemHelper import check_and_create_folder
from utils.plotting.PlotStyles import get_style

class Plot1D:

    _output_folder = "./data/"
    _base_selection = "SELECT * from player_stats"
    
    def __init__ (self, config, df):
        self.config = config
        self.df = df
        self.init ()

    def init (self):
        self.name = self.config["name"] if "name" in self.config.keys() else "NONE"
        self.variable = self.config["variable"] if "variable" in self.config.keys() else "NONE"
        self.selection = self._base_selection
        self.selection += " WHERE " + self.config["selection"] if "selection" in self.config.keys() else str()
        self.group_by = self.config["group_by"] if "group_by" in self.config.keys() else dict()
        

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
        self.fig.savefig(outfile_name)

    def draw (self, bins):
        plt.rcParams["image.cmap"] = "Pastel2"
        if len (self.group_by.keys()) == 0:
            self.draw_single(bins)
        else:
            self.draw_multiple(bins)


    def draw_single (self, bins):
        self.df.hist (column = self.variable,
                      bins = bins,
                      ax = self.ax,
                      grid=False, density=1)

    def draw_multiple (self, bins):
        igroup = 0
        for group_name, group_selection in self.group_by.items():
            self.df [ eval (group_selection) ].hist(column = self.variable,
                                                    bins = bins,
                                                    ax = self.ax,
                                                    grid=False, density=1,
                                                    label = group_name,
                                                    **get_style (igroup))
            igroup += 1
        plt.legend(loc='upper right')
            
            
    def plot (self, label):
        logging.info ("[1D] Plotting %s [#events = %d]" % (self.name, len(self.df.index)))
        bins = self.setup_bins ()
        self.fig, self.ax = plt.subplots()
        self.draw( bins )
        self.ax.set_xlabel (self.xtitle if self.xtitle != None else self.name)
        self.ax.set_ylabel ('Density [1/N]')
        self.ax.set_title (str())
        plt.tight_layout()
        self.write (label)
        
