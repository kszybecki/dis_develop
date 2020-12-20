






#class ExtractEntitiesAndRelations:



import sys
sys.path.insert(0, 'C:\\master_repos\\disseration_develop_old\\OpenNRE')

import opennre

model = opennre.get_model('wiki80_bert_softmax')

result = model.infer({'text': 'He was the son of Máel Dúin mac Máele Fithrich, and grandson of the high king Áed Uaridnach (died 612).', 'h': {'pos': (18, 46)}, 't': {'pos': (78, 91)}})

print(result)



    