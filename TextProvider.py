#This reads in the Enron Email dataset

import os
import re
from email.parser import Parser
from pathlib import Path

class TextProvider:

    #adjust directory to your location
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
        TextProvider.file_name_list = files_to_read

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
        TextProvider.file_name_list = files_to_read                      

    def get_next(self):        
        file_name =  TextProvider.file_name_list[TextProvider.file_idx] 
        print(file_name)
        with open(file_name, "r") as f:
            email = Parser().parsestr(f.read()) 
            return self.clean_text(email.get_payload())

    def clean_text(self, text):
        #remove any HTML tags
        clean = re.compile('<.*?>')
        result = re.sub(clean, '', text)

        #remove new-line, tab
        result = result.replace('\n', ' ').replace('\t', ' ')

        #remove URLs 
        result = re.sub(r'http:\/\/.*?[ ]', '', result)

        #remove text with format begins with 2 or more '-----<some text>-----'
        result = re.sub('[-]{2,}[A-Za-z0-9]*[ ][A-Za-z0-9]*[-]{2,}', ' ', result)

        #remove everything inside opening and closing bracket
        result = re.sub(r'\[[A-Za-z0-9]*\]', '', result)

        #remove all other characters not a number or letter except for:
        # ./@-'
        result = re.sub('[^A-Za-z0-9./@-\']', ' ', result)

        #replac multiple space with one space
        result = re.sub('[ ]{2,}', ' ', result)

        return result
        
