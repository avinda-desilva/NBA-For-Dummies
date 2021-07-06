from __future__ import print_function
from test import get_data
import mysql.connector
from mysql.connector import errorcode
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

#dbadmin password: cs411bbotb92


#CREATE TABLE Player(
#
#Player_ID INTEGER NOT NULL
#
#Season_ID INTEGER NOT NULL
#
#Player_Name CHAR(20)
#
#Draft Year INTEGER
#
#Attended College CHAR(20)
#
#Teams Played Array CHAR(20)
#
#Assists in Season INTEGER
#
#RB’s in Season INTEGER
#
#Points in Season INTEGER
#
#Steals in Season INTEGER
#
#PRIMARY KEY(Player_ID, Player_Name)
#
#FOREIGN KEY(Player_ID) REFERENCES InfoPlayerX, ON DELETE CASCADE
#
#)
DB_NAME = "NBA"

TABLES = {}
TABLES['Players'] = (
    "CREATE TABLE `Player` ("
    "  `player_id` int(10) NOT NULL,"
    "  `season_id` varchar(10) NOT NULL,"
    "  `team_id` int(10) NOT NULL,"
    "  `player_name` varchar(30) NOT NULL,"
    "  `points` int(4) NOT NULL,"
    "  PRIMARY KEY (`player_id`,`season_id`, `team_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password123',
)
print("PASSED")
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
        
        

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
        
all_players = players.get_players()[3653::]
SQL_Formula = "INSERT INTO Player (player_id, season_id, team_id, points, player_name) VALUES (%s, %s, %s, %s, %s)"
for player in all_players:
    player_data =  get_data(player)
    cursor.executemany(SQL_Formula, player_data)
    cnx.commit()
#    print(player_df)

cursor.close()
cnx.close()