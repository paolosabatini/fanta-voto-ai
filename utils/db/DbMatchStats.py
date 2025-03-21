#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
from utils.db.DbConnection import DbConnection

class DbMatchStats(DbConnection):
    _debug = False

    _insert_query ='''\
    INSERT INTO match_stats (`MatchID`, \
    `Home_team`, `Home_goal`, `Home_xg`, `Home_possession`, `Home_pass_accuracy`, \
    `Home_sota`, `Home_saves`, `Home_fouls`, `Home_corners`, `Home_crosses`, `Home_tackles`,\
    `Home_interceptions`, `Home_clearances`, `Home_offsides`,\
    `Away_team`, `Away_goal`, `Away_xg`, `Away_possession`, `Away_pass_accuracy`, \
    `Away_sota`, `Away_saves`, `Away_fouls`, `Away_corners`, `Away_crosses`, `Away_tackles`,\
    `Away_interceptions`, `Away_clearances`, `Away_offsides`)\
    '''

    def get_values_for_match (self, stats):

        return '''\
        (\'%s\', \
        \'%s\', %d, %.1f, %d, %d,\
        %d, %d, %d, %d, %d, %d,\
        %d, %d, %d,\
        \'%s\', %d, %.1f, %d, %d,\
        %d, %d, %d, %d, %d, %d,\
        %d, %d, %d)\
        ''' % (
            stats.id,
            stats.home, int(stats.goal_home), float(stats.xg_home), int(stats.possession_home), int(stats.pass_accuracy_home),
            int(stats.sota_home), int(stats.saves_home), int(stats.fouls_home), int(stats.corners_home), int(stats.crosses_home), int(stats.tackles_home),
            int(stats.interceptions_home), int(stats.clearances_home), int(stats.offsides_home),
            stats.away, int(stats.goal_away), float(stats.xg_away), int(stats.possession_away), int(stats.pass_accuracy_away),
            int(stats.sota_away), int(stats.saves_away), int(stats.fouls_away), int(stats.corners_away), int(stats.crosses_away), int(stats.tackles_away),
            int(stats.interceptions_away), int(stats.clearances_away), int(stats.offsides_away)
        )

    def write_from_list(self, list_of_stats ):
        
        this_query = self._insert_query + ' VALUES '
        this_query += ",".join ( [ self.get_values_for_match (stats) for stats in list_of_stats ] )
        this_query += ';'
        try:
            self.execute(this_query)
            if not self._debug:
                self.commit()
        except Exception as e:
            logging.error ("[ERROR] DB:Error in committing match stats")
            logging.error (e)
            return False
        return True

