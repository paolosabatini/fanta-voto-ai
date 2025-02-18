#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)

from utils.db.DbPlayerMarks import DbPlayerMarks

class PlayerStatsDresser:
    def __init__ (self):
        self.dbadapter = DbPlayerMarks()


    def get_vote (self, matchweek, id):
        this_query = "SELECT Punteggio FROM punteggio_giornate_calciatrici\
         WHERE IDGiornata = %d AND IDCalciatrice = %d" % (matchweek, id)

        self.dbadapter.execute(this_query)
        marks = self.dbadapter.fetchall()
        return -1 if len( marks ) == 0 else marks[0][0]
            
