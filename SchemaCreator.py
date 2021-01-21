


import os.path
from os import path

import sqlite3
from sqlite3 import Error

class SchemaCreator:


    enron_relational_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_relational_v2.db"
    enron_data_warehouse_path = "C:\\master_repos\\dis_develop\\SQLite\\enron_data_warehouse.db"
    prev_entities = []
    prev_relations = []

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
        sentence_id = -1
        if len(entities) > 0:
            sentence_id = self.insert_sentence(sentence)
        for entity in entities:
            self.create_table(entity)      

            last_row_id = None
            result_row = self.get_entity_from_value(entity)
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

            self.insert_entity_sentence(entity, last_row_id, sentence_id) 

    def insert_relations(self, relations):
        for relation in relations:
            self.rename_relation(relation)
            self.create_relation_table(relation)

            # get entity primary key and check if exists in relatin table
            entity1 = {"name": relation["entity1_name"], "value": relation["entity1_value"]}            
            entity2 = {"name": relation["entity2_name"], "value": relation["entity2_value"]}
            entity1_row = self.get_entity_from_value(entity1)
            entity2_row = self.get_entity_from_value(entity2)
        
            if entity1_row is not None and entity2_row is not None:
                #check if they exist in relation table
                result_row = self.get_relation_from_foreign_keys(relation, entity1_row[0], entity2_row[0])
                if result_row is None:                        
                    self.insert_relation_instance(relation, entity1_row[0], entity2_row[0])


    def insert_relation_instance(self, relation, entity1_id, entity2_id):
        table_name = relation["relation"]
        column_names = self.get_relation_column_names(relation)

        sql = "INSERT INTO " + table_name + " ("+ column_names["entity1_column_name"] + ", " + \
                            column_names["entity2_column_name"] + ") " + \
                            "VALUES (" +  str(entity1_id) + ", " + str(entity2_id) + ")"
        SchemaCreator.conn.cursor().execute(sql)
        SchemaCreator.conn.commit()

    def get_entity_from_value(self, entity):
        table_name = self.get_table_name(entity)
        fetch_cursor = SchemaCreator.conn.execute(
            "SELECT * FROM " + table_name + " WHERE Value = '" + entity["value"] + "'"
        )
        result_row = fetch_cursor.fetchone()
        return result_row

    def get_relation_from_foreign_keys(self, relation, entity1_id, entity2_id):
        column_names = self.get_relation_column_names(relation)        
        entity1_column_name = column_names["entity1_column_name"]
        entity2_column_name = column_names["entity2_column_name"]

        sql = "SELECT " + entity1_column_name + ", " + entity2_column_name + " FROM " + relation["relation"] + \
            " WHERE " + entity1_column_name + " = " + str(entity1_id) + " and " + entity2_column_name + " = " + str(entity2_id)
        fetch_cursor = SchemaCreator.conn.execute(sql)
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
        sentence = sentence.replace("'", "")
        sql = "INSERT INTO Sentence (Sentence) VALUES ('" + sentence + "')"
        insert_cursor = SchemaCreator.conn.cursor()
        insert_cursor.execute(sql)
        SchemaCreator.conn.commit()
        return insert_cursor.lastrowid

    def create_relation_table(self, relation):

        sql = "CREATE TABLE IF NOT EXISTS " + relation["relation"] + " (" + relation["relation"] + "Id INTEGER PRIMARY KEY)"
        SchemaCreator.conn.cursor().execute(sql)
        SchemaCreator.conn.commit()

        column_names = self.get_relation_column_names(relation)
        
        sql = "SELECT COUNT(*) AS CNTREC FROM pragma_table_info('" + relation["relation"] + "') WHERE name='" + \
            column_names["entity1_column_name"] + "'"
        fetch_cursor = SchemaCreator.conn.execute(sql)
        result_row = fetch_cursor.fetchone()
        if result_row[0] == 0:
            self.add_column_to_relation_table(relation["relation"], column_names["entity1_column_name"])

        sql = "SELECT COUNT(*) AS CNTREC FROM pragma_table_info('" + relation["relation"] + "') WHERE name='" + \
            column_names["entity2_column_name"] + "'"
        fetch_cursor = SchemaCreator.conn.execute(sql)
        result_row = fetch_cursor.fetchone()
        if result_row[0] == 0:
            self.add_column_to_relation_table(relation["relation"], column_names["entity2_column_name"])

    def add_column_to_relation_table(self, table_name, column_name):
        sql = "ALTER TABLE " + table_name + " ADD COLUMN " + column_name + " INTEGER"
        SchemaCreator.conn.execute(sql)
        SchemaCreator.conn.commit()

    def create_table(self, entity):
        # create entity table
        length = len(list(filter(lambda x: x["name"] == entity["name"], SchemaCreator.prev_entities)))            
        if length == 0:
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

            SchemaCreator.prev_entities.append(entity)   

    def get_table_name(self, entity):
        if SchemaCreator.schema_type == "Relational":
            return entity["name"]
        else:
            return "Dim" + entity["name"]             

    def rename_relation(self, relation):        
        relation["relation"] = relation["relation"].title().replace(" ", "") + "Relation"
        relation["relation"] = relation["relation"].replace("/", "")

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
    
    def get_relation_column_names(self, relation):
        entity1_column_name = relation["entity1_name"] + "Id"

        if relation["entity1_name"] == relation["entity2_name"]:
            entity2_column_name = relation["entity2_name"] + "2Id"
        else:
            entity2_column_name = relation["entity2_name"] + "Id"

        return {"entity1_column_name": entity1_column_name, "entity2_column_name": entity2_column_name}

    def insert_dimension_entities(self, entities):
        stop = ""