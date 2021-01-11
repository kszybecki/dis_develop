


import os.path
from os import path

import sqlite3
from sqlite3 import Error

database_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_db.db"

conn = None

def create_sentence_table(cursor):
    cursor.execute(
        ''' 
            CREATE TABLE Sentence (
                SentenceId INT PRIMARY KEY,
                Sentence TEXT
            )
        '''
    )
    conn.commit()

try:
    conn = sqlite3.connect(database_path)      
except Error as e:
    print(e)

create_sentence_table(conn.cursor())
