


import os.path
from os import path

import sqlite3
from sqlite3 import Error

class SchemaCreator:

    enron_relational_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db"
    enron_data_warehouse_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db"
    prev_entities = []

    def __init__(self, schema_type):
        SchemaCreator.conn = None
        try:
            if schema_type == "Relational":
                SchemaCreator.conn = sqlite3.connect(SchemaCreator.enron_relational_path)
                self.create_sentence_table()
            else: 
                SchemaCreator.conn = sqlite3.connect(SchemaCreator.enron_data_warehouse_path)  
                self.create_fact_table()                
        except Error as e:
            print(e)

    def insert_entities(self, entities, sentence):
        for entity in entities:
            #check if table already exists
            length = len(list(filter(lambda x: x["name"] == entity["name"], SchemaCreator.prev_entities)))            
            if length == 0:
                if entity["name"] == None:
                    stop = ""
                self.create_table(entity["name"])
                SchemaCreator.prev_entities.append(entity)

            #check if entity instance already exists
            fetch_cursor = SchemaCreator.conn.execute(
                "SELECT * FROM " + entity["name"] + " WHERE Value = '" + entity["value"] + "'"
            )
            
            last_row_id = None
            result_row = fetch_cursor.fetchone()
            if result_row is None:
                insert_cursor = SchemaCreator.conn.cursor()
                insert_cursor.execute(
                    "INSERT INTO " + entity["name"] + " (Value) " + \
                    "VALUES ('" + entity["value"] + "')"
                )
                SchemaCreator.conn.commit()
                last_row_id = insert_cursor.lastrowid
            else: 
                # get ID value from primary key column
                last_row_id = result_row[0]

            self.insert_entity_sentence(entity, last_row_id, sentence["sentence_id"]) 

    def insert_entity_sentence(self, entity, entity_id, sentence_id):
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO " + entity["name"] + "Sentence (SentenceId, " + entity["name"] + "Id) " + \
            "VALUES (" + str(sentence_id) + ", " + str(entity_id) + ")"
        )    
        SchemaCreator.conn.commit()

    def insert_sentence(self, sentence):
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO Sentence (SentenceId, Sentence) VALUES (" + str(sentence["sentence_id"]) + ", '" + sentence["value"] + "')"
        )
        SchemaCreator.conn.commit()

    def create_table(self, table_name):
        # create entity table
        SchemaCreator.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" + table_name + "Id INTEGER PRIMARY KEY, Value TEXT)"
            )
        SchemaCreator.conn.commit()

        #create Sentence relation table
        SchemaCreator.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + "Sentence (SentenceId INTEGER, " + table_name + "Id INTEGER)"
            )
        SchemaCreator.conn.commit()


    def create_sentence_table(self):
        SchemaCreator.conn.cursor().execute(
            """
                CREATE TABLE IF NOT EXISTS Sentence (
                    SentenceId INTEGER PRIMARY KEY,
                    Sentence TEXT
                )
            """
        )
        SchemaCreator.conn.commit()

    def create_fact_table(self):
        SchemaCreator.conn.cursor().execute(
            """ 
                CREATE TABLE IF NOT EXISTS Fact (
                    FactId INTEGER PRIMARY KEY
                )
            """
        )
        SchemaCreator.conn.commit()

    def tear_down(self):
        if SchemaCreator.conn:
            SchemaCreator.conn.close()

