
#split by \.[ ]? and trim on both sides

import re

text = "This is a test.. What the dead... I dont't understand why.   This is a new sentence. "

sentences = list(map(str.strip, re.split(r'\.[ ]?', text)))
sentences = list(filter(lambda x: x.strip() != '', sentences))

print(sentences)