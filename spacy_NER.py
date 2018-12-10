import spacy

import extractText

nlp = spacy.load('xx_ent_wiki_sm')

doc = nlp(extractText.text)

for entity in doc.ents:
    if(entity.text!=''):
        print(entity.text,entity.label_)


