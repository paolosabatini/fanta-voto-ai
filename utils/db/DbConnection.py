#!/usr/bin/env python3

import MySQLdb as mysql

class DbConnection:
    _db = "fantavoto_ai"
    _config = {
        'user': 'root',
        'password': 'password',
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

    def query (self, query):
        if query == None or query == "" or "SELECT" not in query:
            logging.error ("[ERROR] Passed query is empty or not valid")
            return []
        self.execute (query)
        stats = [ list(row) for row in self.fetchall() ]
        return stats
        
