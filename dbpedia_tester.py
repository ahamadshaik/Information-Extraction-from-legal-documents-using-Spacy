import spotlight
import preProcessing
import extractText
annotations = spotlight.annotate('http://api.dbpedia-spotlight.org/de/annotate',extractText.text,
                                 confidence=0.9, support=10)

for i in annotations:
    print(i)