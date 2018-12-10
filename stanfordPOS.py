import extractText
import nltk

pos_categories = []
jar_path = 'stanford-postagger-full-2018-10-16\stanford-postagger-3.9.2.jar'
file_path = 'stanford-postagger-full-2018-10-16\models\german-hgc.tagger'
path = nltk.tag.stanford.StanfordPOSTagger(file_path,jar_path)
path.java_options='-mx4096m'
pos_categories.append(path.tag(extractText.text.split()))




#spacy
#nlp = spacy.load('de')
#docs = nlp(text)

#for token in docs:
#    spacy_token_list.append(token.text)
#    print(token.text,token.pos_)
#
#for sentence in docs.sents:
#   spacy_sentence_list.append(sentence)