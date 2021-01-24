#This reads in the Enron Email dataset

import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
import email
import mailparser
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class TextProvider:

    rootdir = "C:\\master_repos\\dis_develop\\enron_email_dataset"

    file_name_list = []
    name_dir_list = []    

    name_dir_idx = 0
    file_idx = -1

    #constructor
    def __init__(self):
        TextProvider.name_dir_list = os.listdir(self.rootdir)
        directory = Path(self.rootdir + "\\" + TextProvider.name_dir_list[0] + "\\inbox")
        files_to_read = list(filter(lambda y:y.is_file(), directory.iterdir()))        
        TextProvider.file_name_list = sorted(files_to_read, key=lambda x: int(x.name.replace("_", "")))

    #checks whethere more name dir exist to inspect
    def has_next(self):

        len_name_dir_list = len(TextProvider.name_dir_list)
        len_file_name_list = len(TextProvider.file_name_list)

        if TextProvider.file_idx == (len_file_name_list - 1) and (TextProvider.name_dir_idx + 1) == len_name_dir_list:
            #no more name folders to inspect
            return False
        elif TextProvider.file_idx < (len_file_name_list - 1):
            #next file
            TextProvider.file_idx += 1 
            return True
        elif TextProvider.file_idx == (len_file_name_list - 1):
            #last file in inbox, thus increase name_dir_idx
            TextProvider.file_idx = 0            
            self.set_file_name_list()

            return True

    def set_file_name_list(self):
        TextProvider.name_dir_idx += 1 
        TextProvider.file_name_list = []
        directory = Path(self.rootdir + "\\" + TextProvider.name_dir_list[TextProvider.name_dir_idx] + "\\inbox")

        #keep iterating until valid inbox directory found
        while os.path.exists(directory) == False:
            TextProvider.name_dir_idx += 1 
            directory = Path(self.rootdir + "\\" + TextProvider.name_dir_list[TextProvider.name_dir_idx] + "\\inbox")
        
        files_to_read = list(filter(lambda y:y.is_file(), directory.iterdir()))        
        TextProvider.file_name_list = sorted(files_to_read, key=lambda x: int(x.name.replace("_", "")))                    

    def get_current_file_name(self):
        return TextProvider.file_name_list[TextProvider.file_idx]
    
    def get_next_email_text(self):        
        file_name = TextProvider.file_name_list[TextProvider.file_idx] 
        print(file_name)
        mail = mailparser.parse_from_file(file_name)
        body_list = mail.body.splitlines()
        return self.clean_text2(body_list)

    def clean_text2(self, body_list):
        sentence_list = []        
        for text in body_list:
            text = text.replace("'", "")
            text = text.replace("`", "")
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
               sentence_list.append(text) 

        return sentence_list
                



        
