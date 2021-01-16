


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


relation = "member".title().replace(" ", "") + "Relation"

print(relation)