




import sqlite3
from sqlite3 import Error
import os
import sys


def create_table(file):
    sql = "CREATE TABLE IF NOT EXISTS " + file["table_name"] + " (Value TEXT)"

def insert_value(file, value):
    sql "INSERT INTO " + file["table_name"] + " (Value) VALUES (" + value + ")"


conn = None
try:
    conn = sqlite3.connect("C:\\master_repos\\dis_develop\\SQLite\\evaluation.db")
    
    log_files = []

    #relation log files
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\relational_logs\\entity_B-LOC_log.txt", "table_name": "RelBLocation"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\relational_logs\\entity_I-LOC_log.txt", "table_name": "RelILocation"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\relational_logs\\entity_I-ORG_log.txt", "table_name": "RelIOrganization"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\relational_logs\\entity_I-PER_log.txt", "table_name": "RelIPerson"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\relational_logs\\relation_log.txt", "table_name": "RelRelation"})

    #data warehouse log files
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\data_warehouse\\entity_B-LOC_log.txt", "table_name": "DwBLoc"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\data_warehouse\\entity_I-LOC_log.txt", "table_name": "DwlILoc"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\data_warehouse\\entity_I-ORG_log.txt", "table_name": "DwlIOrg"})
    log_files.append({"path": "C:\\master_repos\\dis_develop\\logs\\data_warehouse\\entity_I-PER_log.txt", "table_name": "DwlIPer"})

    for file in log_files:      
        with open(file["path"], "r") as a_file:
            create_table(file)
            for line in a_file:
                stripped_line = line.strip()
                insert_value(file, stripped_line)





except Error as e:
    print(e)
finally:
    if conn:
        conn.close()

