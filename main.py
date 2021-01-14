

import time
import TextProvider
import NerReExtractor
import SchemaCreator
import re

SCHEMA_TYPE = "Relational"

text_provider = TextProvider.TextProvider()
ner_re_extractor = NerReExtractor.NerReExtractor()
schema_creator = SchemaCreator.SchemaCreator(SCHEMA_TYPE)

GLOBAL_SENTENCE_ID = 0

#t_start = time.time()
while(text_provider.has_next()):
    text = text_provider.get_next()
    # split text into sentences and remove spaces
    sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
    # filter out empty string list items
    sentences = list(filter(lambda x: x.strip() != '', sentences))  

    for sentence in sentences:
        print(sentence)

        #since 2 entities are required to predict relations, ignore sentences less than 3 words in length
        if len(sentence.split()) < 3:
            continue
        """ 
        perform sentence level extraction
        include index of sentence as a key for joining entities to sentences
        """
        sentence = {"sentence_id": GLOBAL_SENTENCE_ID, "value": sentence}
        schema_creator.insert_sentence(sentence)

        entities = ner_re_extractor.get_entities(sentence)
        schema_creator.insert_entities(entities, sentence)

        # if SCHEMA_TYPE == "Relational":
        #     relations = ner_re_extractor.get_relations(entities, sentence)       

        GLOBAL_SENTENCE_ID += 1
        
schema_creator.tear_down()

    


# AT THE END TO RECORD TIME IT TOOK
#t_stop = time.time()
#print((t_stop - t_start) / 60)
