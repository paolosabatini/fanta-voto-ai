#!/usr/bin/env python


'''
 Decode the settings
'''
def decode_settings_to_dict (settings):
    return { x.split (':')[0] : x.split (':')[-1] for x in settings.split (",")  }
    
