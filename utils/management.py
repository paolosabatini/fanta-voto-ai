#!/usr/bin/env python

"""
 Helper functions for management (shell, etc..)
"""

import os, sys

"""
 Check whether folder exists and create it if missing
"""
def check_folder_and_create (path):
    if not os.path.exists (path):
        os.system ("mkdir %s" % path)

"""
 Save the JSON file from dictionary
"""
def save_json_from_dict (dictionary, file_name):
    import json
    with open (file_name,"w+") as f:
        json.dump (dictionary, f)


