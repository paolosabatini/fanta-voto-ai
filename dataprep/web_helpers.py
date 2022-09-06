#!/usr/bin/env python

import requests

def read_webpage (url):
    req = requests.get(url, 'html.parser')
    return req.text

def scrape_info ( text, key, left, right):
    line = [(x.strip()) for x in text.splitlines() if key in x][0]
    return line.split (left)[-1].split(right)[0]

def get_div ( web_content, div_id = '', div_type = '' ):
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
        if found:
            div_content += '%s\n' % l
            if '</%s>'%div_type in l: break
    return div_content
