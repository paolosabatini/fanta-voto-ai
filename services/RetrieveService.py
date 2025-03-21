#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

'''
Import the needed parsers
'''
from utils.parser.CalendarParser import CalendarParser

class RetrieveService:

    _url = "https://fbref.com/en/comps/208/schedule/Serie-A-Scores-and-Fixtures"

    matches = []
    stats = []
    errors = []
    
    def __init__ (self, matchweek):
        self.matchweek = matchweek


    def execute (self):
        
        cp = CalendarParser()
        cp.set_url (self._url)
        self.matches = cp.get_matches_by_matchweek (matchweek = self.matchweek)
        logging.info ("N. match report found: \t%d" % len (self.matches))

        [ match.retrieve_match_stats() for match in self.matches ]
        [ match.retrieve_stats() for match in self.matches ]
        self.errors  = [ match_report.errors for  match_report in self.matches ]
        
        
        
    def get_retrieved_stats(self):
        return self.stats

    def get_matches(self):
        return self.matches

    def get_all_stats (self):
        return [ pl_stat for match_report in self.matches for pl_stat in match_report.stats ] 

    def get_all_match_stats (self):
        return [ match_report.match_stats for match_report in self.matches ] 

    def get_all_errors(self):
        return [ err for match_report in self.matches for err in match_report.errors ] 
