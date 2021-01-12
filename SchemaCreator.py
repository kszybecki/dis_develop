


import os.path
from os import path

import sqlite3
from sqlite3 import Error

class SchemaCreator:

    enron_relational_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db"
    enron_data_warehouse_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_relational.db"
    entities = []

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
            length = len(list(filter(lambda x: x["name"] == entity["name"], SchemaCreator.entities)))            
            if length == 0:
                self.create_table(entity["name"])
                entities.append(entity)

            #check if entity instance already exists
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
                #here

    def insert_sentence(self, sentence):
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO Sentence (SentenceId, Sentence) VALUES (" + str(sentence["sentence_id"]) + ", '" + sentence["value"] + "')"
        )
        SchemaCreator.conn.commit()

    def create_table(self, table_name):
        # create entity table
        SchemaCreator.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" + table_name + "Id INTEGER PRIMARY KEY, Value TEXT, SentenceId INTEGER)"
            )
        SchemaCreator.conn.commit()

        #create Sentence relation table
        SchemaCreator.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + "Sentence (Value TEXT, SentenceId INTEGER, " + table_name + "Id)"
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

