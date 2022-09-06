#!/usr/bin/env python

import requests

def read_webpage (url):
    req = requests.get(url, 'html.parser')
    return req.text

