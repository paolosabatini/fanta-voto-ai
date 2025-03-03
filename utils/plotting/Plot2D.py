#!/usr/bin/env python3A

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.json.JsonHelper import get_dict_from_json_file
import pandas as pd
import matplotlib.pyplot as plt
from utils.system.SystemHelper import check_and_create_folder
from utils.plotting.PlotStyles import get_marker, get_color

class Plot2D:

    _output_folder = "./data/"
    _base_selection = "SELECT * from player_stats"
    
    def __init__ (self, config, db):
        self.config = config
        self.db = db
        self.init ()

    def init (self):
        self.name = self.config["name"] if "name" in self.config.keys() else "NONE"
        self.variable_x = self.config["variable_x"] if "variable_x" in self.config.keys() else "NONE"
        self.variable_y = self.config["variable_y"] if "variable_y" in self.config.keys() else "NONE"
        self.selection = self._base_selection
        self.selection += " WHERE " + self.config["selection"] if "selection" in self.config.keys() else str()
        self.group_by = self.config["group_by"] if "group_by" in self.config.keys() else dict()
        try:
            self.df = pd.read_sql(self.selection, self.db._cnx)
        except:
            logging.error ("[ERROR] Query `%s` not valid: fallback to inclusive selection" % self.selection)
            self.selection = self._base_selection
            self.df = pd.read_sql(self.selection, self.db._cnx)


    def write (self, label):
        output_folder = self._output_folder + label
        check_and_create_folder (output_folder)
        outfile_name =  output_folder + "/" + self.name + ".png"
        self.fig.savefig(outfile_name)

    def draw (self):
        plt.rcParams["image.cmap"] = "Pastel2"
        if len (self.group_by.keys()) == 0:
            self.draw_single()
        else:
            self.draw_multiple()


    def draw_single (self):
        self.df.hist (x = self.variable_x,
                      y = self.variable_y,
                      ax = self.ax,
                      grid=True,
                      label = group_name,
                      marker = get_marker (0))

    def draw_multiple (self):
        igroup = 0
        for group_name, group_selection in self.group_by.items():
            self.df [ eval (group_selection) ].plot.scatter(x = self.variable_x,
                                                            y = self.variable_y,
                                                            ax = self.ax,
                                                            grid=True,
                                                            label = group_name,
                                                            marker = get_marker (igroup),
                                                            color = get_color (igroup))
            igroup += 1
        plt.legend(loc='upper right')
            
            
    def plot (self, label):
        logging.info ("[1D] Plotting %s [#events = %d]" % (self.name, len(self.df.index)))
        self.fig, self.ax = plt.subplots()
        self.draw(  )
        self.ax.set_xlabel (self.variable_x)
        self.ax.set_ylabel (self.variable_y)
        self.ax.set_title (str())
        plt.tight_layout()
        self.write (label)
        
