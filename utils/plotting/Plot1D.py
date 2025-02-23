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

class Plot1D:

    _output_folder = "./data/"
    _base_selection = "SELECT * from player_stats"
    
    def __init__ (self, config, db):
        self.config = config
        self.db = db
        self.init ()

    def init (self):
        self.name = self.config["name"] if "name" in self.config.keys() else "NONE"
        self.variable = self.config["variable"] if "variable" in self.config.keys() else "NONE"
        self.selection = self._base_selection
        self.selection += " WHERE " + self.config["selection"] if "selection" in self.config.keys() else str()
        try:
            self.df = pd.read_sql(self.selection, self.db._cnx)
        except:
            logging.error ("[ERROR] Query `%s` not valid: fallback to inclusive selection" % self.selection)
            self.selection = self._base_selection
            self.df = pd.read_sql(self.selection, self.db._cnx)

    def setup_bins (self):
        if "bins" in self.config.keys():
            return self.config["bins"]

        min_value = self.df [ self.variable ].min( axis = 0,
                                                   skip_na = True,
                                                   numeric_only = True)
        max_value = self.df [ self.variable ].max( axis = 0,
                                                   skip_na = True,
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
        
    def plot (self, label):
        logging.info ("[1D] Plotting %s [#events = %d]" % (self.name, len(self.df.index)))
        bins = self.setup_bins ()
        self.fig, self.ax = plt.subplots()
        self.df.hist (column = self.variable,
                      bins = bins,
                      ax = self.ax,
                      grid=False, density=1)
        self.ax.set_xlabel (self.name)
        self.ax.set_ylabel ('Density [1/N]')
        self.ax.set_title (str())
        plt.tight_layout()
        self.write (label)
        
