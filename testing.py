








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

import json


results = []
results.append('{"entity_group": "I-PER", "score": 0.59, "word": "Kris Szybecki"}')
results.append('{"entity_group": "I-ORG", "score": 0.9987585544586182, "word": "Agilent Inc"}')
results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')
results.append('{"entity_group": "I-ORG", "score": 0.9990890423456827, "word": "Manitoba Hydro"}')

no_duplicates = []

for entity in results:
    json_entity = json.loads(entity)
      
    length = len(list(filter(lambda x: x['word'] == json_entity['word'], no_duplicates)))
    if length == 0:
        no_duplicates.append(json_entity)