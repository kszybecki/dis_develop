

import re
from transformers import  pipeline
import json

#only use entities where the confidence threashold is above 60%
CONFIDENCE_THREASHOLD = .60
dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'\s\w+\s\d{1,2},\s\d{4}')
emailRegEx = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')

sentence1 = "I am Kris Szybecki and I work at Agilent Inc. but also worked at Manitoba Hydro. "
sentence2 = "I Kris Szybecki where born on July 4, 2005 and my email address is smokerjones@pm.me"

# This works
# nlp = pipeline("ner", grouped_entities=True)
# result = nlp(sequence2)
# for r in result:
#     print(r["entity_group"] + " " + r["word"])

entity = {
    "entity_group": "I-PER", 
    "word": "Kris Szybecki",
    "begin_idx": 5,
    "end_idx": 10
}


ner_results = []
regex_results = []
entity_list = []

ner_results.append('{"entity_group": "I-PER", "score": 0.9987585544586182, "word": "Kris Szybecki"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9987585544586182, "word": "Agilent Inc"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')
ner_results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')

for entity in ner_results:
    json_entity = json.loads(entity)

    #remove entities with score less than CONFIDENCE_THREASHOLD
    if float(json_entity['score']) < CONFIDENCE_THREASHOLD:
        continue  

    #filter out duplicate entities
    length = len(list(filter(lambda x: x['value'] == json_entity['word'], entity_list)))
    if length == 0:
        #store begin and end index for each entity
        begin_idx = sentence1.index(json_entity['word'])
        end_idx = begin_idx + len(json_entity['word'])
        entity_list.append(
            {
                "name": json_entity['entity_group'],
                "value": json_entity['word'],
                "begin_idx": begin_idx,
                "end_idx": end_idx
            }
        )








#-----------------------

#extracting entities other than ones by NER

# to extract dates but only in number form
# mo = dateRegEx.search('Today''s date is 06/06/2018') 
# print(mo.group(1)) 

#Sep|September 1, 2019
# you don't know the context of the date 
# but you can see which sentence 
# result = re.findall(r'\s\w+\s\d{1,2},\s\d{4}', sequence2)
# for r in result:
#     print(r)

# regex for emails
# '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'



