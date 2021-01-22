

# "I-PER"   # Person's name
# "I-ORG"   # Organisation
# "I-LOC"    # Location
# "DATE"     # Date 
# "EMAIL"    # Email


import re
import json
from transformers import  pipeline
from dateutil.parser import parse

class EntityExtractor:

    CONFIDENCE_THRESHOLD = .60    

    dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
    dateRegEx2 = re.compile(r'\s\w+\s\d{1,2},\s\d{4}')
    emailRegEx = re.compile(r'[\w\.-]+@[\w\.-]+(?:\.[\w]+)+')
    entity_log_base_path = r"C:\\master_repos\\dis_develop\\logs\\"

    ner_results = []
    regex_results = []
    entity_list = []
    ner_pipeline = ""
    
    def __init__(self):
        #initialize pre-trained name entitiy recognition model
        EntityExtractor.ner_pipeline = pipeline("ner", grouped_entities=True)

    def get_entities_from_sentence(self, sentence):
        EntityExtractor.entity_list = [] 
        self.extract_entities_using_model(sentence)
        self.insert_ner_entities(sentence)
        EntityExtractor.regex_results = re.findall(EntityExtractor.dateRegEx1, sentence) 
        EntityExtractor.regex_results.extend(re.findall(EntityExtractor.dateRegEx2, sentence))
        self.insert_regex_entities("DATE", sentence)
        EntityExtractor.regex_results = re.findall(EntityExtractor.emailRegEx, sentence)
        self.insert_regex_entities("EMAIL", sentence)

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

    def extract_entities_using_model(self, sentence):
        EntityExtractor.ner_results = EntityExtractor.ner_pipeline(sentence)

    def insert_ner_entities(self, sentence):
        for entity in EntityExtractor.ner_results:

            #ignore entities that contain partial results
            #ignore enities which have a MISC classification
            if "#" in entity["word"] or "MISC" in entity["entity_group"]:
                continue

            #remove entities with score less than CONFIDENCE_THRESHOLD
            if float(entity["score"]) < EntityExtractor.CONFIDENCE_THRESHOLD:
                continue  

            #filter out duplicate entities
            length = len(list(filter(lambda x: x['value'] == entity["word"], EntityExtractor.entity_list)))
            if length == 0:
                try:                    
                    begin_idx = sentence.index(entity["word"])
                    end_idx = begin_idx + len(entity["word"])
                    entity_name = self.exchange_entity_name(entity["entity_group"])

                    EntityExtractor.entity_list.append({
                            "name": entity_name,
                            "value": entity["word"],
                            "begin_idx": begin_idx,
                            "end_idx": end_idx                 
                    })
                    #log entity for validation
                    self.log_entity(entity)
                except: # if the predicted entity instance cannot be found in the sentence, ignore sentence
                    continue

    def insert_regex_entities(self, entity_type, sentence):
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
                                
                begin_idx = sentence.index(result_string)
                end_idx = begin_idx + len(result_string)

                #get insert index to perserve order the entities appeard in, in the sentence
                insert_index = self.get_insert_index(begin_idx)
                EntityExtractor.entity_list.insert(insert_index, {
                        "name": entity_type,
                        "value": entity_value,
                        "begin_idx": begin_idx,
                        "end_idx": end_idx                 
                })
            except:
                pass  

    def exchange_entity_name(self, value):
        if value == "I-ORG" or value == "B-ORG":
            return "Organization"
        if value == "I-PER" or value == "B-PER":
            return "Person"
        if value == "I-LOC" or value == "B-LOC":
            return "Location"
        if value == "DATE":
            return "Date"
        if value == "EMAIL":
            return "Email"

    def log_entity(self, entity):
        file_name = "entity_" + entity["entity_group"] + "_log.txt"
        entity_log_file = open(EntityExtractor.entity_log_base_path + file_name, "a")
        entity_log_file.write(entity["word"] + "\n")
        entity_log_file.close()
