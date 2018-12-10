#Tokenization
import spacy
import extractText
import re

token_list = []
nlp = spacy.load('de')

doc = nlp(extractText.text)


for token in doc:
    token_list.append(token.text)

#sentence splitting

sentence_list = []

for sentence in doc.sents:
    sentence_list.append(sentence)



for toc in token_list:
    if toc=='\n':
        token_list.remove('\n')

# not feasible solution to remove \n
new_token_list = []
for toc in token_list:
    if(len(toc)==1):
        new_token_list.append(toc)
    else:
        temp = re.findall('[a-zA-Z\x7f-\xff]+|\\d+', toc)
        for to in temp:
            new_token_list.append(to)




