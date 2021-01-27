


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
                self.create_bridge_tables()
                self.create_dimension_tables()
                self.create_sentence_table()
            self.create_email_table()            
        except Error as e:
            print(e)

    def insert_relational_schema(self, entities, sentence):
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
        sql = "INSERT INTO " + table_name + "Sentence (SentenceId, " + table_name + "Id) " + \
            "VALUES (" + str(sentence_id) + ", " + str(entity_id) + ")"
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

    def insert_sentence(self, sentence):
        sentence = sentence.replace("'", "")
        sql = "INSERT INTO Sentence (SourceEmailFileId, Sentence) VALUES (" + str(SchemaCreator.current_SourceEmailFileId) + ", '" + sentence + "')"
        insert_cursor = SchemaCreator.conn.cursor()
        insert_cursor.execute(sql)
        SchemaCreator.conn.commit()
        return insert_cursor.lastrowid

    def create_relation_table(self, relation):
        sql = "CREATE TABLE IF NOT EXISTS " + relation["relation"] + " (" + relation["relation"] + "Id INTEGER PRIMARY KEY)"
        SchemaCreator.conn.cursor().execute(sql)
        SchemaCreator.conn.commit()

        column_names = self.get_relation_column_names(relation)
        
        #check if column exist in relation table, if not create them
        sql = "SELECT COUNT(*) AS CNTREC FROM pragma_table_info('" + relation["relation"] + "') WHERE name='" + \
            column_names["entity1_column_name"] + "'"
        fetch_cursor = SchemaCreator.conn.execute(sql)
        result_row = fetch_cursor.fetchone()
        if result_row[0] == 0:
            self.add_column_to_table(relation["relation"], column_names["entity1_column_name"])

        sql = "SELECT COUNT(*) AS CNTREC FROM pragma_table_info('" + relation["relation"] + "') WHERE name='" + \
            column_names["entity2_column_name"] + "'"
        fetch_cursor = SchemaCreator.conn.execute(sql)
        result_row = fetch_cursor.fetchone()
        if result_row[0] == 0:
            self.add_column_to_table(relation["relation"], column_names["entity2_column_name"])

    def add_column_to_table(self, table_name, column_name):
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
            SchemaCreator.conn.cursor().execute(
                "CREATE TABLE IF NOT EXISTS " + table_name + "Sentence (SentenceId INTEGER, " + table_name + "Id INTEGER)"
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
                    SourceEmailFileId INTEGER,
                    Sentence TEXT
                )
            """
        )
        SchemaCreator.conn.commit()

    def create_email_table(self):
        SchemaCreator.conn.cursor().execute(
            """
                CREATE TABLE IF NOT EXISTS SourceEmailFile (
                    SourceEmailFileId INTEGER PRIMARY KEY,
                    FileName TEXT
                )
            """
        )
        SchemaCreator.conn.commit()

    def insert_current_file_name(self, file_name):
        insert_cursor = SchemaCreator.conn.cursor()
        sql = "INSERT INTO SourceEmailFile (FileName) VALUES ('" + str(file_name) + "')"
        insert_cursor.execute(sql)
        SchemaCreator.conn.commit()
        SchemaCreator.current_SourceEmailFileId = insert_cursor.lastrowid

    def create_fact_table(self):
        SchemaCreator.conn.cursor().execute(
        """ 
            CREATE TABLE IF NOT EXISTS Fact (
                FactId INTEGER PRIMARY KEY,
                PersonBridgeId INTEGER,
                OrganizationBridgeId INTEGER,
                LocationBridgeId INTEGER,
                EmailBridgeId INTEGER,
                DateBridgeId INTEGER
            )
        """
        )
        SchemaCreator.conn.commit()

    def create_bridge_tables(self):
        sql = """
            CREATE TABLE IF NOT EXISTS PersonBridge (
                PersonBridgeId INTEGER,
                DimPersonId INTEGER
            )    
        """
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS OrganizationBridge (
                OrganizationBridgeId INTEGER,
                DimOrganizationId INTEGER
            )    
        """
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS LocationBridge (
                LocationBridgeId INTEGER,
                DimLocationId INTEGER
            )    
        """
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS EmailBridge (
                EmailBridgeId INTEGER,
                DimEmailId INTEGER
            )    
        """
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS DateBridge (
                DateBridgeId INTEGER,
                DimDated INTEGER
            )    
        """
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

    def create_dimension_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS DimPerson (DimPersonId INTEGER PRIMARY KEY, Value TEXT)"
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = "CREATE TABLE IF NOT EXISTS DimLocation (DimLocationId INTEGER PRIMARY KEY, Value TEXT)"
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = "CREATE TABLE IF NOT EXISTS DimOrganization (DimOrganizationId INTEGER PRIMARY KEY, Value TEXT)"
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = "CREATE TABLE IF NOT EXISTS DimDate (DimDateId INTEGER PRIMARY KEY, Value TEXT)"
        SchemaCreator.conn.cursor().execute(sql)    
        SchemaCreator.conn.commit()

        sql = "CREATE TABLE IF NOT EXISTS DimEmail (DimEmailId INTEGER PRIMARY KEY, Value TEXT)"
        SchemaCreator.conn.cursor().execute(sql)    
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

    def insert_into_data_warehouse_schema(self, entity_list):
        entity_groups = self.sort_entity_list_for_dw(entity_list)

        for group in entity_groups:



    def sort_entity_list_for_dw(self, entity_list):
        entity_groups = []
        for entity in entity_list:
            entity_list = sorted(entity_list, key=lambda x: x["name"])            
            entity_group = []
            entity_group_name = entity_list[0]["name"]        

            for index, entity in enumerate(entity_list):            
                if entity["name"] == entity_group_name:
                    entity_group.append(entity)
                else:
                    entity_groups.append(entity_group)
                    entity_group_name = entity["name"]
                    entity_group = []
                    entity_group.append(entity) 

                if index == len(entity_list) - 1:
                    entity_groups.append(entity_group)
        #test this
        return entity_groups

