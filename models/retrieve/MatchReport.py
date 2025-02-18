#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

import utils.html.HtmlRetriever as hr
import utils.parser.PlayerStatsParser as psr
import utils.dresser.PlayerStatsDresser as psd
from copy import deepcopy

_base_host_url = "https://fbref.com/"


class MatchReport:

    matchweek = None
    home = None
    away = None
    url  = None
    stats = []
    errors = []
    
    def __init__ (self, matchweek, home, away, url):
        self.matchweek = matchweek
        self.home = home
        self.away = away
        self.url = _base_host_url + url
        
    def __str__ (self):
        return ("[G %d] %s\t-\t%s\t (%s)" %
                (self.matchweek,
                 self.home,
                 self.away,
                 "URL found" if self.url != None else "URL missing"))
        
    
    def retrieve_stats(self):

        parser = psr.PlayerStatsParser ()
        parser.set_url ( self.url )
        parser.execute()
        self.stats = deepcopy(parser.get_stats())
        self.errors = deepcopy(parser.get_errors())
        parser.clear()

        dresser = psd.PlayerStatsDresser()
        [ stat.set_mark ( dresser.get_vote( self.matchweek, stat.id ) ) for stat in self.stats ]
