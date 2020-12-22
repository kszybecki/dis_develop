

import re

#class EntityExtractor

# label_list = [
#     "O",       # Outside of a named entity
#     "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
#     "I-MISC",  # Miscellaneous entity
#     "B-PER",   # Beginning of a person's name right after another person's name
#     "I-PER",   # Person's name
#     "B-ORG",   # Beginning of an organisation right after another organisation
#     "I-ORG",   # Organisation
#     "B-LOC",   # Beginning of a location right after another location
#     "I-LOC"    # Location
# ]



sequence2 = "Today is September 1, 2014. I am Kris Szybecki."

# from transformers import  pipeline
# nlp = pipeline("ner", grouped_entities=True)
# print(nlp(sequence2))


# to extract dates but only in number form
# dateRegEx = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
# mo = dateRegEx.search('Today''s date is 06/06/2018') 
# print(mo.group(1)) 

#Sep|September 1, 2019
# you don't know the context of the date 
# but you can see which sentence 
result = re.findall(r'\s\w+\s\d{1,2},\s\d{4}', sequence2)
for r in result:
    print(r)




