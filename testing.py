


import sqlite3
from sqlite3 import Error

conn = None

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
    
    for group in entity_groups:




except Error as e:
    print(e)
finally:
    if conn:
        conn.close()


