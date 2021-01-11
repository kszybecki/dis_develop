


import os.path
from os import path

import sqlite3
from sqlite3 import Error

'''
EntityExtractor.entity_list.append({
        "name": entity["entity_group"],
        "value": entity["word"],
        "begin_idx": begin_idx,
        "end_idx": end_idx,
        "sentence_id": EntityExtractor.sentence_id                    
})
'''

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
            SchemaCreator.conn.cursor.execute(
                "INSERT INTO " + entity["name"] + " (Value) " + \
                "VALUES (" + entity["value"] + ")"
            )
            SchemaCreator.conn.commit()

    def insert_sentence(self, sentence):
        SchemaCreator.conn.cursor.execute(
            "INSERT INTO Sentence (SentenceId, Sentence) " + \
            "VALUES (" + sentence["sentence_id"] + ", " + sentence["value"] + ")"
        )
        SchemaCreator.conn.commit()

    def create_table(self, table_name):
        SchemaCreator.conn.cursor.execute("CREATE TABLE IF NOT " + table_name + " (" + table_name + "Id INT PRIMARY KEY, Value TEXT)")
        SchemaCreator.conn.commit()

    def create_sentence_table(self):
        SchemaCreator.conn.cursor.execute(
            ''' 
                CREATE TABLE IF NOT Sentence (
                    SentenceId INT PRIMARY KEY,
                    Sentence TEXT
                )
            '''
        )
        SchemaCreator.conn.commit()

    def create_fact_table(self):
        SchemaCreator.conn.cursor.execute(
            ''' 
                CREATE TABLE IF NOT Fact (
                    FactId INT PRIMARY KEY
                )
            '''
        )
        SchemaCreator.conn.commit()

    def tear_down(self):
        if SchemaCreator.conn:
            SchemaCreator.conn.close()

