# label_list = [
#     "O",       # Outside of a named entity
#     "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
#     "I-MISC",  # Miscellaneous entity
#     "B-PER",   # Beginning of a person's name right after another person's name
#     "I-PER",   # Person's name
#     "B-ORG",   # Beginning of an organisation right after another organisation
#     "I-ORG",   # Organisation
#     "B-LOC",   # Beginning of a location right after another location
#     "I-LOC"    # Location
#     "DATE"     # Date 
#     "EMAIL"    # Email
# ]


import sys
sys.path.insert(0, 'C:\\master_repos\\dis_develop\\OpenNRE')

from transformers import  pipeline
import opennre
import EntityExtractor
import json

class NerReExtractor:

    entity_extractor = EntityExtractor.EntityExtractor()
    RE_CONFIDANCE_THRESHOLD = .60

    #constructor
    def __init__(self):
        #initialize pre-trained relation extraction model from opennre
        NerReExtractor.re_model = opennre.get_model('wiki80_bert_softmax')

    def get_entities(self, sentence):
        entities = NerReExtractor.entity_extractor.get_entities_from_sentence(sentence)
        return entities

    def get_relations(self, entity_list, sentence):
        relations = []
        # since 2 entities are required for relation extraction, skip extraction for entity_list with one entity
        if len(entity_list) > 1:
            #extract relation for all permutations of entities
            
            for i, entity1 in enumerate(entity_list):      
                j = i + 1
                while j < len(entity_list):        
                    entity2 = entity_list[j]
                    #here I can put in counts to see of the potential candidates, how many relations where actually found
                    relation = self.extract_relation(entity1, entity2, sentence)    

                    if relation[1] > NerReExtractor.RE_CONFIDANCE_THRESHOLD:
                        relation[0].replace(" ", "_")
                        #if relation is not None:
                        
                        relations.append({
                            "entity1_name": entity1["name"],
                            "entity1_value": entity1["value"],
                            "entity2_name": entity2["name"],
                            "entity2_value": entity2["value"],
                            "relation": relation[0]
                        })

                    j = j + 1      

        return relations

    def extract_relation(self, entity1, entity2, sentence):         
        result = NerReExtractor.re_model.infer({'text': sentence["value"], \
             'h': {'pos': (entity1["begin_idx"], entity1["end_idx"])}, \
             't': {'pos': (entity2["begin_idx"], entity2["end_idx"])}})        
        return result
