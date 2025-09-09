#!/usr/bin/env python3

import logging
logger = logging.getLogger(__name__)
from utils.db.DbConnection import DbConnection
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

'''
Variables
'''

'''
Execute method
'''

class PreprocessGkBasic:

    _features_zscaling = [
        "GK_sota", "GK_GA", "GK_PSXG", "GK_saves", "Goal_diff"
    ]
    _features_minmax = [
        "Minutes", "Goals", "Assists", "Pens", "Pens_attempted",
        "Yellow_card", "Red_card", "Own_goals", "GK_pen_saved"
    ]

    _features = _features_zscaling + _features_minmax

    zscaler = StandardScaler()
    minmaxscaler = MinMaxScaler(feature_range=(-0.5, 0.5))
    
    def set_df(self,df):
        self.df = df
        
    def get_df (self):
        return self.df

    def get_df_zscaled (self):
        df_zscaled_features = self.df [self._features_zscaling]
        zscaled_array = self.zscaler.fit_transform(df_zscaled_features)
        return pd.DataFrame(zscaled_array, columns=df_zscaled_features.columns)

    def get_df_minmax(self):
        df_minmax_features = self.df [self._features_minmax]
        minmax_array = self.minmaxscaler.fit_transform(df_minmax_features)
        return pd.DataFrame(minmax_array, columns=df_minmax_features.columns)

    
    def execute (self):
        logging.info("GK Basic preprocessing: starting")

        # Selecting only GK on Fantasy
        self.df = self.df [ (self.df["FantaPosition"] == "P")
                            & self.df["Mark"] > 0 ] 

        # Add some feature
        # 1. Add feature to understand if GK lost the game or not
        self.df["Goal_diff"] = self.df["goal"].sub( self.df ["goal_against"] )
        
        # Selecting interesting feaetures
        df_zscaled = self.get_df_zscaled()
        df_minmaxscaled = self.get_df_minmax()
        self.df = pd.concat ( [df_zscaled, df_minmaxscaled], axis=1)


        
