


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
        SchemaCreator.schema_type = schema_type
        try:
            if schema_type == "Relational":
                SchemaCreator.conn = sqlite3.connect(SchemaCreator.enron_relational_path)
                self.create_sentence_table()
            else: 
                SchemaCreator.conn = sqlite3.connect(SchemaCreator.enron_data_warehouse_path)  
                self.create_fact_table()                
        except Error as e:
            print(e)

    def insert_relational_entities(self, entities, sentence):
        if len(entities) > 0:
            self.insert_sentence(sentence)
        for entity in entities:
            #check if table already exists
            length = len(list(filter(lambda x: x["name"] == entity["name"], SchemaCreator.prev_entities)))            
            if length == 0:
                self.create_table(entity)
                SchemaCreator.prev_entities.append(entity)
            
            last_row_id = None
            result_row = self.check_if_entity_value_exists(entity)
            if result_row is None:
                table_name = self.get_table_name(entity)
                insert_cursor = SchemaCreator.conn.cursor()
                insert_cursor.execute(
                    "INSERT INTO " + table_name + " (Value) " + \
                    "VALUES ('" + entity["value"] + "')"
                )
                SchemaCreator.conn.commit()
                last_row_id = insert_cursor.lastrowid
            else: 
                # get ID value from primary key column
                last_row_id = result_row[0]

            self.insert_entity_sentence(entity, last_row_id, sentence["sentence_id"]) 

    def check_if_entity_value_exists(self, entity):
        table_name = self.get_table_name(entity)
        fetch_cursor = SchemaCreator.conn.execute(
            "SELECT * FROM " + table_name + " WHERE Value = '" + entity["value"] + "'"
        )
        result_row = fetch_cursor.fetchone()
        return result_row

    def insert_entity_sentence(self, entity, entity_id, sentence_id):
        table_name = self.get_table_name(entity)
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO " + table_name + "Sentence (SentenceId, " + table_name + "Id) " + \
            "VALUES (" + str(sentence_id) + ", " + str(entity_id) + ")"
        )    
        SchemaCreator.conn.commit()

    def insert_sentence(self, sentence):
        SchemaCreator.conn.cursor().execute(
            "INSERT INTO Sentence (SentenceId, Sentence) VALUES (" + str(sentence["sentence_id"]) + ", '" + sentence["value"] + "')"
        )
        SchemaCreator.conn.commit()

    def create_table(self, entity):
        # create entity table
        table_name = self.get_table_name(entity)
        SchemaCreator.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" + table_name + "Id INTEGER PRIMARY KEY, Value TEXT)"
            )
        SchemaCreator.conn.commit()

        #create Sentence relation table
        if SchemaCreator.schema_type == "Relational":
            SchemaCreator.conn.cursor().execute(
                "CREATE TABLE IF NOT EXISTS " + entity["name"] + "Sentence (SentenceId INTEGER, " + entity["name"] + "Id INTEGER)"
                )
            SchemaCreator.conn.commit()

    def get_table_name(self, entity):
        if SchemaCreator.schema_type == "Relational":
            return entity["name"]
        else:
            return "Dim" + entity["name"]             

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

