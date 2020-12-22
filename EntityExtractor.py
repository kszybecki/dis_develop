

import re
from transformers import  pipeline
import json

sequence2 = "I am Kris Szybecki and I work at Agilent Inc. but also worked at Manitoba Hydro. "

# nlp = pipeline("ner", grouped_entities=True)
# result = nlp(sequence2)
# for r in result:
#     print(r["entity_group"] + " " + r["word"])



results = []
results.append("{'entity_group': 'I-PER', 'score': 0.9944502472877502, 'word': 'Kris Szybecki'}")
results.append("{'entity_group': 'I-ORG', 'score': 0.9987585544586182, 'word': 'Agilent Inc'}")
results.append("{'entity_group': 'I-ORG', 'score': 0.9990890423456827, 'word': 'Manitoba Hydro'}")
results.append("{'entity_group': 'I-ORG', 'score': 0.9990890423456827, 'word': 'Manitoba Hydro'}")

res = [item for item in results if item[0] == 1]

#results2 = results
#res = [i for i in test_list if i not in remove_list]

# for result in results:
#     r = [item for item in result if item[0] == 1]






#should I take the entities in a sentence with the greatest accuracy confidence?
#looks like I'll have to remove duplicates from the list

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



