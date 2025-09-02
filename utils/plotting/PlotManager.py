#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.json.JsonHelper import get_dict_from_json_file
from utils.plotting.Plotly1D import Plotly1D
from utils.plotting.Plot2D import Plot2D
import pandas as pd

class PlotManager:

    def __init__ (self, path_to_config_file, label, input_filename):
        
        self.config_file = path_to_config_file
        self.input_filename = input_filename
        self.config = get_dict_from_json_file (self.config_file)
        self.label = label
        self.init()

        
    def init(self):
        self.init_df()
        self.init_1d()
        self.init_2d()

    def init_df(self):
        self.df = pd.read_parquet(self.input_filename)
        
    def init_1d(self):
        list_of_1d_plot_config = list(self.config ["1D"] if "1D" in self.config.keys() else [])
        if list_of_1d_plot_config == None:
            logging.warning ("[WARNING] No 1D plot in the passed configuration")
            self.plots_1d = []
            return
        logging.info ("N. 1D plots:\t%d" % len (list_of_1d_plot_config))
        self.plots_1d = [ Plotly1D (config, self.df) for config in list_of_1d_plot_config ]

    def init_2d(self):
        list_of_2d_plot_config = list(self.config ["2D"] if "2D" in self.config.keys() else [])
        if list_of_2d_plot_config == None:
            logging.warning ("[WARNING] No 2D plot in the passed configuration")
            self.plots_2d = []
            return
        logging.info ("N. 2D plots:\t%d" % len (list_of_2d_plot_config))
        self.plots_2d = [ Plot2D (config,self.df) for config in list_of_2d_plot_config ]

        
    def plot (self):
        [ p.plot (self.label) for p in self.plots_1d ]
        [ p.plot (self.label) for p in self.plots_2d ]
