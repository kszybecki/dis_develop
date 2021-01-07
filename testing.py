








#contains the following format:
# {
#   "entities": [<entity 1>, <entity 2>], 
#   "key2": [4, 5, 6]
# }


# entities list contains
#  each entity pair:  
#    key => entity name ("per", "loc", "date"), value being entity instance
#    key => "relation": "<relation value>"
#    key => "sentence": "<sentence where this appeared>"
#    key => "sentence_id": "<unique id for sentence>"
#           each sentence should have a unique value as to not duplicate them
#   

import re
from dateutil.parser import parse

#sentence = "The first date is but today's date is 06/06/2018   and On also 01-12-2021  and also 2020-01-01 and also 1999/31/31 "
sentence = "The first date is but today's date is"

dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'(\s\w+\s\d{1,2},\s\d{4})')

regex_results = []
entity_list = []

        # entity_list.append(
        #     {
        #         "name": json_entity['entity_group'],
        #         "value": json_entity['word'],
        #         "begin_idx": begin_idx,
        #         "end_idx": end_idx
        #     }
        # )


def get_insert_index(begin_idx):
    index = 0
    if len(entity_list) == 0:
        return 0        
    for index, item in enumerate(entity_list):
        idx = item['begin_idx']
        if begin_idx < idx:
           return index
    return (index + 1)    

results = re.findall(dateRegEx1, sentence) 

#also test if there is no error
for result in results:    
    try:
        dt = parse(result[0].strip())
        begin_idx = sentence.index(result[0].strip())
        end_idx = begin_idx + len(result[0].strip())

        #get insert index to perserve order the entities appeard in, in the sentence
        insert_index = get_insert_index(begin_idx)
        entity_list.insert(insert_index, 
            {
                "name": "DATE",
                "value": str(dt.date()),
                "begin_idx": begin_idx,
                "end_idx": end_idx
            }
        )
    except ValueError:
        pass

results = re.findall(dateRegEx2, sentence)

for result in results:
    try:
        dt = parse(result.strip())
        begin_idx = sentence.index(result.strip())
        end_idx = begin_idx + len(result.strip())

        #get insert index to perserve order the entities appeard in, in the sentence
        insert_index = get_insert_index(begin_idx)
        entity_list.insert(insert_index, 
            {
                "name": "DATE",
                "value": str(dt.date()),
                "begin_idx": begin_idx,
                "end_idx": end_idx
            }
        )
    except ValueError:
        pass

stop = "stop"

