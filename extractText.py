import numpy
import pandas
import spacy
import PyPDF2
import nltk
import os
java_path = "C:\\Program Files\\Java\\jdk-11.0.1\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path

text_string =''
s = ''
spacy_token_list = []
spacy_sentence_list = []
#pypdf2
filename = '1_Grundlagen.pdf'

pdfObj =  open(filename,'rb')
pdfReader = PyPDF2.PdfFileReader(filename)

num_pages = pdfReader.getNumPages()

count = 0
text = ''

while count < num_pages:
    pageObj = pdfReader.getPage(count)
    #print(pageObj.extractText())
    count += 1
    text += pageObj.extractText()
    s = pageObj.extractText()
    text_string.__add__(s)



#nltk
#stop_words = nltk.corpus.stopwords.words('english')
#punctuations = ['(',')',';',':','[',']',',']

#tokens = nltk.tokenize.word_tokenize(text)
#keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

#print(keywords)




