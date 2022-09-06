#!/usr/bin/env python

import mysql.connector

def get_votes_per_matchday ( connection, matchday ):
    sqlman = sqlmanager (connection)
    votes = sqlman.get_all_votes_per_matchday (matchday)
    return votes

class sqlmanager ():

    
    
    def __init__ (self, connection):
       self.connection = connection
       self.init()
       
    def init (self):
        self.server = mysql.connector.connect(
            host = self.connection ['host'],
            user = self.connection ['user'],
            passwd = self.connection ['password'],
            database = self.connection ['database']
        )
        


    def get_all_votes_per_matchday (self, matchday):
        cmd = 'select c.Nome, c.Cognome, c.IDSquadra, pgc.Punteggio, pgc.PunteggioBonus, pgc.PunteggioTotale'
        cmd += ' from calciatrici c left join punteggio_giornate_calciatrici pgc on pgc.IDCalciatrice = c.IDCalciatrice'
        cmd += ' where pgc.IDGiornata = %d' % matchday

        cursor = self.server.cursor()
        cursor.execute (cmd)
        votes_per_player_raw = cursor.fetchall()

        votes_per_player = {}
        for vppr in votes_per_player_raw:
            name = vppr[0] + ' ' + vppr [1]
            votes_per_player [name] = {
                'Squadra' : vppr [2],
                'Punteggio' : vppr [3],
                'PunteggioBonus' : vppr [4],
                'PunteggioTotale' : vppr [5],
            }
            
        return votes_per_player
