#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
from utils.db.DbConnection import DbConnection
import pandas as pd
import numpy as np

class StatsAggregator:

    
    def __init__ (self):
        self._base_selection = "SELECT * from player_stats ps LEFT JOIN match_stats ms ON ps.MatchStatsRef = ms.MatchID"
        self.db = DbConnection()
        self.init()

    def init (self):
        self.init_df()
        logging.info("Retrieved %d players" % self.df.shape[0])
        
    def init_df(self):
        try:
            self.df = pd.read_sql_query(self._base_selection, self.db._cnx)
        except:
            logging.error ("[ERROR] Query `%s` not valid: exit" % self._base_selection)
            exit(1)

    def execute(self):
        stats_to_be_aggregated = [col.replace("Home_","") for col in self.df.columns if col.startswith('Home_')]
        logging.info ("Number of columns to be targeted by aggregation: %d/%d" % (len(self.df.columns), len(stats_to_be_aggregated)))

        for stat in stats_to_be_aggregated:
            stat_against = stat + "_against"
            
            self.df[stat] = np.where(
                self.df["Team"] == "H",
                self.df["Home_"+stat],
                self.df["Away_"+stat]
            )
            self.df[stat_against] = np.where(
                self.df["Team"] == "A",
                self.df["Home_"+stat],
                self.df["Away_"+stat]
            )

        self.df.drop(columns=["Home_"+stat for stat in stats_to_be_aggregated], inplace=True)
        self.df.drop(columns=["Away_"+stat for stat in stats_to_be_aggregated], inplace=True)


    def get_df(self):
        return self.df
