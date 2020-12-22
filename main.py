



import time
import TextProvider
import NerReExtractor
import re

text_provider = TextProvider.TextProvider()
ner_re_extractor = NerReExtractor.NerReExtractor()

#t_start = time.time()
while(text_provider.has_next()):
    text = text_provider.get_next()
    #split text into sentences and remove spaces
    sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
    #filter out empty string list items
    sentences = list(filter(lambda x: x.strip() != '', sentences))  

    for sentence in sentences:  
        #since I require 2 entities to predict relations, ignore sentences less than 3 words in length
        if len(sentence.split()) < 3:
            continue
        #perform sentence level extraction
        result = ner_re_extractor.get_result(sentence)

        #create schema (relational/data warehouse)

        print(sentence)


    


# AT THE END TO RECORD TIME IT TOOK
#t_stop = time.time()
#print((t_stop - t_start) / 60)
