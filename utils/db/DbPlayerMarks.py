#!/usr/bin/env python3
import MySQLdb as mysql
from utils.db.DbConnection import DbConnection

class DbPlayerMarks(DbConnection):

    _config = {
        'user': 'FantaWomenDB_palacehurt',
        'password':'a947d284ef9347c9b2375b2e76d2f20fb7b32775',
        'host': 'c0k.h.filess.io',
        'database': 'FantaWomenDB_palacehurt',
        'port':3307
    }
    
    def __init__ (self):
        self._cnx = mysql.connect(**self._config)
        self._cursor = self._cnx.cursor()



