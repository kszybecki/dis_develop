

import re
import json
from transformers import  pipeline
from dateutil.parser import parse


CONFIDENCE_THREASHOLD = .60
dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'\s\w+\s\d{1,2},\s\d{4}')
emailRegEx = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')

sentence = "I am Kris Szybecki and I work at Agilent Inc. 06/06/2018  but also worked at Manitoba Hydro since July 4, 2005 . "
#sentence2 = "I Kris Szybecki where born on July 4, 2005 and my email address is smokerjones@pm.me

# This works
# nlp = pipeline("ner", grouped_entities=True)
# result = nlp(sequence2)
# for r in result:
#     print(r["entity_group"] + " " + r["word"])

ner_results = []
regex_results = []
entity_list = []

ner_results.append('{"entity_group": "I-PER", "score": 0.9987585544586182, "word": "Kris Szybecki"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9987585544586182, "word": "Agilent Inc"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')

def get_insert_index(begin_idx):
    index = 0
    if len(entity_list) == 0:
        return 0        
    for index, item in enumerate(entity_list):
        idx = item['begin_idx']
        if begin_idx < idx:
           return index
    return (index + 1)    

#this is good
for entity in ner_results:
    json_entity = json.loads(entity)

    #remove entities with score less than CONFIDENCE_THREASHOLD
    if float(json_entity['score']) < CONFIDENCE_THREASHOLD:
        continue  

    #filter out duplicate entities
    length = len(list(filter(lambda x: x['value'] == json_entity['word'], entity_list)))
    if length == 0:
        begin_idx = sentence.index(json_entity['word'])
        end_idx = begin_idx + len(json_entity['word'])
        entity_list.append(
            {
                "name": json_entity['entity_group'],
                "value": json_entity['word'],
                "begin_idx": begin_idx,
                "end_idx": end_idx
            }
        )

regex_results = re.findall(dateRegEx1, sentence) 
for result in regex_results:    
    try:
        date_value = ""
        if isinstance(result, list):
            date_value = result[0].strip()
        else:
            date_value = parse(result.strip())
            
        dt = parse(date_value)        
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

regex_results = re.findall(dateRegEx2, sentence)
for result in regex_results:
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



