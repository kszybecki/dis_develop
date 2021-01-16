

import time
import TextProvider
import NerReExtractor
import SchemaCreator
import re

SCHEMA_TYPE = "Relational"

sentence_log_file = open(r"C:\\master_repos\\dis_develop\\logs\sentence_log.txt", "a")

text_provider = TextProvider.TextProvider()
ner_re_extractor = NerReExtractor.NerReExtractor()
schema_creator = SchemaCreator.SchemaCreator(SCHEMA_TYPE)

#t_start = time.time()
while(text_provider.has_next()):
    text = text_provider.get_next()
    # split text into sentences and remove spaces
    sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
    # filter out empty string list items
    sentences = list(filter(lambda x: x.strip() != '', sentences))  

    for sentence in sentences:        
        print( sentence + "\n")
        #sentence_log_file.write(sentence + "\n\n")

        """ 
        perform sentence level extraction
        include index of sentence as a key for joining entities to sentences
        """   
        entities = ner_re_extractor.get_entities(sentence)

        if SCHEMA_TYPE == "Relational":   
            schema_creator.insert_relational_entities(entities, sentence)
            #since 2 entities are required to predict relations, ignore sentences less than 3 words in length
            # if len(sentence["value"].split()) < 3:
            #     continue
            # relations = ner_re_extractor.get_relations(entities, sentence)  

        
sentence_log_file.close()
schema_creator.tear_down()

    


# AT THE END TO RECORD TIME IT TOOK
#t_stop = time.time()
#print((t_stop - t_start) / 60)
