#!/usr/bin/env python3

from utils.db.DbConnection import DbConnection

class DbPlayers(DbConnection):

    _query_get_all_players = "SELECT * from players"


    def get_all_players(self):
        self.execute (self._query_get_all_players)
        all_players = [ list(pl) for pl in self.fetchall() ]
        return all_players

