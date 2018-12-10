import re
from preProcessing import token_list

new_list = []
for tok in token_list:
    new_list.append(re.findall("(([0-9]+)([A-Z]))", tok))

ano_list = []
for el in range(0,len(token_list)):
    ano_list.append(token_list[el])

sub_list = []
for t in range(0,len(ano_list)):
    print(re.findall("([0-9]+)|([A-Z])", ano_list[t]))











