


import sqlite3
from sqlite3 import Error

conn = None

schema_type = "DataWarehouse"

def get_table_name(entity):
    if schema_type == "Relational":
        return entity["name"]
    else:
        return "Dim" + entity["name"]   

def get_entity_from_value(entity):
    table_name = get_table_name(entity)
    sql = "SELECT * FROM " + table_name + " WHERE Value = '" + entity["value"] + "'"
    fetch_cursor = conn.execute(sql)
    result_row = fetch_cursor.fetchone()
    return result_row

def get_next_id_from_bridge_table(group_name):
    key_column_name = group_name + "BridgeId"
    table_name = group_name + "Bridge"
    sql = "SELECT MAX(" + key_column_name + ") FROM " + table_name
    fetch_cursor = conn.execute(sql)
    conn.commit()
    result_row = fetch_cursor.fetchone()
    if result_row[0] is not None:
        next_id = int(result_row[0]) + 1
        return next_id
    else:
        return 1    

def insert_into_dimension_table(entity, group_id):
    result_row = get_entity_from_value(entity)
    dim_table_name = "Dim" + entity["name"]
    dim_table_key_column_name = "Dim" + entity["name"] + "Id"
    last_row_id = -1
    if result_row is None:           
        sql = "INSERT INTO " + dim_table_name + " (Value) VALUES ('" + entity["value"] + "')"
        insert_cursor = conn.cursor()
        insert_cursor.execute(sql)
        conn.commit()
        last_row_id = insert_cursor.lastrowid
    else: 
        last_row_id = result_row[0]

    bridge_key_column_name = entity["name"] + "BridgeId"
    bridge_table_name = entity["name"] + "Bridge"
    sql = "INSERT INTO " + bridge_table_name + " (" + bridge_key_column_name + "," + dim_table_key_column_name + ") " \
          "VALUES (" + str(group_id) + "," + str(last_row_id) + ")"
    conn.execute(sql)
    conn.commit()

def insert_into_fact_table(fact):
    column_names = ""
    column_key_values = ""
    for dim in fact:
        column_names = column_names + dim["column_name"] + ","
        column_key_values = column_key_values + str(dim["group_id"]) + ","

    column_names = column_names[0:(len(column_names) - 1)]
    column_key_values = column_key_values[0:(len(column_key_values) - 1)]

    sql = "INSERT INTO Fact (" + column_names + ") VALUES (" + column_key_values + ")"
    conn.execute(sql)
    conn.commit()


try:
    conn = sqlite3.connect("C:\\master_repos\\dis_develop\\SQLite\\data_warehouse_test.db")

    entity_list = []

    entity_groups = []
    entity_group = []

    entity_group.append({"name": "Organization","value": "Org A"})
    entity_group.append({"name": "Organization","value": "Org B"})
    entity_groups.append(entity_group)

    entity_group = []
    entity_group.append({"name": "Location","value": "Loc B"})
    entity_group.append({"name": "Location","value": "Loc A"})
    entity_groups.append(entity_group)

    entity_group = []
    entity_group.append({"name": "Person","value": "Person A"})
    entity_groups.append(entity_group)  

    fact = []
    for group in entity_groups:
        group_name = group[0]["name"]
        group_id = get_next_id_from_bridge_table(group_name)
        fact.append({"column_name": group_name + "BridgeId", "group_id": group_id })
        for entity in group:
            insert_into_dimension_table(entity, group_id)

    insert_into_fact_table(fact)







except Error as e:
    print(e)
finally:
    if conn:
        conn.close()


