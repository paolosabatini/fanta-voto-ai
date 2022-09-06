#!/usr/bin/env python

import os, sys

def check_folder_and_create (path):
    if not os.path.exists (path):
        os.system ("mkdir %s" % path)



def save_json_from_dict (dictionary, file_name):
    import json
    with open (file_name,"w+") as f:
        json.dump (dictionary, f)
