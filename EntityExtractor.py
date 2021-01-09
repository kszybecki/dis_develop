

import re
import json
from transformers import  pipeline
from dateutil.parser import parse

class EntityExtractor:

    CONFIDENCE_THREASHOLD = .60
    dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
    dateRegEx2 = re.compile(r'\s\w+\s\d{1,2},\s\d{4}')
    emailRegEx = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+')

    sentence = "I am Kris Szybecki and I work at Agilent Inc. 06/06/2018  but also worked at smokerjones@pm.me Manitoba Hydro since July 4, 2005 . "

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

    def get_insert_index(self, begin_idx):
        index = 0
        if len(EntityExtractor.entity_list) == 0:
            return 0        
        for index, item in enumerate(EntityExtractor.entity_list):
            idx = item['begin_idx']
            if begin_idx < idx:
                return index

        return (index + 1)    

    def insert_ner_entities(self, ner_results):
        for entity in ner_results:
            json_entity = json.loads(entity)

            #remove entities with score less than CONFIDENCE_THREASHOLD
            if float(json_entity['score']) < EntityExtractor.CONFIDENCE_THREASHOLD:
                continue  

            #filter out duplicate entities
            length = len(list(filter(lambda x: x['value'] == json_entity['word'], EntityExtractor.entity_list)))
            if length == 0:
                begin_idx = sentence.index(json_entity['word'])
                end_idx = begin_idx + len(json_entity['word'])
                EntityExtractor.entity_list.append(
                    {
                        "name": json_entity['entity_group'],
                        "value": json_entity['word'],
                        "begin_idx": begin_idx,
                        "end_idx": end_idx
                    }
                )

    def insert_regex_entities(self, regex_results, entity_type):
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
                insert_index = self.get_insert_index(begin_idx)
                EntityExtractor.entity_list.insert(insert_index, 
                    {
                        "name": entity_type,
                        "value": entity_value,
                        "begin_idx": begin_idx,
                        "end_idx": end_idx
                    }
                )
            except ValueError:
                pass  

# insert_ner_entities(ner_results)

# regex_results = re.findall(dateRegEx1, sentence) 
# regex_results.extend(re.findall(dateRegEx2, sentence))
# insert_regex_entities(regex_results, "DATE")

# regex_results = re.findall(emailRegEx, sentence)
# insert_regex_entities(regex_results, "EMAIL")


stop = "stop"



