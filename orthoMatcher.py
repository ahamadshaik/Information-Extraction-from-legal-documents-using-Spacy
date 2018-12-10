import spacy

nlp = spacy.load('de')

doc = nlp('hello guYs hOw Are you AlL')

for toc in doc:
    print(toc.text,toc.shape_)