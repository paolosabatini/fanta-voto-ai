#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

import os
from utils.plotting.PlotManager import PlotManager

'''
Main function
'''
def main():
    arguments = get_option_parser()
    json_configuration = arguments.config
    output_label = arguments.label
    input_filename = arguments.input
    logging.info("Json configuration:\t%s" % json_configuration)
    logging.info("Input Parquet data:\t%s" % input_filename)
    logging.info("Output label:\t%s" % output_label)

    if not os.path.isfile (json_configuration):
        logging.error ("[ERROR] Json configuration file is not found")
        exit()
    pm = PlotManager (json_configuration, output_label, input_filename)
    pm.plot()

    
'''
Argument parser
'''
def get_option_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input",type=str,
                        help="Path to parquet data",required=True)
    parser.add_argument("-c", "--config", dest="config",type=str,
                        help="Path to configuration JSON file",required=True)
    parser.add_argument("-l", "--label", dest="label",type=str,
                        help="Label to save the output with",default="v1")
    return parser.parse_args()
    

'''
Main executable
'''
if __name__ == '__main__':
    main()
