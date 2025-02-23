#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)

import json

def get_dict_from_json_file (json_file):
    d = {}
    with open (json_file, "r+") as handle:
        d = json.loads (handle.read())

    return d
