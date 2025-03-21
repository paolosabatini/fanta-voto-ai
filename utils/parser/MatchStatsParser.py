#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

import utils.html.HtmlRetriever as hr
from models.retrieve.MatchStats import MatchStats
from bs4 import BeautifulSoup

'''
Helper methods
'''

def get_team_from_scorebox (bs4_scorebox, team):
    index = 0 if team == "home" else -1
    return (bs4_scorebox.find_all("img", attrs={"class" : "teamlogo"})[index].get("alt").strip(" Club Crest"))

def get_goal_from_scorebox (bs4_scorebox, team, is_xg = False):
    index = 0 if team == "home" else -1
    suffix = "_xg" if is_xg else str()
    return (bs4_scorebox.find_all("div", attrs={"class" : "score"+suffix})[index].contents[0])

'''
Match stats parser
'''
class MatchStatsParser:
    url = None
    match_stats = None
    html = None
    _parser_algo = "html.parser"
    _blacklist_stats = ["Cards"]
    _whitelist_stats_extra = ["Fouls", "Corners", "Crosses", "Tackles", "Interceptions", "Clearances", "Offsides"]
    
    def set_url (self, url):
        self.url = url
        self.html = hr.get_html (self.url)
        self.match_stats = MatchStats( self.extract_id () )

    def extract_id (self):
        return self.url.split("/")[-1]
    
    def get_stats(self):
        return self.match_stats
        
    def clear (self):
        self.html = None
        self.match_stats = None
        self.url = None

    def execute (self):
        bs4_html = BeautifulSoup (self.html, self._parser_algo)

        self.fill_from_scorebox (bs4_html)
        self.fill_from_team_stats (bs4_html)
        self.fill_from_team_stats_extra (bs4_html)

    def fill_from_scorebox (self, bs4_html):
        
        scorebox = bs4_html.body.find ("div", attrs={"class" : "scorebox"})
        self.match_stats.home = get_team_from_scorebox (scorebox, 'home')
        self.match_stats.away = get_team_from_scorebox (scorebox, 'away')
        self.match_stats.goal_home = get_goal_from_scorebox (scorebox, 'home')
        self.match_stats.goal_away = get_goal_from_scorebox (scorebox, 'away')
        self.match_stats.xg_home = get_goal_from_scorebox (scorebox, 'home', True)
        self.match_stats.xg_away = get_goal_from_scorebox (scorebox, 'away', True)
        
        
    def fill_from_team_stats (self, bs4_html):
        team_stats =  bs4_html.body.find ("div", attrs={"id" : "team_stats"})
        this_label = str()
        home_value = 0
        away_value = 0
        for irow,row in enumerate( team_stats.table.find_all(["tr"])):

            if row.th != None :
                # header row
                this_label = row.th.contents[0]
                continue
            if this_label == str() or this_label in self._blacklist_stats:
                continue

            cols = row.find_all("td")
            home_value = cols[0].div.div.strong.contents[0].strip("%")
            away_value = cols[-1].div.div.strong.contents[0].strip("%")
            logging.debug ("MatchStats: %s -> %s vs. %s" % (this_label, home_value, away_value))
            self.fill_match_stats_from_label (this_label, home_value, away_value)
            
            # reset
            this_label = str()
        
    def fill_match_stats_from_label (self, label, home_value, away_value):
        home_value = '0' if home_value == '' else home_value
        away_value = '0' if away_value == '' else away_value
        match label:
            case "Possession":
                self.match_stats.possession_home = home_value
                self.match_stats.possession_away = away_value
            case "Passing Accuracy":
                self.match_stats.pass_accuracy_home = home_value
                self.match_stats.pass_accuracy_away = away_value
            case "Shots on Target":
                self.match_stats.sota_home = home_value
                self.match_stats.sota_away = away_value
            case "Saves":
                self.match_stats.saves_home = home_value
                self.match_stats.saves_away = away_value
            case "Fouls":
                self.match_stats.fouls_home = home_value
                self.match_stats.fouls_away = away_value
            case "Corners":
                self.match_stats.corners_home = home_value
                self.match_stats.corners_away = away_value
            case "Crosses":
                self.match_stats.crosses_home = home_value
                self.match_stats.crosses_away = away_value
            case "Tackles":
                self.match_stats.tackles_home = home_value
                self.match_stats.tackles_away = away_value
            case "Interceptions":
                self.match_stats.interceptions_home = home_value
                self.match_stats.interceptions_away = away_value
            case "Clearances":
                self.match_stats.clearances_home = home_value
                self.match_stats.clearances_away = away_value
            case "Offsides":
                self.match_stats.offsides_home = home_value
                self.match_stats.offsides_away = away_value

        
    def fill_from_team_stats_extra (self, bs4_html):
        team_stats_extra = bs4_html.body.find ("div", attrs={"id" : "team_stats_extra"})

        for label in self._whitelist_stats_extra:
            label_div = team_stats_extra.find("div", string = label)
            home_value = label_div.find_previous_sibling("div").contents[0]
            away_value = label_div.find_next_sibling("div").contents[0]
            self.fill_match_stats_from_label ( label, home_value, away_value)        

