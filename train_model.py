#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

import os, sys
from utils.training.Trainer import Trainer

"""
Main function of the code
"""
def main ():

    arguments = get_option_parser()
    logging.info ("== Training ==")
    logging.info (" Model: \t%s" % arguments.model )
    logging.info (" Input: \t%s" % arguments.input)
    logging.info (" Output:\t%s" % arguments.output)
    logging.info (" Valid.:\t%s" % arguments.validation)

    trainer = Trainer ( arguments.model, arguments.input, arguments.validation)

    # train the model
    trainer.train ()


    # save the model
    trainer.save (arguments.output)
    
'''
Argument parser
'''
def get_option_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-m","--model", dest="model",  help="Model to train", default = None)
    parser.add_argument("-i","--input", dest="input",  help="Label of the input files", default = 'v1')
    parser.add_argument("-o","--output", dest="output",  help="Label for the output model", default = 'test')
    parser.add_argument("-v","--validation", dest="validation",  help="Cross-validation to use", default = None)
    return parser.parse_args()

"""
 Main function is called
"""
if __name__ == "__main__":
    main ()

