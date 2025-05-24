#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

import os
from utils.preprocess.StatsAggregator import StatsAggregator
import importlib

_BASE_OUTPUT_FOLDER = "./data/parquet/"

'''
Main function
'''
def main():
    arguments = get_option_parser()
    configuration = arguments.config
    output_label = arguments.label
    logging.info("Preprocess config:\t%s" % configuration)
    logging.info("Output label:     \t%s" % output_label)
    
    aggregator = StatsAggregator()
    aggregator.execute()
    
    preprocessor = load_preprocessor(configuration)
    preprocessor.set_df (aggregator.get_df())
    preprocessor.execute()
    
    save(preprocessor.get_df(), output_label)
    

'''
Argument parser
'''
def get_option_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config",type=str,
                        help="Name of preprocessing configuration",required=True,
                        choices=["Raw"])
    parser.add_argument("-l", "--label", dest="label",type=str,
                        help="Label to save the output with",default="v1")
    return parser.parse_args()

'''
Load the preprocessor
'''
def load_preprocessor (configuration_name):
    preprocessor_name = "Preprocess"+configuration_name
    module = importlib.import_module("utils.preprocess."+preprocessor_name)
    preprocessor_class = getattr(module, preprocessor_name)
    return preprocessor_class()

'''
Save preprocessed Dataframe
'''
def save(df, label):

    output_folder_name = _BASE_OUTPUT_FOLDER+label
    os.makedirs(output_folder_name, exist_ok=True)
    output_file_name = output_folder_name+"/data.parquet"
    
    logging.info("Saving to %s" % output_file_name)
    df.to_parquet(output_file_name)
    

'''
Main executable
'''
if __name__ == '__main__':
    main()
