#!/usr/bin/env python3

import mysql.connector
import csv
_csv_name = "Calciatrici.csv"

'''
Query
'''
query_all_players = '''
select IDCalciatrice, Ruolo, Nome, Cognome from calciatrici
'''

'''
Sql connection
'''

server = mysql.connector.connect(
    host = "c0k.h.filess.io",
    user = "FantaWomenDB_palacehurt",
    passwd = "a947d284ef9347c9b2375b2e76d2f20fb7b32775",
    database = "FantaWomenDB_palacehurt",
    port = 3307
)


'''
Get all players
'''
cursor = server.cursor()
cursor.execute (query_all_players)
players = cursor.fetchall()

'''
Export to CSV
'''
print (type (players).__name__)
print (type (players[0]).__name__)
with open (_csv_name, "w+") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(players)
