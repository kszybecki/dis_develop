



import time
import TextProvider
import ExtractEntitiesAndRelations
import re

#t_start = time.time()


text_provider = TextProvider.TextProvider()
extractor = ExtractEntitiesAndRelations.ExtractEntitiesAndRelations()

while(text_provider.has_next()):
    text = text_provider.get_next()
    #split text into sentences and remove spaces
    sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
    #filter out empty string list items
    sentences = list(filter(lambda x: x.strip() != '', sentences))

    

    for sentence in sentences:
        print(sentence)


    #identify entities


    #identify relations between entities



    #create schema (relational/data warehouse)






#t_stop = time.time()
#print((t_stop - t_start) / 60)
