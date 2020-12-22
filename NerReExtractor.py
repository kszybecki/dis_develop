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
# ]


import sys
sys.path.insert(0, 'C:\\master_repos\\dis_develop\\OpenNRE')

import re 
from transformers import  pipeline
import opennre

class NerReExtractor:

    re_model = ""
    nlp_model = ""
    sentence = ""

    #contains the following format:
    # {
    #   "entities": [<entity 1>, <entity 2>], 
    #   "key2": [4, 5, 6]
    # }
    result = ""

    #constructor
    def __init__(self):
        #initialize pre-trained models
        NerReExtractor.re_model = opennre.get_model('wiki80_bert_softmax')
        NerReExtractor.nlp_model = pipeline("ner", grouped_entities=True)

    def get_result(self, sentence):
        return ""

    def extract_entity_pair(self, sentence):
        #should I take the entities in a sentence with the greatest accuracy confidence?
        return NerReExtractor.nlp_model(sentence)

    def extract_relation(self, sentence, entity1_idx, entity2_idx):
        return NerReExtractor.re_model.infer({'text': sentence, 'h': {'pos': (entity1_idx.start, entity1_idx.end)}, 't': {'pos': (entity2_idx.start, entity2_idx.end)}})