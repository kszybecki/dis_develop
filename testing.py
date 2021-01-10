

# from transformers import  pipeline

# 
# #dslim/bert-base-NER
# ner_pipeline = pipeline("ner", grouped_entities=True)
# result = ner_pipeline(sentence)
# stop = "stop"


import sys
sys.path.insert(0, 'C:\\master_repos\\dis_develop\\OpenNRE')
import opennre

sentence = "NEWS ANALYSIS Sylvia Carr P2P NOW FOR BIZ"

re_model = opennre.get_model('wiki80_bert_softmax')

result = re_model.infer({'text': sentence, \
        'h': {'pos': (0, 12)}, \
        't': {'pos': (14, 25)}})

stop = "stop"