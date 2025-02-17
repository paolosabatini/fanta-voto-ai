#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
from bs4 import BeautifulSoup
import re
import utils.html.HtmlRetriever as hr
import models.retrieve.PlayerStats as ps
from models.retrieve.ParserError import ParserError

'''
Helper functions
'''

def get_all_stats_tables(bs4_html):
    return bs4_html.body.find_all ("div",
                                   attrs={"class" : "table_container tabbed current",
                                          "id" : re.compile(".*_summary")})
def get_all_gk_stats_tables(bs4_html):
    return bs4_html.body.find_all ("div",
                                   attrs={"class" : "table_container",
                                          "id" : re.compile("div_keeper_stats_.*")})

    
def is_table_row_to_be_skipped (irow, row):
    return (row.th.has_attr("class") and  "over_header" in row.th.attrs["class"]) \
        or (row.th.has_attr("scope") and row.th.attrs["scope"] == "col") \
        or ((str(irow-2)+" Players") in row.find("th", attrs={"data-stat":"player"}).contents[0])

'''
Player Stats retriever
'''
class PlayerStatsParser:

    stats = []
    errors = []
    _parser_algo = "html.parser"
    
    def __init__ (self):
        self.html = None


    def set_url (self, url):
        self.url = url
        self.html = hr.get_html (self.url)
        
    def execute(self):
        bs4_html = BeautifulSoup (self.html, self._parser_algo)
        stat_tables = get_all_stats_tables ( bs4_html )
        for stat_table in stat_tables:
            self.stats += self.get_stat_from_table ( stat_table )
            
            
        gk_stat_tables = get_all_gk_stats_tables ( bs4_html )
        for stat_gk_table in gk_stat_tables:
            self.fill_gk_stats ( stat_gk_table )
        
    def get_stat_from_table ( self, stat_table ):
        this_match_stats = []

        for irow, row in enumerate (stat_table.find_all(["tr"])):
            if is_table_row_to_be_skipped (irow, row): continue
            player_stats = ps.PlayerStats (row)

            if not player_stats.find_id():
                logging.error ("[ERROR] %s ID not found" % player_stats.name)
                self.errors.append( ParserError ("ID_NOT_FOUND", "Player ID for  %s not found in Player table" % player_stats.name) )
                continue
            else:
                logging.debug("[DEBUG] Player %s -> ID %s" % (player_stats.name, player_stats.id))
            this_match_stats.append (player_stats)
        logging.info ("N. MatchReport stats: \t %d" % len (this_match_stats))
        return this_match_stats

    def fill_gk_stats (self, gk_stat_table):
        for gk in gk_stat_table.tbody.find_all (["tr"]):
            gk_name = gk.th.a.contents[0]
            try:
                gk_stat = next ( pl for pl in self.stats if pl.name == gk_name)
                gk_stat.fill_gk_stats (gk)
            except:
                logging.error ("[ERROR] %s Not found" % gk_name)
                self.errors.append( ParserError ("GK_NOT_FOUND", "GK %s not found in PlayerStat table" % gk_name) )

    def clear (self):
        self.html = None
        self.stats.clear()
        self.errors.clear()
    
    def get_stats(self):
        return self.stats

    def get_errors(self):
        return self.errors
