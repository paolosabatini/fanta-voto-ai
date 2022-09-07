#!/usr/bin/env python

"""
 Helpers class and functions for SQL management
 - get_votes_per_matchday: interface to open the connection and read
 - sqlmanager: managing the connection and queries
"""

import mysql.connector

"""
 Interface function to get votes from db
"""
def get_votes_per_matchday ( connection, matchday ):
    sqlman = sqlmanager (connection)
    votes = sqlman.get_all_votes_per_matchday (matchday)
    return votes

"""
 Class that manages the connectiona and queries.
 - init: initialize the connection
 - get_all_votes_per_matchday: launching query and providing the result
"""
class sqlmanager ():

    # constructor
    def __init__ (self, connection):
       self.connection = connection
       self.init()
       
    # init function   
    def init (self):
        self.server = mysql.connector.connect(
            host = self.connection ['host'],
            user = self.connection ['user'],
            passwd = self.connection ['password'],
            database = self.connection ['database']
        )
        
    # get the votes: launching query and providing results
    def get_all_votes_per_matchday (self, matchday):
        from utils.converter import name2noutf8
        
        cmd = 'select c.Nome, c.Cognome, c.IDSquadra, pgc.Punteggio, pgc.PunteggioBonus, pgc.PunteggioTotale'
        cmd += ' from calciatrici c left join punteggio_giornate_calciatrici pgc on pgc.IDCalciatrice = c.IDCalciatrice'
        cmd += ' where pgc.IDGiornata = %d and pgc.Presenza = 1' % matchday

        cursor = self.server.cursor()
        cursor.execute (cmd)
        votes_per_player_raw = cursor.fetchall()

        votes_per_player = {}
        for vppr in votes_per_player_raw:
            name = name2noutf8(vppr[0] + ' ' + vppr [1])
            votes_per_player [name] = {
                'Squadra' : vppr [2],
                'Punteggio' : vppr [3],
                'PunteggioBonus' : vppr [4],
                'PunteggioTotale' : vppr [5],
            }
            
        return votes_per_player
