








#contains the following format:
# {
#   "entities": [<entity 1>, <entity 2>], 
#   "key2": [4, 5, 6]
# }


# entities list contains
#  each entity pair:  
#    key => entity name ("per", "loc", "date"), value being entity instance
#    key => "relation": "<relation value>"
#    key => "sentence": "<sentence where this appeared>"
#    key => "sentence_id": "<unique id for sentence>"
#           each sentence should have a unique value as to not duplicate them
#   

import re
from datetime import datetime

dateRegEx1 = re.compile(r'(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})') 
dateRegEx2 = re.compile(r'(\s\w+\s\d{1,2},\s\d{4})')

results1 = re.findall(dateRegEx1, "Today's date is 06/06/2018 and also 01-12-2021 and also 2020-01-01 and also 1999/01/12") 

#also test if there is no error
for result in results1:
    date_result = None
    try:
        date_result = datetime.strptime(result[0].strip(), r'%d/%m/%Y')    
        print(date_result.date())
        continue
    except ValueError:
        pass
    try:
        date_result = datetime.strptime(result[0].strip(), r'%Y/%m/%d')    
        print(date_result.date())
        continue
    except ValueError:
        pass
    try:
        date_result = datetime.strptime(result[0].strip(), r'%d-%m-%Y')    
        print(date_result.date())
        continue
    except ValueError:
        pass
    try:
        date_result = datetime.strptime(result[0].strip(), r'%Y-%m-%d')    
        print(date_result.date())
        continue
    except ValueError:
        pass

# results2 = re.findall(dateRegEx2, "On November 15, 2019 he went and got something ")

# for result in results2:
#     print(result.strip())



