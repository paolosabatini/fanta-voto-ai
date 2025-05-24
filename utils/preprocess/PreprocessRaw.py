#!/usr/bin/env python3

import logging
logger = logging.getLogger(__name__)
from utils.db.DbConnection import DbConnection
import pandas as pd
import numpy as np

'''
Variables
'''

'''
Execute method
'''

class PreprocessRaw:

    def set_df(self,df):
        self.df = df
        
    def get_df (self):
        return self.df

    def execute (self):
        logging.info("ConfigRaw: returning received DataFrame")

        
