#!/usr/bin/env python

"""
 Helper functions for the web decoding
"""

import requests

"""
 Get the HTML content of the webpage
"""
def read_webpage (url):
    req = requests.get(url, 'html.parser')
    return req.text

"""
 In a table: use this to get a cell content
"""
def scrape_info ( text, key, left, right):
    line = [(x.strip()) for x in text.splitlines() if key in x][0]
    return line.split (left)[-1].split(right)[0]

"""
 Get the div content (especially when it is a table)
 TODO: it does not handle well "div" and nested structures
"""
def get_div ( web_content, div_id = '', div_type = '', extra_label = '' ):
    div_content = str()        
    found = False
    if div_type == '' : return web_content
    for l in web_content.split('\n'):
        if not found:
            if div_id!='':
                if '<%s'%div_type not in l and '"%s"'%div_id not in l: continue
                else: found = True
            else:
                if '<%s'%div_type not in l: continue
                else: found = True

            if extra_label != '' and not extra_label in l and found: found = False
        if found:
            div_content += '%s\n' % l
            if '</%s>'%div_type in l: break
    return div_content


"""
 Get list of images in document
"""
def get_list_of_images (web_content):
    return [l for l in web_content.split('\n') if "<img" in l and "src=" in l]
