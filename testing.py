


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

# import os
# from pathlib import Path
# import re

# rootdir = "C:\\master_repos\\dis_develop\\enron_email_dataset"

# name_dir_list = sorted(os.listdir(rootdir))
# directory = Path(rootdir + "\\" + name_dir_list[0] + "\\inbox")
# files_to_read = list(filter(lambda y:y.is_file(), directory.iterdir()))

# file_name_list = sorted(files_to_read, key=lambda x: int(x.name.replace("_", "")))
# file_name = str(files_to_read[0])

# stop = ""

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

text = "Thanks!"

text_length = len(text.split(" "))
if ("-----Original Message-----" not in text and 
    "From:" not in text and 
    "To:" not in text and
    "Subject:" not in text and 
    "Sent" not in text and
    "Cc:" not in text and
    "<<" not in text and
    "\t" not in text and
    "- Forwarded" not in text and
    "> > > > >" not in text and
    "http://" not in text and
    "******************ELSEWHERE ON ZDNET!******************" not in text and
    "<!--" not in text and "-->" not in text and
    "align=\"" not in text and
    "width=\"" not in text and
    not bool(BeautifulSoup(text, "html.parser").find()) and 
    text_length > 2):
    print("Yes")
