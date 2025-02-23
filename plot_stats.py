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
    logging.info("Json configuration:\t%s" % json_configuration)

    if not os.path.isfile (json_configuration):
        logging.error ("[ERROR] Json configuration file is not found")
        exit()
    pm = PlotManager (json_configuration, output_label)
    pm.plot()

    
'''
Argument parser
'''
def get_option_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
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
