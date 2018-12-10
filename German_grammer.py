from German_gazetter import matched_data
from preProcessing import new_token_list
# only rules for date
import spacy
from spacy import matcher
import re

nlp = spacy.load('de')
toc_with_lookups = []
for j in range(0,len(matched_data)):
    #
    toc_with_lookups.append([new_token_list[matched_data[j][1]],matched_data[j][3],matched_data[j][4]])
