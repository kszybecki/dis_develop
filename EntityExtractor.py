

import re
from transformers import  pipeline
import json

#on use entities where the confidence threashold is above 60%
CONFIDENCE_THREASHOLD = .60

sequence2 = "I am Kris Szybecki and I work at Agilent Inc. but also worked at Manitoba Hydro. "
# This works
# nlp = pipeline("ner", grouped_entities=True)
# result = nlp(sequence2)
# for r in result:
#     print(r["entity_group"] + " " + r["word"])



results = []
results.append('{"entity_group": "I-PER", "score": 0.59, "word": "Kris Szybecki"}')
results.append('{"entity_group": "I-ORG", "score": 0.9987585544586182, "word": "Agilent Inc"}')
results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')
results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')

no_duplicates = []

for entity in results:
    json_entity = json.loads(entity)
    if float(json_entity['score']) < CONFIDENCE_THREASHOLD:
        continue  
      
    length = len(list(filter(lambda x: x['word'] == json_entity['word'], no_duplicates)))
    if length == 0:
        no_duplicates.append(json_entity)








#-----------------------

#extracting entities other than ones by NER

# to extract dates but only in number form
# dateRegEx = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
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



