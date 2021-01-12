


import sqlite3
from sqlite3 import Error

conn = None
try:
    conn = sqlite3.connect("C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db")

    SchemaCreator.conn.cursor().execute(
        "SELECT * FROM " + entity["name"] + " WHERE Value = '" + entity["value"] + "'"
    )

    result = SchemaCreator.conn.cursor().fetchone()
    if result is None:
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO " + entity["name"] + " (Value, SentenceId) " + \
            "VALUES ('" + entity["value"] + "', " + str(entity["sentence_id"]) +")"
        )
        SchemaCreator.conn.commit()
    else:

        
    conn.commit()
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()




# stop = ""