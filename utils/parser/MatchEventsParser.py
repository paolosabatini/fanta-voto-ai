#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
from bs4 import BeautifulSoup
import utils.html.HtmlRetriever as hr
import re
import models.retrieve.MatchEvent as me
from models.retrieve.ParserError import ParserError

'''
Helper functions
'''
def get_all_events(bs4_html):
    return bs4_html.body.find ("div", attrs={"id":"events_wrap"}).findAll("div",
                                                                          attrs={"class": re.compile("event .*")})

'''
Match Events Parser
'''
class MatchEventsParser:
    events = []
    _parser_algo = "html.parser"
    
    def __init__ (self):
        self.html = None


    def set_url (self, url):
        self.url = url
        self.html = hr.get_html (self.url)

    def set_html (self, html):
        self.html = html

    def get_events(self):
        return self.events

    def clear (self):
        self.html = None
        self.events.clear()


    def execute (self):
        bs4_html = BeautifulSoup (self.html, self._parser_algo)
        event_rows = get_all_events(bs4_html)
        self.events = [ me.MatchEvent(event_row )for event_row in event_rows ]
        logging.info ("N. MatchEvents:\t%d" % len (self.events))
