import spacy
from spacy.matcher import Matcher

def on_match(matcher, doc, id, matches):
    print('Matched!', matches)

nlp = spacy.load('en')
matcher = Matcher(nlp.vocab)
matcher.add('HelloWorld', on_match, [{'LOWER': 'hello'}, {'LOWER': 'world'}])
matcher.add('GoogleMaps', on_match, [{'ORTH': 'Google'}, {'ORTH': 'Maps'}])
doc = nlp(u'HELLO WORLD on Google Maps.')
matches = matcher(doc)

for ent_id, start, end in matches:
    print(ent_id, doc[start:end].text)

