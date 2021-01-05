








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

sentence = "Today's date is 06/06/2018 and also 01-12-2021 and also 2020-01-01 and also 1999/31/31"

dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'(\s\w+\s\d{1,2},\s\d{4})')

regex_results = []
entity_list = []

# entity_list.append(
#     {
#         "index": begin_idx,
#         "name": json_entity['entity_group'],
#         "value": json_entity['word'],
#         "begin_idx": begin_idx,
#         "end_idx": end_idx
#     }
# )


results1 = re.findall(dateRegEx1, sentence) 

#also test if there is no error
for result in results1:    
    try:
        dt = parse(result[0].strip())
        begin_idx = sentence.index(result[0].strip())
        end_idx = begin_idx + len(result[0].strip())
        print(dt.date())
    except ValueError:
        pass

results2 = re.findall(dateRegEx2, "On November 15, 2019 he went and got something ")

for result in results2:
    try:
        dt = parse(result.strip())
        print(dt.date())
    except ValueError:
        pass



