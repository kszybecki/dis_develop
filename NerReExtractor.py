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

    sentence = ""
    entity_extractor = EntityExtractor.EntityExtractor()
    ner_re = []

    #constructor
    def __init__(self):
        #initialize pre-trained relation extraction model from opennre
        NerReExtractor.re_model = opennre.get_model('wiki80_bert_softmax')

    def get_entities_and_relations(self, sentence):
        NerReExtractor.sentence = sentence
        entity_list = NerReExtractor.entity_extractor.get_entities_from_sentence(sentence)

        # since 2 entities are required for relation extraction, skip extraction for entity_list with one entity
        if len(entity_list) > 1:
            #strategy for relation extraction
            relations = []
            for i, entity1 in enumerate(entity_list):      
                j = i + 1
                while j < len(entity_list): 
                    # entity1 is the parent relation        
                    entity2 = entity_list[j]
                    relation = self.extract_relation(entity1["begin_idx"], entity2["end_idx"])

                    if relation is not None:

                    j = j + 1

                NerReExtractor.ner_re.append({
                    "name": entity1["name"],
                    "sentence_id": entity1["sentence_id"],
                    "relations": relations
                })

        #     self.extract_relation(NerReExtractor.sentence, 1, 1)

        
        return ""


    def extract_relation(self, entity1_idx, entity2_idx):
        result = NerReExtractor.re_model.infer({'text': NerReExtractor.sentence, \
                                              'h': {'pos': (entity1_idx.start, entity1_idx.end)}, \
                                              't': {'pos': (entity2_idx.start, entity2_idx.end)}})
        
        return result
