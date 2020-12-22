

import re

#class EntityExtractor





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
# result = re.findall(r'\s\w+\s\d{1,2},\s\d{4}', sequence2)
# for r in result:
#     print(r)


# regex for emails
# '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'



