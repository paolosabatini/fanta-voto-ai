#!/usr/bin/env python

"""
 Main class that manages the reading of info and storage.
 - reading player statistics per matchday (web)
 - reading the fixtures of a matchday (web)
 - reading team performance (web)
 - reading votes FW (db)
 TODO: fixtures and match stats very limited
"""

from utils.myprint import myprint
from .conf import  _WEB_STATS_PLAYERS_FIGC_, _WEB_STATS_PLAYERS_FBREF_, _DATA_FOLDER_, _WEB_STATS_MATCHES_, _WEB_STATS_PERF_
from .conf import _SQL_CONNECTION_
from utils.globalvalues import get_dict_of_teams
import dataprep.web_helpers as webh 
import dataprep.figc_helpers as figch
import dataprep.fbref_helpers as fbrefh


class data_preparator ():

    # constructor
    def __init__ (self, matchday = 1, debug = False, use_fbref = False):
        self.matchday = matchday
        self.debug = debug
        self.use_fbref = use_fbref
        self.init()

    # init and logger
    def init (self):
        self.logger = myprint ("data_preptor", self.debug)
        self.logger.print_info ("initializing..")
        self.logger.print_info (msg = " - web-page players   = %s" % _WEB_STATS_PLAYERS_FBREF_ if self.use_fbref else _WEB_STATS_PLAYERS_FIGC_)
        self.logger.print_info (msg = " - web-page fixturess = %s" % _WEB_STATS_MATCHES_)
        self.logger.print_info (msg = " - web-page peform    = %s" % _WEB_STATS_PERF_)

    # read and save the player stats from web
    def read_player_stats (self):
        dict_teams = get_dict_of_teams()
        players = {}
        if self.use_fbref:
            players = self.get_player_stats_from_fbref (dict_teams)
        else:
            players = self.get_player_stats_from_figc (dict_teams)

       
        self.logger.print_info ("Storing output to JSON ..")
        self.save (players, 'players')

    def get_player_stats_from_figc (self, dict_teams):
        players = {}
        for team_name, team_url in dict_teams.items ():
            self.logger.print_debug( "   from " + str(team_name) )
            team_complete_url = _WEB_STATS_PLAYERS_FIGC_ + team_url
            players.update ( figch.decode_these_players ( webh.read_webpage(team_complete_url), team_name) )

        if self.matchday>1:
            players = self.subtract_previous_matchday (players, 'players')
        return players
     
    def sum_player_stats_from_jsons (self, previous_jsons):

        from utils.management import read_json_to_dict
        summed = {}
        for json in previous_jsons:
            curr_players = read_json_to_dict (json)
            for player_name in curr_players:
                if player_name not in summed:
                    summed [player_name] = curr_players [player_name]
                else:
                    for stat in summed[player_name]:
                        if stat in ['Ruolo','Squadra','Maglia']: continue
                        summed[player_name][stat] = float(summed[player_name][stat]) + float(curr_players [player_name][stat])

        return summed

        
    def subtract_previous_matchday (self, players, name_of_json):

        previous_jsons = [ 'data//Matchday_%d/%s.json' % (i, name_of_json) for i in range (1, self.matchday) ]
        self.logger.print_debug( "   subtracting player stats from previous %d matchdays" % len(previous_jsons) )        
        summed_previous_matchday = self.sum_player_stats_from_jsons (previous_jsons)

        for player_name in players:
            if player_name not in summed_previous_matchday: continue
            for stat in players [player_name]:
                if stat in ['Ruolo','Squadra','Maglia']: continue
                players [player_name][stat] = float (players [player_name][stat]) - float(summed_previous_matchday [player_name][stat])

        return players
            
    def get_player_stats_from_fbref (self, dict_teams):
        players = {}
        web_page_fixtures_content = webh.read_webpage(_WEB_STATS_PLAYERS_FBREF_)
        for team_name, team_url in dict_teams.items ():
            self.logger.print_debug( "   from " + str(team_name) )
            match_report_url = fbrefh.get_matchreport_url_for_team_and_matchday (web_page_fixtures_content, team_name, self.matchday)
            self.logger.print_debug( "     ~> " + (match_report_url if match_report_url else "N/A") )
            if not match_report_url:
                continue
            players.update (fbrefh.get_player_stats_for_team_from_matchreport ( webh.read_webpage(match_report_url), team_name, self.matchday))
        return players

            
    # read and save the fixtures from web
    # TODO: find a better place to get match info
    def read_fixtures (self):
        web_content = webh.read_webpage (_WEB_STATS_MATCHES_)
        fixtures = fbrefh.decode_fixtures (web_content, self.matchday)
        if self.debug:
            for fxt in fixtures: self.logger.print_debug ("   %s %s %s-%s" % (fxt['home'], fxt['away'], fxt['goal_home'], fxt['goal_away']))
        self.logger.print_info ("Storing output to JSON ..")
        self.save (fixtures, 'fixtures')

        
    # read and save the team performance from web
    def read_perf (self):
        web_content = webh.read_webpage (_WEB_STATS_PERF_)
        perf = fbrefh.decode_perf (web_content)
        if self.debug:
            for p in perf: self.logger.print_debug ("   for %s" % p["team"])
        self.logger.print_info ("Storing output to JSON ..")
        self.save (perf, 'performance')
        
        
    # read and save the vote from db
    def read_votes (self):
        import dataprep.sql_helpers as sql_helpers
        votes = sql_helpers.get_votes_per_matchday ( connection = _SQL_CONNECTION_,
                                                     matchday = self.matchday)
        self.logger.print_info ("Storing output to JSON ..")
        if self.debug:
            self.logger.print_debug ("   n. Calciatrici = %d" % len (votes.keys()))
            for iplayer, player in enumerate (votes.keys()):
                self.logger.print_debug ("   - %s: voto %.1f" % (player, votes[player]['Punteggio']))
                if iplayer > 10: break
            self.logger.print_debug ("   ..." )
        self.save (votes, 'votes')
        
    # save the dictionary to JSON
    def save (self, dictionary, label):
        from utils.management import check_folder_and_create
        check_folder_and_create (_DATA_FOLDER_)
        matchday_folder = "%s/Matchday_%d" % (_DATA_FOLDER_, self.matchday)
        check_folder_and_create (matchday_folder)
        json_file = "%s/%s.json" % (matchday_folder, label)
        self.logger.print_debug ("   to %s" % json_file)
        from utils.management import save_json_from_dict
        save_json_from_dict (dictionary, json_file)

