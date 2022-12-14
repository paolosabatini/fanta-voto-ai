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


"""
 Read the JSON file to dictionary
"""
def read_json_to_dict (file_name):
    import json
    with open (file_name,"r+") as f:
        dictionary = json.load(f)
    return dictionary


"""
 Get availaible matchdays
"""
def get_availaible_matchdays (path):
    return [int(x.split("/")[-1].split("_")[-1]) for x in os.listdir(path)]

"""
 Check file is actually there 
"""
def is_this_file_there (path_to_file):
    if not path_to_file: return False
    return os.path.exists (path_to_file)

"""
 Check file is actually there 
"""
def is_this_folder_there (path_to_folder):
    if not path_to_folder: return False
    return os.path.isdir (path_to_folder)

