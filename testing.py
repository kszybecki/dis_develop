


# import sqlite3
# from sqlite3 import Error

# conn = None


# def insert_entity_sentence(entity_id, sentence_id):
#     conn.cursor().execute(
#         "INSERT INTO " + entity["name"] + "Sentence (SentenceId, " + entity["name"] + "Id) " + \
#         "VALUES (" + str(sentence_id) + ", " + str(entity_id) + ")"
#     )    
#     conn.commit()

# try:
#     conn = sqlite3.connect("C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db")


# except Error as e:
#     print(e)
# finally:
#     if conn:
#         conn.close()

import os
from pathlib import Path
import re

paragraph = "This is exactly what we need.  Would it possible to add the prior day for each of the dates below to the pivot table.  In order to validate the curve shift on the dates below we also need the prior days ending positions."

result = list(map(str.strip, re.split(r'\.[ ]+?', paragraph)))




setup = ""

