#!/usr/bin/env python

import MySQLdb as mysql

class DbConnection:
    _db = "fantavoto_ai"
    _config = {
        'user': 'root',
        'host': 'localhost',
        'database': 'fantavoto_ai'
    }
    
    def __init__ (self):
        self._cnx = mysql.connect(**self._config)
        self._cursor = self._cnx.cursor()
        

    def execute (self, query):
        self._cursor.execute(query)

        
    def fetchall (self):
        return self._cursor.fetchall()

    def commit(self):
        self._cnx.commit()
