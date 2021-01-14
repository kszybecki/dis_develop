


import sqlite3
from sqlite3 import Error

conn = None


def insert_entity_sentence(entity_id, sentence_id):
    conn.cursor().execute(
        "INSERT INTO " + entity["name"] + "Sentence (SentenceId, " + entity["name"] + "Id) " + \
        "VALUES (" + str(sentence_id) + ", " + str(entity_id) + ")"
    )    
    conn.commit()

try:
    conn = sqlite3.connect("C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db")

    entity = {"name": "Organization", "value": "KRIS"}

    #check if entity instance already exists
    fetch_cursor = conn.execute(
        "SELECT * FROM " + entity["name"] + " WHERE Value = '" + entity["value"] + "'"
    )

    last_row_id = None
    result_row = fetch_cursor.fetchone()
    if result_row is None:
        insert_cursor = conn.cursor()
        insert_cursor.execute(
            "INSERT INTO " + entity["name"] + " (Value) " + \
            "VALUES ('" + entity["value"] + "')"
        )
        conn.commit()
        last_row_id = insert_cursor.lastrowid

    else: 
        # get ID value from primary key column
        last_row_id = result_row[0]

    insert_entity_sentence(1, 0)   


except Error as e:
    print(e)
finally:
    if conn:
        conn.close()




# stop = ""