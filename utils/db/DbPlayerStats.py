#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
from utils.db.DbConnection import DbConnection

class DbPlayerStats(DbConnection):
    _debug = False
    
    _insert_query_player ='''\
    INSERT INTO player_stats (`Matchweek`, `ID`, `Name`, `Position`, `Minutes`, \
    `Goals`, `Assists`, `Pens`, `Pens_attempted`, `Shots`, \
    `Shots_on_target`, `Yellow_card`, `Red_card`, `Touches`, `Tackles`, \
    `Intercepts`, `Blocks`, `XG`, `NPXG`, `XA`, \
    `SCA`, `GCA`, `Pass_completed`, `Pass_attempted`, `Progressive_pass`, \
    `Carries`, `Progressive_carries`, `Dribbles`, `Dribbles_attempted`, \
    `Mark`, `FantaPosition`)\
    '''

    def get_values_for_player (self, stats, matchweek):

        return '''\
        (%d, %d, \'%s\', \'%s\', %d, \
        %d, %d, %d, %d, %d, \
        %d, %d, %d, %d, %d, \
        %d, %d, %f, %f, %f, \
        %f, %f, %d, %d, %d, \
        %d, %d, %d, %d,\
        %f, \'%s\')\
        ''' % (
            int(matchweek), int(stats.id), stats.name, stats.pos, int(stats.min),
            int(stats.goal), int(stats.assist), int(stats.pen), int(stats.pen_attempted), int(stats.shots),
            int(stats.shots_on_target), int(stats.yellow_card), int(stats.red_card), int(stats.touches), int(stats.tackles),
            int(stats.intercepts), int(stats.blocks), float(stats.xg), float(stats.npxg), float(stats.xa),
            float(stats.shot_creating_actions), float(stats.goal_creating_actions), int(stats.pass_completed), int(stats.pass_attempted), int(stats.progressive_pass),
            int(stats.carries), int(stats.progressive_carries), int(stats.dribbles), int(stats.dribbles_attempted),
            float(stats.mark), str(stats.fanta_pos)
        )

    def get_update_query_gk_stats (self, gk):
        return '''\
        UPDATE player_stats \
        SET GK_sota = %d, GK_GA = %f, GK_saves = %d, GK_PSXG = %f, GK_launches_completed = %d, \
        GK_passes = %d, GK_throws = %d, GK_avg_pass_length = %f, GK_crosses = %d, \
        GK_crosses_stopped = %d, GK_def_actions_outside_box = %d WHERE ID = %d \
        ''' % (
            int(gk.gk_sota), float(gk.gk_ga), int(gk.gk_saves), float(gk.gk_psxg), int(gk.gk_launches_completed),
            int(gk.gk_passes), int(gk.gk_throws), float(gk.gk_avg_pass_length), int(gk.gk_crosses),
            int(gk.gk_crosses_stopped), int(gk.gk_def_actions_outside_box), int(gk.id)
        )
    
    def write_from_list_for_matchweek(self, matchweek, list_of_stats ):
        
        this_query = self._insert_query_player + ' VALUES '
        this_query += ",".join ( [ self.get_values_for_player (stats, matchweek) for stats in list_of_stats ] )
        this_query += ';'
        try:
            self.execute(this_query)
            if not self._debug:
                self.commit()
        except:
            logging.error ("[ERROR] DB:Error in committing players matchweek %d" % (matchweek))
            return False
        return True
        
    def update_gk_stats_for_matchweek (self, matchweek, list_of_gk):
        list_of_queries = [ self.get_update_query_gk_stats (gk) for gk in list_of_gk if gk.has_valid_gk_stats() ]
        for iquery, query in enumerate(list_of_queries):
            try:
                self.execute(query)
                if self._debug:
                    continue
                self.commit()
            except:
                logging.error ("[ERROR] DB:Error in committing GK [%d] %s for matchweek %d" % (
                list_of_gk [iquery].id,
                list_of_gk [iquery].name,
                matchweek))
                return False
        return True


    def query (self, query):
        if query == None or query == "" or "SELECT" not in query:
            logging.error ("[ERROR] Passed query is empty or not valid")
            return []
        self.execute (query)
        stats = [ list(pl) for pl in self.fetchall() ]
        return stats
        
