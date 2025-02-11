#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
from bs4 import BeautifulSoup

'''
Import needed modules
'''
import utils.html.HtmlRetriever as hr
from models.retrieve import MatchReport as mr


'''
Helper functions for parsing
'''
def is_header_of_calendar_table (irow):
    return (irow == 0)


def get_header_columns (row):
    return [ cell.text for cell in row.findChildren("th") ]

def get_matchweek_from_calendar_row (row):
    return row.findChild(["th","td"],attrs={"data-stat":"gameweek"}).contents[0]

def get_content_in_row ( row, element, attrs, get_href = False):
    current_a = row.findChild(element ,attrs=attrs).a
    return current_a.attrs["href"] if get_href else current_a.contents[0] 

'''
Calendar parser class
'''
class CalendarParser:

    _parser_algo = "html.parser"
    _calendar_table_id = "sched_2024-2025_208_1"
    url = str()
    matches = []

    def set_url (self, url):
        self.url = url
    
        
    def parse_calendar_by_matchweek (self, bs4_html, matchweek):
        calendar_table = bs4_html.body.find ("table", attrs={"id" : self._calendar_table_id})
        for irow, row in enumerate (calendar_table.findChildren('tr')):
            if is_header_of_calendar_table (irow):
                header = get_header_columns (row)
                continue
            try:
                this_matchweek = int(get_matchweek_from_calendar_row (row))
                this_matchweek = this_matchweek if this_matchweek != None else matches[-1]["gameweek"]
            except:
                # this is a spacer
                continue

            if this_matchweek < matchweek:
                continue
            elif this_matchweek > matchweek:
                break

            
            
            this_matchreport = mr.MatchReport( matchweek = matchweek,
                                               home = get_content_in_row (row, ["th","td"], {"data-stat":"home_team"}),
                                               away = get_content_in_row (row, ["th","td"], {"data-stat":"away_team"}),
                                               url =  get_content_in_row (row, ["th","td"], {"data-stat":"match_report"}, True) )
  

            logging.info ("Exported %s", str(this_matchreport))
            self.matches.append (this_matchreport)
            
    def get_matches_by_matchweek (self, matchweek):
        try:
            html = hr.get_html (self.url)
        except:
            logging.error ("[ERROR] No URL is available to retrieve matches")
            exit(1)

        self.parse_calendar_by_matchweek (BeautifulSoup (html,self._parser_algo),
                                          matchweek)


        return self.matches
