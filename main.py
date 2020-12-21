



import time
import TextProvider
import RelationExtractor
import EntityExtractor
import re

#t_start = time.time()


text_provider = TextProvider.TextProvider()
re_extor = RelationExtractor.RelationExtractor()
#en_extor = EntityExtractor.EntityExtractor()

while(text_provider.has_next()):
    text = text_provider.get_next()
    #split text into sentences and remove spaces
    sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
    #filter out empty string list items
    sentences = list(filter(lambda x: x.strip() != '', sentences))  

    #since I require 2 entities to predict relations, I should ignore sentences less than 3 words in length
    #len(test_string.split()) 

    for sentence in sentences:  
        #ignore sentences with length less than 3 words
        if len(sentence.split()) < 3:
            continue

        print(sentence)


    #identify entities
    #should I take the entities in a sentence with the greatest accuracy confidence?




    #identify relations between entities



    #create schema (relational/data warehouse)






#t_stop = time.time()
#print((t_stop - t_start) / 60)
