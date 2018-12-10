from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

#Tokenization
import spacy
import extractText

a = ''

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
a = convert_pdf_to_txt('1_Grundlagen.pdf')




token_list = []
nlp = spacy.load('de')

doc = nlp(a)

for token in doc:
    token_list.append(token.text)

#sentence splitting

sentence_list = []

for sentence in doc.sents:
    sentence_list.append(sentence)



for toc in token_list:
    if toc=='\n':
        token_list.remove('\n')
    if toc == '\n\n':
        token_list.remove('\n\n')

# not feasible solution to remove \n
