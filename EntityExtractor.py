

import re
import json
from transformers import  pipeline
from dateutil.parser import parse


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
        begin_idx = sentence1.index(json_entity['word'])
        end_idx = begin_idx + len(json_entity['word'])
        entity_list.append(
            {
                "index": begin_idx,
                "name": json_entity['entity_group'],
                "value": json_entity['word'],
                "begin_idx": begin_idx,
                "end_idx": end_idx
            }
        )





# regex for emails
# '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'



