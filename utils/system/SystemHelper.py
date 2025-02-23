#!/usr/bin/env python3

import os

def path_exists (path):
    return os.path.exists (path)

def check_and_create_folder (path):
    if path_exists(path):
        return
    os.makedirs (path)
    
