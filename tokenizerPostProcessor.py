import numpy as np
from preProcessing import new_token_list
from extractText import text
import spacy

nlp = spacy.load('de')
doc = nlp(text)


num_token = []
# add num
for toc in doc:
    if(toc.is_digit):
        num_token.append([toc.idx,(toc.idx)+len(toc),'number',toc.text,len(toc),'ordinal'])


#num join

#
