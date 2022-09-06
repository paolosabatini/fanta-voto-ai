#!/usr/bin/env python

from utils.myprint import myprint
from conf import  _WEB_STATS_PLAYERS_, _DATA_FOLDER_, _WEB_STATS_MATCHES_, _WEB_STATS_PERF_
from conf import _SQL_CONNECTION_
import web_helpers as webh 
import figc_helpers as figch
import fbref_helpers as fbrefh

class data_preparator ():
    
    def __init__ (self, matchday = 1, debug = False):
        self.matchday = matchday
        self.debug = debug
        self.init()

    def init (self):
        self.logger = myprint ("data_preptor", self.debug)
        self.logger.print_info ("initializing..")
        self.logger.print_info (msg = " - web-page players   = %s" % _WEB_STATS_PLAYERS_)
        self.logger.print_info (msg = " - web-page fixturess = %s" % _WEB_STATS_MATCHES_)
        self.logger.print_info (msg = " - web-page peform    = %s" % _WEB_STATS_PERF_)

    def read_player_stats (self):
        web_content = webh.read_webpage (_WEB_STATS_PLAYERS_)
        dict_teams = figch.get_dict_of_teams (web_content)

        players = {}
        for team_name, team_url in dict_teams.iteritems ():
            self.logger.print_debug( "   from " + str(team_name) )
            team_complete_url = _WEB_STATS_PLAYERS_ + team_url
            players.update ( figch.decode_these_players ( webh.read_webpage(team_complete_url), team_name) )
           
        self.logger.print_info ("Storing output to JSON ..")
        self.save (perf, 'players')
            
    # TODO: find a better place to get match info
    def read_fixtures (self):
        web_content = webh.read_webpage (_WEB_STATS_MATCHES_)
        fixtures = fbrefh.decode_fixtures (web_content, self.matchday)
        if self.debug:
            for fxt in fixtures: self.logger.print_debug ("   %s %s %s-%s" % (fxt['home'], fxt['away'], fxt['goal_home'], fxt['goal_away']))
        self.logger.print_info ("Storing output to JSON ..")
        self.save (perf, 'fixtures')
        


    def read_perf (self):
        web_content = webh.read_webpage (_WEB_STATS_PERF_)
        perf = fbrefh.decode_perf (web_content)
        if self.debug:
            for p in perf: self.logger.print_debug ("   for %s" % p["team"])
        self.logger.print_info ("Storing output to JSON ..")
        self.save (perf, 'performance')
        
        


    def read_votes (self):
        import sql_helpers
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
        

    def save (self, dictionary, label):
        from utils.management import check_folder_and_create
        check_folder_and_create (_DATA_FOLDER_)
        matchday_folder = "%s/Matchday_%d" % (_DATA_FOLDER_, self.matchday)
        check_folder_and_create (matchday_folder)
        json_file = "%s/%s.json" % (matchday_folder, label)
        self.logger.print_debug ("   to %s" % json_file)
        from utils.management import save_json_from_dict
        save_json_from_dict (dictionary, json_file)

