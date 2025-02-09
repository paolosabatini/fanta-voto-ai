#!/usr/bin/env python

"""
 Store some global conditions
"""

_MATCHES_IN_REGULAR_SEASON_ = 18

def is_regular_season (matchday):
    return (matchday <= _MATCHES_IN_REGULAR_SEASON_)

def get_matches_in_regular_season():
    return _MATCHES_IN_REGULAR_SEASON_

def get_dict_of_teams():
    return {
        "Roma" : "",
        "Juventus" : "",
        "Fiorentina" : "",
        "Sassuolo" : "",
        "Inter" : "",
        "Milan" : "",
        "Como" : "",
        "Napoli" : "",
        "Sampdoria" : "",
        "Pomigliano" : ""
    }

    
