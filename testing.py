

# from transformers import  pipeline

# sentence = "NEWS ANALYSIS Sylvia Carr P2P NOW FOR BIZ"
# #dslim/bert-base-NER
# ner_pipeline = pipeline("ner", grouped_entities=True)
# result = ner_pipeline(sentence)
# stop = "stop"


this_list = [1, 2, 3, 4, 5]

for i, item1 in enumerate(this_list):      
    j = i + 1
    while j < len(this_list):         
        print("(" + str(item1) + " " + str(this_list[j]) + ")")
        j = j + 1

