


import sys
sys.path.insert(0, 'C:\\master_repos\\dis_develop\\OpenNRE')

import opennre

class RelationExtractor:

    model = "model"

    #constructor
    def __init__(self):
        RelationExtractor.model = opennre.get_model('wiki80_bert_softmax')




    def get_entity_list(self, entity_list):
        test = entity_list


    

    # result = model.infer({'text': 'He was the son of Máel Dúin mac Máele Fithrich, and grandson of the high king Áed Uaridnach (died 612).', 'h': {'pos': (18, 46)}, 't': {'pos': (78, 91)}})

    # print(result)



    