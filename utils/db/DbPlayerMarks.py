#!/usr/bin/env python3
import MySQLdb as mysql
from utils.db.DbConnection import DbConnection

class DbPlayerMarks(DbConnection):

    _config = {
        'user': 'root',
        'password':'password',
        'host': 'localhost',
        'database': 'fantawomen_2425',
        'port':3306
    }
    
    def __init__ (self):
        self._cnx = mysql.connect(**self._config)
        self._cursor = self._cnx.cursor()



