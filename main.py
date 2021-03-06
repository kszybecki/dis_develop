


import TextProvider
import NerReExtractor
import SchemaCreator
import re
from datetime import datetime


SCHEMA_TYPE = "DataWarehouse"

sentence_log_file_path = r"C:\\master_repos\\dis_develop\\logs\\sentence_log.txt"
relation_log_file_path = r"C:\\master_repos\\dis_develop\\logs\\relation_log.txt"
timer_file_path = r"C:\\master_repos\\dis_develop\\logs\\data_warehouse_time_log.txt"

text_provider = TextProvider.TextProvider()
ner_re_extractor = NerReExtractor.NerReExtractor()
schema_creator = SchemaCreator.SchemaCreator(SCHEMA_TYPE)

t_start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
timer_log_file = open(timer_file_path, "a")
timer_log_file.write("start: " + t_start + "\n\n")
timer_log_file.close()

while(text_provider.has_next()):
    body_list = text_provider.get_next_email_text()
    schema_creator.insert_current_file_name(text_provider.get_current_file_name())
    for paragraph in body_list:
        sentences = list(map(str.strip, re.split(r'\.[ ]+?', paragraph)))        
        for sentence in sentences:
            words_in_sentence = len(sentence.split(" "))
            if sentence == '':
                continue
            if SCHEMA_TYPE == "Relational" and words_in_sentence < 2:
                continue
            sentence_log_file = open(sentence_log_file_path, "a")
            sentence_log_file.write(sentence + "\n\n")
            sentence_log_file.close()

            entities = ner_re_extractor.get_entities(sentence)

            if SCHEMA_TYPE == "Relational":      
                schema_creator.insert_relational_schema(entities, sentence)          
                #since 2 entities are required to predict relations, ignore entities list with less than 2
                if len(entities)> 1:
                    relations = ner_re_extractor.get_relations(entities, sentence)  
                    if len(relations) > 0:
                        schema_creator.insert_relations(relations)
                        for relation in relations:
                            relation_log_file = open(relation_log_file_path, "a")
                            relation_log_file.write(relation["relation"] + "\n")
                            relation_log_file.close()
            else:
                schema_creator.insert_into_data_warehouse_schema(entities)

schema_creator.tear_down()

t_end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
timer_log_file = open(timer_file_path, "a")
timer_log_file.write("end: " + t_end + "\n\n")
timer_log_file.close()
print("Done!")  

