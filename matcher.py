from spacy.matcher import PhraseMatcher
import spacy
import extractText

nlp = spacy.load('en')
matcher = PhraseMatcher(nlp.vocab)
matcher.add('OBAM', None, nlp(u"Diss"))
doc = nlp(extractText.text)
matches = matcher(doc)


print(matches)

for ent_id, start, end in matches:
    print(ent_id, doc[start:end].text)

for ent_id,start,end in matches:
    for i in range(0,end):
        print(doc[0:end].text)

