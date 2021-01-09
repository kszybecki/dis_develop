

import re
import json
from transformers import  pipeline
from dateutil.parser import parse

class EntityExtractor:

    CONFIDENCE_THREASHOLD = .60
    dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
    dateRegEx2 = re.compile(r'\s\w+\s\d{1,2},\s\d{4}')
    emailRegEx = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+')

    ner_results = []
    regex_results = []
    entity_list = []
    ner_pipeline = ""
    
    def __init__(self):
        #initialize pre-trained name entitiy recognition model
        EntityExtractor.ner_pipeline = pipeline("ner", grouped_entities=True)

    def get_entities_from_sentence(self, sentence):
        EntityExtractor.entity_list = []

        EntityExtractor.sentence = sentence["sentence"]
        EntityExtractor.sentence_id = sentence["sentence_id"]

        self.extract_entities_using_model()
        self.insert_ner_entities()
        EntityExtractor.regex_results = re.findall(EntityExtractor.dateRegEx1, EntityExtractor.sentence) 
        EntityExtractor.regex_results.extend(re.findall(EntityExtractor.dateRegEx2, EntityExtractor.sentence))
        self.insert_regex_entities("DATE")
        EntityExtractor.regex_results = re.findall(EntityExtractor.emailRegEx, EntityExtractor.sentence)
        self.insert_regex_entities("EMAIL")

        #do I need to log the count of entities found here? for evaluation purposes, 
        #maybe log as a file the counts

        return EntityExtractor.entity_list

    def get_insert_index(self, begin_idx):
        index = 0
        if len(EntityExtractor.entity_list) == 0:
            return 0        
        for index, item in enumerate(EntityExtractor.entity_list):
            idx = item['begin_idx']
            if begin_idx < idx:
                return index

        return (index + 1)    

    def extract_entities_using_model(self):
        EntityExtractor.ner_results = EntityExtractor.ner_pipeline(EntityExtractor.sentence)

    def insert_ner_entities(self):
        for entity in EntityExtractor.ner_results:

            #ignore entities that contain partial results
            if "#" in entity["word"]:
                continue

            #remove entities with score less than CONFIDENCE_THREASHOLD
            if float(entity["score"]) < EntityExtractor.CONFIDENCE_THREASHOLD:
                continue  

            #filter out duplicate entities
            length = len(list(filter(lambda x: x['value'] == entity["word"], EntityExtractor.entity_list)))
            if length == 0:
                begin_idx = EntityExtractor.sentence.index(entity["word"])
                end_idx = begin_idx + len(entity["word"])
                EntityExtractor.entity_list.append({
                        "name": entity["entity_group"],
                        "value": entity["word"],
                        "begin_idx": begin_idx,
                        "end_idx": end_idx,
                        "sentence_id": EntityExtractor.sentence_id                    
                })

    def insert_regex_entities(self, entity_type):
        for result in EntityExtractor.regex_results:    
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
                                
                begin_idx = EntityExtractor.sentence.index(result_string)
                end_idx = begin_idx + len(result_string)

                #get insert index to perserve order the entities appeard in, in the sentence
                insert_index = self.get_insert_index(begin_idx)
                EntityExtractor.entity_list.insert(insert_index, {
                        "name": entity_type,
                        "value": entity_value,
                        "begin_idx": begin_idx,
                        "end_idx": end_idx,
                        "sentence_id": EntityExtractor.sentence_id                    
                })
            except ValueError:
                pass  

