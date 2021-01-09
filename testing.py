

import re
from dateutil.parser import parse

sentence = "The first date is but kris@hydro.ca today's date is 06/06/2018 Nov 15, 2015  and On also 01-12-2021 and also 2020-01-01 and also 1999/31/31 "
#sentence = "The first date is but today's date is"

dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'(\s\w+\s\d{1,2},\s\d{4})')
emailRegEx = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+')

regex_results = []
entity_list = []

def get_insert_index(begin_idx):
    index = 0
    if len(entity_list) == 0:
        return 0        
    for index, item in enumerate(entity_list):
        idx = item['begin_idx']
        if begin_idx < idx:
           return index
    return (index + 1)  

def insert_entities(regex_results, entity_type):
    for result in regex_results:    
        try:
            result_string = ""
            entity_value = ""

            if type(result) is tuple:
                result_string = result[0].strip()
            else:
                result_string = result.strip()
                
            if entity_type == "DATE":                
                entity_value = str(parse(result_string).date())
            else:
                entity_value = result_string
                            
            begin_idx = sentence.index(result_string)
            end_idx = begin_idx + len(result_string)

            #get insert index to perserve order the entities appeard in, in the sentence
            insert_index = get_insert_index(begin_idx)
            entity_list.insert(insert_index, 
                {
                    "name": entity_type,
                    "value": entity_value,
                    "begin_idx": begin_idx,
                    "end_idx": end_idx
                }
            )
        except ValueError:
            pass  

regex_results = re.findall(dateRegEx1, sentence) 
regex_results.extend(re.findall(dateRegEx2, sentence))
insert_entities(regex_results, "DATE")

regex_results = re.findall(emailRegEx, sentence)
insert_entities(regex_results, "EMAIL")


