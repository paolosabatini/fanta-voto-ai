#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.json.JsonHelper import get_dict_from_json_file
from utils.plotting.Plot1D import Plot1D
from utils.plotting.Plot2D import Plot2D
from utils.db.DbPlayerStats import DbPlayerStats

class PlotManager:

    def __init__ (self, path_to_config_file, label):
        
        self.config_file = path_to_config_file
        self.config = get_dict_from_json_file (self.config_file)
        self.label = label
        self.db = DbPlayerStats()
        self.init()

        
    def init(self):
        self.init_1d()
        self.init_2d()

    def init_1d(self):
        list_of_1d_plot_config = list(self.config ["1D"] if "1D" in self.config.keys() else None)
        if list_of_1d_plot_config == None:
            logging.warning ("[WARNING] No 1D plot in the passed configuration")
            return
        logging.info ("N. 1D plots:\t%d" % len (list_of_1d_plot_config))
        self.plots_1d = [ Plot1D (config, self.db) for config in list_of_1d_plot_config ]

    def init_2d(self):
        list_of_2d_plot_config = list(self.config ["2D"] if "2D" in self.config.keys() else None)
        if list_of_2d_plot_config == None:
            logging.warning ("[WARNING] No 2D plot in the passed configuration")
            return
        logging.info ("N. 2D plots:\t%d" % len (list_of_2d_plot_config))
        self.plots_2d = [ Plot2D (config, self.db) for config in list_of_2d_plot_config ]
        
    def plot (self):
        [ p.plot (self.label) for p in self.plots_1d ]
        [ p.plot (self.label) for p in self.plots_2d ]
