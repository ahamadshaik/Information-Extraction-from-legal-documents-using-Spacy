
import re

import spacy

from spacy.matcher import Matcher

import PyPDF2

nlp = spacy.load('de')

Numerals = []
RuleList = []
SubRule = ['gesetz1', 'gesetz2', 'gesetz3', 'gesetz4', 'gesetz5']


def extractText(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    num_pages = pdfReader.getNumPages()
    count = 0
    txt = ''
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        # print(pageObj.extractText())
        count += 1
        txt += pageObj.extractText()
    return txt


def checkIfRomanNumeral(numeral):
    validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
    for letters in numeral:
        if letters not in validRomanNumerals:
            return False
    return True


Doc_PATH_German = '1_Grundlagen.pdf'
txt = extractText(Doc_PATH_German)




print("**********************TOKENIZATION***********************************")
doct = nlp(txt)
token_list = []
for toc in doct:
    token_list.append(toc.text)


for token in doct:
    if checkIfRomanNumeral(token.text):
        Numerals.append(token.text)

# Convert list to set and then back to list
Numerals = list(set(Numerals))

print(Numerals)
########################## PostProcessing #########################
token_list_d = []
d = "."
for line in token_list:
    s = line.split('.')
    if(len(s)==1):
        token_list_d.append(line)
    else:
        token_list_d.append(s[0])
        token_list_d.append('.')
        token_list_d.append(s[1])
new_token_list = []
for toc in token_list_d:
    if(len(toc)==1):
        new_token_list.append(toc)
    else:
        temp = re.findall('[a-zA-Z\x7f-\xff]+|\\d+', toc)
        for to in temp:
            new_token_list.append(to)
print(new_token_list)

newN_token_list =[]
for new_toc in new_token_list:
    if new_toc != '\n':
        newN_token_list.append(new_toc)

newWOdotList = []
for dtoc in newN_token_list:
    temps = dtoc.split('.')
    if(len(temps)==1):
        newWOdotList.append(dtoc)
    else:
        newWOdotList.append(temps[0])
        newWOdotList.append('.')
        newWOdotList.append(temps[1])
newWOspace = []
for stoc in newWOdotList:
    if stoc != "" :
        newWOspace.append(stoc)

newWOnline = []
for ntoc in newWOspace:
    if stoc != "\n":
        newWOnline.append(ntoc)

str11 = " ".join(new_token_list)
str12 = " ".join(newWOdotList)
str13 = " ".join(newWOspace)
doc = nlp(str13)
doc1 = nlp(str12)
doc2 = nlp(str11)

matcher = Matcher(nlp.vocab)

# **********************Rule: toc-chapter**********************
IS_ROMAN = nlp.vocab.add_flag(lambda text: text in Numerals)
IS_DASHPUNCT = nlp.vocab.add_flag(lambda text: text in ['-', '_'])
IS_INHALT = nlp.vocab.add_flag(lambda text: text in ['Inhalt', 'Inhaltsübersicht'])
IS_SINGLELETTER = nlp.vocab.add_flag(
    lambda text: text in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])

"""toc_chapterTop1 = [{'ORTH': "Kapitel"}, {IS_ROMAN: True}, {IS_DASHPUNCT: True, 'OP': '?'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '+'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '?'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '?'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '?'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '?'}]
toc_chapterTop2 = [{'ORTH': "Kap"}, {'IS_PUNCT': True, 'ORTH': '.'}, {IS_ROMAN: True}, {IS_DASHPUNCT: True, 'OP': '?'},
                   {'LIKE_NUM': False, 'IS_PUNCT': False, IS_SINGLELETTER: False, IS_INHALT: False, 'OP': '+'}]

matcher.add('toc-chapter', None, toc_chapterTop1)
matcher.add('toc-chapter', None, toc_chapterTop2)
"""


# **************************************************************
# ************************* Rule : ******************************
IS_AL = nlp.vocab.add_flag(lambda text: text in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K'])
IS_STARTPUNCT = nlp.vocab.add_flag(lambda text: text in [',,', '“'])
IS_BRACK = nlp.vocab.add_flag(lambda text: text in ['(', ')'])
rn_art = nlp.vocab.add_flag(lambda text: text in ['Rn', 'Art'])
stop = nlp.vocab.add_flag(lambda text: text in ['.'])
IS_J = nlp.vocab.add_flag(lambda text: text in ['J'])

pattern1 = [{'IS_LOWER': False, 'LIKE_NUM': False}]
pattern2 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}]
part_number = [{'IS_TITLE': True, IS_AL: True, 'LENGTH': 1}]
part1 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': False, 'IS_PUNCT': False, 'OP': '+'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part2 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part3 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part4 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part5 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part6 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part7 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part8 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part9 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part10 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part11 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part12 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part13 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part14 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part15 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part16 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part17 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part18 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part19 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part20 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part21 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part22 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part23 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part24 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
################################################################################################
part25 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part26 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part27 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part28 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part29 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part30 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part31 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part32 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part33 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part34 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part35 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part36 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part37 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part38 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part39 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part40 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part41 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part42 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part43 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part44 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part45 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part46 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part47 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part48 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#############################################################################################################################################################
part49 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part50 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part51 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part52 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part53 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part54 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part55 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part56 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part57 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part58 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part59 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part60 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part61 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part62 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part63 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part64 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part65 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part66 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part67 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part68 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part69 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part70 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part71 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part72 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#######################################################################################################
part73 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part74 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part75 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part76 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part77 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part78 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part79 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part80 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part81 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part82 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part83 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part84 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part85 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part86 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part87 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part88 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part89 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part90 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part91 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part92 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part93 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part94 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part95 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part96 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
####################################################################################################################################################
part97 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}]
part98 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part99 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part100 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part101 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part102 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part103 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part104 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part105 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part106 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part107 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part108 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part109 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part110 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part111 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part112 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part113 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part114 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part115 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part116 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part117 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part118 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part119 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part120 = [{'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#################################################################################################################################################


part121 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part122 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part123 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part124 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part125 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part126 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part127 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part128 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part129 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part130 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part131 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part132 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part133 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part134 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part135 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part136 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part137 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part138 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part139 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part140 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part141 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part142 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part143 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part144 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
################################################################################################
part145 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part146 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part147 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part148 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part149 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part150 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part151 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part152 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part153 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part154 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part155 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part156 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part157 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part158 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part159 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part160 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part161 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part162 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part163 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part164 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part165 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part166 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part167 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part168 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#############################################################################################################################################################
part169 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part170 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part171 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part172 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part173 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part174 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part175 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part176 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part177 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part178 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part179 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part180 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part181 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part182 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part183 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part184 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part185 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part186 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part187 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part188 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part189 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part190 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part191 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part192 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#######################################################################################################
part193 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part194 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part195 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part196 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part197 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part198 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part199 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part200 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part201 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part202 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part203 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part204 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part205 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part206 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part207 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part208 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part209 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part210 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part211 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part212 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part213 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part214 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part215 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part216 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
####################################################################################################################################################
part217 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}]
part218 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part219 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part220 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part221 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part222 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part223 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part224 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part225 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part226 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part227 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part228 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part229 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part230 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part231 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part232 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part233 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part234 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part235 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part236 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part237 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part238 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part239 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part240 = [{'IS_LOWER': False, 'LIKE_NUM': False}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
######################################################################################################################################################
part241 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part242 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part243 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part244 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part245 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part246 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part247 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part248 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part249 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part250 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part251 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part252 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part253 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part254 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part255 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part256 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part257 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part258 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part259 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part260 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part261 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part262 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part263 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part264 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
################################################################################################
part265 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part266 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part267 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part268 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part269 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part270 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part271 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part272 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part273 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part274 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part275 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part276 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part277 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part278 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part279 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part280 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part281 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part282 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part283 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part284 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part285 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part286 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part287 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part288 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH':')'}, {IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#############################################################################################################################################################
part289 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part290 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part291 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part292 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part293 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part294 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part295 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part296 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part297 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part298 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part299 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part300 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part301 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part302 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part303 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part304 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part305 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part306 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part307 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part308 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part309 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part310 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part311 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part312 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {rn_art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#######################################################################################################
part313 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part314 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part315 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part316 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part317 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part318 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part319 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part320 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part321 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part322 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part323 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part324 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part325 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part326 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part327 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part328 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part329 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part330 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part331 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part332 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part333 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part334 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part335 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part336 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
####################################################################################################################################################
part337 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LENGTH': 1, 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}]
part338 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'ADJA'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part339 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'NN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part340 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'VVFIN'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part341 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part342 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part343 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part344 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part345 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part346 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part347 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part348 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part349 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'ff'}, {'ORTH': '.'}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part350 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part351 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part352 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part353 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part354 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part355 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part356 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part357 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part358 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part359 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH':')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
part360 = [{'ORTH': 'Abs'}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'IS_UPPER': True, IS_AL: True, 'LENGTH': 1}, {'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]

matcher.add('part', None, part1)
matcher.add('part', None, part2)
matcher.add('part', None, part3)
matcher.add('part', None, part4)
matcher.add('part', None, part5)
matcher.add('part', None, part6)
matcher.add('part', None, part7)
matcher.add('part', None, part8)
matcher.add('part', None, part9)
matcher.add('part', None, part10)
matcher.add('part', None, part11)
matcher.add('part', None, part12)
matcher.add('part', None, part13)
matcher.add('part', None, part14)
matcher.add('part', None, part15)
matcher.add('part', None, part16)
matcher.add('part', None, part17)
matcher.add('part', None, part18)
matcher.add('part', None, part19)
matcher.add('part', None, part20)
matcher.add('part', None, part21)
matcher.add('part', None, part22)
matcher.add('part', None, part23)
matcher.add('part', None, part24)
matcher.add('part', None, part25)
matcher.add('part', None, part26)
matcher.add('part', None, part27)
matcher.add('part', None, part28)
matcher.add('part', None, part29)
matcher.add('part', None, part30)
matcher.add('part', None, part31)
matcher.add('part', None, part32)
matcher.add('part', None, part33)
matcher.add('part', None, part34)
matcher.add('part', None, part35)
matcher.add('part', None, part36)
matcher.add('part', None, part37)
matcher.add('part', None, part38)
matcher.add('part', None, part39)
matcher.add('part', None, part40)
matcher.add('part', None, part41)
matcher.add('part', None, part42)
matcher.add('part', None, part43)
matcher.add('part', None, part44)
matcher.add('part', None, part45)
matcher.add('part', None, part46)
matcher.add('part', None, part47)
matcher.add('part', None, part48)
matcher.add('part', None, part49)
matcher.add('part', None, part50)
matcher.add('part', None, part51)
matcher.add('part', None, part52)
matcher.add('part', None, part53)
matcher.add('part', None, part54)
matcher.add('part', None, part55)
matcher.add('part', None, part56)
matcher.add('part', None, part57)
matcher.add('part', None, part58)
matcher.add('part', None, part59)
matcher.add('part', None, part60)
matcher.add('part', None, part61)
matcher.add('part', None, part62)
matcher.add('part', None, part63)
matcher.add('part', None, part64)
matcher.add('part', None, part65)
matcher.add('part', None, part66)
matcher.add('part', None, part67)
matcher.add('part', None, part68)
matcher.add('part', None, part69)
matcher.add('part', None, part70)
matcher.add('part', None, part71)
matcher.add('part', None, part72)
matcher.add('part', None, part73)
matcher.add('part', None, part74)
matcher.add('part', None, part75)
matcher.add('part', None, part76)
matcher.add('part', None, part77)
matcher.add('part', None, part78)
matcher.add('part', None, part79)
matcher.add('part', None, part80)
matcher.add('part', None, part81)
matcher.add('part', None, part82)
matcher.add('part', None, part83)
matcher.add('part', None, part84)
matcher.add('part', None, part85)
matcher.add('part', None, part86)
matcher.add('part', None, part87)
matcher.add('part', None, part88)
matcher.add('part', None, part89)
matcher.add('part', None, part90)
matcher.add('part', None, part91)
matcher.add('part', None, part92)
matcher.add('part', None, part93)
matcher.add('part', None, part94)
matcher.add('part', None, part95)
matcher.add('part', None, part96)
matcher.add('part', None, part97)
matcher.add('part', None, part98)
matcher.add('part', None, part99)
matcher.add('part', None, part100)
matcher.add('part', None, part101)
matcher.add('part', None, part102)
matcher.add('part', None, part103)
matcher.add('part', None, part104)
matcher.add('part', None, part105)
matcher.add('part', None, part106)
matcher.add('part', None, part107)
matcher.add('part', None, part108)
matcher.add('part', None, part109)
matcher.add('part', None, part110)
matcher.add('part', None, part111)
matcher.add('part', None, part112)
matcher.add('part', None, part113)
matcher.add('part', None, part114)
matcher.add('part', None, part115)
matcher.add('part', None, part116)
matcher.add('part', None, part117)
matcher.add('part', None, part118)
matcher.add('part', None, part119)
matcher.add('part', None, part120)
matcher.add('part', None, part121)
matcher.add('part', None, part122)
matcher.add('part', None, part123)
matcher.add('part', None, part124)
matcher.add('part', None, part125)
matcher.add('part', None, part126)
matcher.add('part', None, part127)
matcher.add('part', None, part128)
matcher.add('part', None, part129)
matcher.add('part', None, part130)
matcher.add('part', None, part131)
matcher.add('part', None, part132)
matcher.add('part', None, part133)
matcher.add('part', None, part134)
matcher.add('part', None, part135)
matcher.add('part', None, part136)
matcher.add('part', None, part137)
matcher.add('part', None, part138)
matcher.add('part', None, part139)
matcher.add('part', None, part140)
matcher.add('part', None, part141)
matcher.add('part', None, part142)
matcher.add('part', None, part143)
matcher.add('part', None, part144)
matcher.add('part', None, part145)
matcher.add('part', None, part146)
matcher.add('part', None, part147)
matcher.add('part', None, part148)
matcher.add('part', None, part149)
matcher.add('part', None, part150)
matcher.add('part', None, part151)
matcher.add('part', None, part152)
matcher.add('part', None, part153)
matcher.add('part', None, part154)
matcher.add('part', None, part155)
matcher.add('part', None, part156)
matcher.add('part', None, part157)
matcher.add('part', None, part158)
matcher.add('part', None, part159)
matcher.add('part', None, part160)
matcher.add('part', None, part161)
matcher.add('part', None, part162)
matcher.add('part', None, part163)
matcher.add('part', None, part164)
matcher.add('part', None, part165)
matcher.add('part', None, part166)
matcher.add('part', None, part167)
matcher.add('part', None, part168)
matcher.add('part', None, part169)
matcher.add('part', None, part170)
matcher.add('part', None, part171)
matcher.add('part', None, part172)
matcher.add('part', None, part173)
matcher.add('part', None, part174)
matcher.add('part', None, part175)
matcher.add('part', None, part176)
matcher.add('part', None, part177)
matcher.add('part', None, part178)
matcher.add('part', None, part179)
matcher.add('part', None, part180)
matcher.add('part', None, part181)
matcher.add('part', None, part182)
matcher.add('part', None, part183)
matcher.add('part', None, part184)
matcher.add('part', None, part185)
matcher.add('part', None, part186)
matcher.add('part', None, part187)
matcher.add('part', None, part188)
matcher.add('part', None, part189)
matcher.add('part', None, part190)
matcher.add('part', None, part191)
matcher.add('part', None, part192)
matcher.add('part', None, part193)
matcher.add('part', None, part194)
matcher.add('part', None, part195)
matcher.add('part', None, part196)
matcher.add('part', None, part197)
matcher.add('part', None, part198)
matcher.add('part', None, part199)
matcher.add('part', None, part200)
matcher.add('part', None, part201)
matcher.add('part', None, part202)
matcher.add('part', None, part203)
matcher.add('part', None, part204)
matcher.add('part', None, part205)
matcher.add('part', None, part206)
matcher.add('part', None, part207)
matcher.add('part', None, part208)
matcher.add('part', None, part209)
matcher.add('part', None, part210)
matcher.add('part', None, part211)
matcher.add('part', None, part212)
matcher.add('part', None, part213)
matcher.add('part', None, part214)
matcher.add('part', None, part215)
matcher.add('part', None, part216)
matcher.add('part', None, part217)
matcher.add('part', None, part218)
matcher.add('part', None, part219)
matcher.add('part', None, part220)
matcher.add('part', None, part221)
matcher.add('part', None, part222)
matcher.add('part', None, part223)
matcher.add('part', None, part224)
matcher.add('part', None, part225)
matcher.add('part', None, part226)
matcher.add('part', None, part227)
matcher.add('part', None, part228)
matcher.add('part', None, part229)
matcher.add('part', None, part230)
matcher.add('part', None, part231)
matcher.add('part', None, part232)
matcher.add('part', None, part233)
matcher.add('part', None, part234)
matcher.add('part', None, part235)
matcher.add('part', None, part236)
matcher.add('part', None, part237)
matcher.add('part', None, part238)
matcher.add('part', None, part239)
matcher.add('part', None, part240)
matcher.add('part', None, part241)
matcher.add('part', None, part242)
matcher.add('part', None, part243)
matcher.add('part', None, part244)
matcher.add('part', None, part245)
matcher.add('part', None, part246)
matcher.add('part', None, part247)
matcher.add('part', None, part248)
matcher.add('part', None, part249)
matcher.add('part', None, part250)
matcher.add('part', None, part251)
matcher.add('part', None, part252)
matcher.add('part', None, part253)
matcher.add('part', None, part254)
matcher.add('part', None, part255)
matcher.add('part', None, part256)
matcher.add('part', None, part257)
matcher.add('part', None, part258)
matcher.add('part', None, part259)
matcher.add('part', None, part260)
matcher.add('part', None, part261)
matcher.add('part', None, part262)
matcher.add('part', None, part263)
matcher.add('part', None, part264)
matcher.add('part', None, part265)
matcher.add('part', None, part266)
matcher.add('part', None, part267)
matcher.add('part', None, part268)
matcher.add('part', None, part269)
matcher.add('part', None, part270)
matcher.add('part', None, part271)
matcher.add('part', None, part272)
matcher.add('part', None, part273)
matcher.add('part', None, part274)
matcher.add('part', None, part275)
matcher.add('part', None, part276)
matcher.add('part', None, part277)
matcher.add('part', None, part278)
matcher.add('part', None, part279)
matcher.add('part', None, part280)
matcher.add('part', None, part281)
matcher.add('part', None, part282)
matcher.add('part', None, part283)
matcher.add('part', None, part284)
matcher.add('part', None, part285)
matcher.add('part', None, part286)
matcher.add('part', None, part287)
matcher.add('part', None, part288)
matcher.add('part', None, part289)
matcher.add('part', None, part290)
matcher.add('part', None, part291)
matcher.add('part', None, part292)
matcher.add('part', None, part293)
matcher.add('part', None, part294)
matcher.add('part', None, part295)
matcher.add('part', None, part296)
matcher.add('part', None, part297)
matcher.add('part', None, part298)
matcher.add('part', None, part299)
matcher.add('part', None, part300)
matcher.add('part', None, part301)
matcher.add('part', None, part302)
matcher.add('part', None, part303)
matcher.add('part', None, part304)
matcher.add('part', None, part305)
matcher.add('part', None, part306)
matcher.add('part', None, part307)
matcher.add('part', None, part308)
matcher.add('part', None, part309)
matcher.add('part', None, part310)
matcher.add('part', None, part311)
matcher.add('part', None, part312)
matcher.add('part', None, part313)
matcher.add('part', None, part314)
matcher.add('part', None, part315)
matcher.add('part', None, part316)
matcher.add('part', None, part317)
matcher.add('part', None, part318)
matcher.add('part', None, part319)
matcher.add('part', None, part320)
matcher.add('part', None, part321)
matcher.add('part', None, part322)
matcher.add('part', None, part323)
matcher.add('part', None, part324)
matcher.add('part', None, part325)
matcher.add('part', None, part326)
matcher.add('part', None, part327)
matcher.add('part', None, part328)
matcher.add('part', None, part329)
matcher.add('part', None, part330)
matcher.add('part', None, part331)
matcher.add('part', None, part332)
matcher.add('part', None, part333)
matcher.add('part', None, part334)
matcher.add('part', None, part335)
matcher.add('part', None, part336)
matcher.add('part', None, part337)
matcher.add('part', None, part338)
matcher.add('part', None, part339)
matcher.add('part', None, part340)
matcher.add('part', None, part341)
matcher.add('part', None, part342)
matcher.add('part', None, part343)
matcher.add('part', None, part344)
matcher.add('part', None, part345)
matcher.add('part', None, part346)
matcher.add('part', None, part347)
matcher.add('part', None, part348)
matcher.add('part', None, part349)
matcher.add('part', None, part350)
matcher.add('part', None, part351)
matcher.add('part', None, part352)
matcher.add('part', None, part353)
matcher.add('part', None, part354)
matcher.add('part', None, part355)
matcher.add('part', None, part356)
matcher.add('part', None, part357)
matcher.add('part', None, part358)
matcher.add('part', None, part359)
matcher.add('part', None, part360)


#####*****************subTocSubChapterExtractor********************###############################################
IS_Nr = nlp.vocab.add_flag(lambda text: text in ['Nr'])
IS_rnArt = nlp.vocab.add_flag(lambda text: text in ['Rn', 'Art'])
IS_DOT = nlp.vocab.add_flag(lambda text: text in ['.'])
IS_XIV = nlp.vocab.add_flag(lambda text: text in ['X', 'I', 'V'])
IS_XV = nlp.vocab.add_flag(lambda text: text in ['X', 'V'])
IS_Rn_Nr_Art = nlp.vocab.add_flag(lambda text: text in ['Nr', 'Rn', 'Art'])

subtocsubchapternumber = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}]
SubChapter1 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]###additional
SubChapter2 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter3 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter4 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter5 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter6 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter7 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter8 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter9 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter10 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter11 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter12 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter13 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter14 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter15 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter16 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter17 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter18 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter19 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter20 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter21 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter22 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
#################################################################################
SubChapter23 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]###additional
SubChapter24 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter25 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter26 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter27 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter28 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter29 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter30 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter31 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter32 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter33 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter34 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter35 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter36 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter37 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter38 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter39 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter40 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter41 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter42 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter43 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter44 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
#################################################################
SubChapter45 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]###additional
SubChapter46 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter47 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter48 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter49 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter50 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter51 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter52 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter53 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter54 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter55 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter56 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter57 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter58 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter59 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter60 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter61 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter62 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter63 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter64 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter65 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter66 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
#########################################################################
SubChapter67 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]###additional
SubChapter68 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter69 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter70 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter71 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter72 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter73 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter74 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter75 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter76 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter77 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter78 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter79 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter80 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter81 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter82 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter83 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter84 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter85 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter86 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter87 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter88 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
##########################################################################
SubChapter89 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]###additional
SubChapter90 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter91 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter92 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter93 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter94 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter95 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter96 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter97 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter98 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter99 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter100 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter101 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter102 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter103 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter104 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter105 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter106 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter107 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter108 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter109 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]
SubChapter110 = [{IS_ROMAN: True, IS_XV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'IS_PUNCT': False}, {'ORTH': '.'}]

matcher.add('SubChapter', None, SubChapter1)
matcher.add('SubChapter', None, SubChapter2)
matcher.add('SubChapter', None, SubChapter3)
matcher.add('SubChapter', None, SubChapter4)
matcher.add('SubChapter', None, SubChapter5)
matcher.add('SubChapter', None, SubChapter6)
matcher.add('SubChapter', None, SubChapter7)
matcher.add('SubChapter', None, SubChapter8)
matcher.add('SubChapter', None, SubChapter9)
matcher.add('SubChapter', None, SubChapter10)
matcher.add('SubChapter', None, SubChapter11)
matcher.add('SubChapter', None, SubChapter12)
matcher.add('SubChapter', None, SubChapter13)
matcher.add('SubChapter', None, SubChapter14)
matcher.add('SubChapter', None, SubChapter15)
matcher.add('SubChapter', None, SubChapter16)
matcher.add('SubChapter', None, SubChapter17)
matcher.add('SubChapter', None, SubChapter18)
matcher.add('SubChapter', None, SubChapter19)
matcher.add('SubChapter', None, SubChapter20)
matcher.add('SubChapter', None, SubChapter21)
matcher.add('SubChapter', None, SubChapter22)
matcher.add('SubChapter', None, SubChapter23)
matcher.add('SubChapter', None, SubChapter24)
matcher.add('SubChapter', None, SubChapter25)
matcher.add('SubChapter', None, SubChapter26)
matcher.add('SubChapter', None, SubChapter27)
matcher.add('SubChapter', None, SubChapter28)
matcher.add('SubChapter', None, SubChapter29)
matcher.add('SubChapter', None, SubChapter30)
matcher.add('SubChapter', None, SubChapter31)
matcher.add('SubChapter', None, SubChapter32)
matcher.add('SubChapter', None, SubChapter33)
matcher.add('SubChapter', None, SubChapter34)
matcher.add('SubChapter', None, SubChapter35)
matcher.add('SubChapter', None, SubChapter36)
matcher.add('SubChapter', None, SubChapter37)
matcher.add('SubChapter', None, SubChapter38)
matcher.add('SubChapter', None, SubChapter39)
matcher.add('SubChapter', None, SubChapter40)
matcher.add('SubChapter', None, SubChapter41)
matcher.add('SubChapter', None, SubChapter42)
matcher.add('SubChapter', None, SubChapter43)
matcher.add('SubChapter', None, SubChapter44)
matcher.add('SubChapter', None, SubChapter45)
matcher.add('SubChapter', None, SubChapter46)
matcher.add('SubChapter', None, SubChapter47)
matcher.add('SubChapter', None, SubChapter48)
matcher.add('SubChapter', None, SubChapter49)
matcher.add('SubChapter', None, SubChapter50)
matcher.add('SubChapter', None, SubChapter51)
matcher.add('SubChapter', None, SubChapter52)
matcher.add('SubChapter', None, SubChapter53)
matcher.add('SubChapter', None, SubChapter54)
matcher.add('SubChapter', None, SubChapter55)
matcher.add('SubChapter', None, SubChapter56)
matcher.add('SubChapter', None, SubChapter57)
matcher.add('SubChapter', None, SubChapter58)
matcher.add('SubChapter', None, SubChapter59)
matcher.add('SubChapter', None, SubChapter60)
matcher.add('SubChapter', None, SubChapter61)
matcher.add('SubChapter', None, SubChapter62)
matcher.add('SubChapter', None, SubChapter63)
matcher.add('SubChapter', None, SubChapter64)
matcher.add('SubChapter', None, SubChapter65)
matcher.add('SubChapter', None, SubChapter66)
matcher.add('SubChapter', None, SubChapter67)
matcher.add('SubChapter', None, SubChapter68)
matcher.add('SubChapter', None, SubChapter69)
matcher.add('SubChapter', None, SubChapter70)
matcher.add('SubChapter', None, SubChapter71)
matcher.add('SubChapter', None, SubChapter72)
matcher.add('SubChapter', None, SubChapter73)
matcher.add('SubChapter', None, SubChapter74)
matcher.add('SubChapter', None, SubChapter75)
matcher.add('SubChapter', None, SubChapter76)
matcher.add('SubChapter', None, SubChapter77)
matcher.add('SubChapter', None, SubChapter78)
matcher.add('SubChapter', None, SubChapter79)
matcher.add('SubChapter', None, SubChapter80)
matcher.add('SubChapter', None, SubChapter81)
matcher.add('SubChapter', None, SubChapter82)
matcher.add('SubChapter', None, SubChapter83)
matcher.add('SubChapter', None, SubChapter84)
matcher.add('SubChapter', None, SubChapter85)
matcher.add('SubChapter', None, SubChapter86)
matcher.add('SubChapter', None, SubChapter87)
matcher.add('SubChapter', None, SubChapter88)
matcher.add('SubChapter', None, SubChapter89)
matcher.add('SubChapter', None, SubChapter90)
matcher.add('SubChapter', None, SubChapter91)
matcher.add('SubChapter', None, SubChapter92)
matcher.add('SubChapter', None, SubChapter93)
matcher.add('SubChapter', None, SubChapter94)
matcher.add('SubChapter', None, SubChapter95)
matcher.add('SubChapter', None, SubChapter96)
matcher.add('SubChapter', None, SubChapter97)
matcher.add('SubChapter', None, SubChapter98)
matcher.add('SubChapter', None, SubChapter99)
matcher.add('SubChapter', None, SubChapter100)
matcher.add('SubChapter', None, SubChapter101)
matcher.add('SubChapter', None, SubChapter102)
matcher.add('SubChapter', None, SubChapter103)
matcher.add('SubChapter', None, SubChapter104)
matcher.add('SubChapter', None, SubChapter105)
matcher.add('SubChapter', None, SubChapter106)
matcher.add('SubChapter', None, SubChapter107)
matcher.add('SubChapter', None, SubChapter108)
matcher.add('SubChapter', None, SubChapter109)
matcher.add('SubChapter', None, SubChapter110)



####(subchapter initiation)######
SubChapter111 = [{'LIKE_NUM': False, IS_Nr: False}]
SubChapter112 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}]
SubChapter113 = [{'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}]
SubChapter114 = [{'POS': 'ADJA', 'IS_PUNCT': True}]
SubChapter115 = [{'POS': 'XY', 'IS_PUNCT': True}]
SubChapter116 = [{'POS': 'VVFIN', 'IS_PUNCT': True}]
SubChapter117 = [{'ORTH': '$'}]
SubChapter118 = [{'ORTH': ':'}]
SubChapter119 = [{'ORTH': ','}]
SubChapter120 = [{'ORTH': '-'}]
SubChapter121 = [{'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}]
SubChapter122 = [{'ORTH': 'bzw'}, {'ORTH': '.'}]
SubChapter123 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}]
SubChapter124 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}]
SubChapter125 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}]
SubChapter126 = [{'ORTH': ';'}]
SubChapter127 = [{'ORTH': '('}, {'ORTH': ')'}]
SubChapter128 = [{'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}]
SubChapter129 = [{'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}]
SubChapter130 = [{'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}]
SubChapter131 = [{'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}]
####################################################################################################################################



subtocsubchapternumber_2 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}]
subChapter1 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]###additional
subChapter2 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter3 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter4 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter5 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter6 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter7 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter8 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter9 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter10 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter11 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter12 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter13 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter14 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter15 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter16 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter17 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter18 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter19 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter20 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter21 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter22 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
################################################################################
subChapter23 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]###additional
subChapter24 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter25 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter26 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter27 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter28 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter29 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter30 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter31 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter32 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter33 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter34 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter35 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter36 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter37 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter38 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter39 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter40 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter41 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter42 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter43 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter44 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
#################################################################
subChapter45 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]###additional
subChapter46 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter47 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter48 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter49 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter50 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter51 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter52 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter53 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter54 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter55 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter56 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter57 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter58 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter59 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter60 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter61 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter62 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter63 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter64 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter65 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter66 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_rnArt: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
#########################################################################
subChapter67 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]###additional
subChapter68 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter69 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter70 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter71 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter72 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter73 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter74 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter75 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter76 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter77 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter78 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter79 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter80 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter81 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter82 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter83 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter84 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter85 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter86 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter87 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter88 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_DOT: False}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
##########################################################################
subChapter89 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]###additional
subChapter90 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter91 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter92 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter93 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter94 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter95 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter96 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter97 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter98 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter99 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter100 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter101 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter102 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter103 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter104 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter105 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter106 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter107 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter108 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter109 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]
subChapter110 = [{IS_ROMAN: True, IS_XIV: True, 'OP': '+'}, {'IS_PUNCT': True, 'ORTH': '.'}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '*'}, {'LIKE_NUM': True, 'POS': 'ADJA', 'OP': '!'}, {'ÍS_J': False, 'IS_PUNCT': False}, {'ORTH': '.'}]

matcher.add('subChapter', None, subChapter1)
matcher.add('subChapter', None, subChapter2)
matcher.add('subChapter', None, subChapter3)
matcher.add('subChapter', None, subChapter4)
matcher.add('subChapter', None, subChapter5)
matcher.add('subChapter', None, subChapter6)
matcher.add('subChapter', None, subChapter7)
matcher.add('subChapter', None, subChapter8)
matcher.add('subChapter', None, subChapter9)
matcher.add('subChapter', None, subChapter10)
matcher.add('subChapter', None, subChapter11)
matcher.add('subChapter', None, subChapter12)
matcher.add('subChapter', None, subChapter13)
matcher.add('subChapter', None, subChapter14)
matcher.add('subChapter', None, subChapter15)
matcher.add('subChapter', None, subChapter16)
matcher.add('subChapter', None, subChapter17)
matcher.add('subChapter', None, subChapter18)
matcher.add('subChapter', None, subChapter19)
matcher.add('subChapter', None, subChapter20)
matcher.add('subChapter', None, subChapter21)
matcher.add('subChapter', None, subChapter22)
matcher.add('subChapter', None, subChapter23)
matcher.add('subChapter', None, subChapter24)
matcher.add('subChapter', None, subChapter25)
matcher.add('subChapter', None, subChapter26)
matcher.add('subChapter', None, subChapter27)
matcher.add('subChapter', None, subChapter28)
matcher.add('subChapter', None, subChapter29)
matcher.add('subChapter', None, subChapter30)
matcher.add('subChapter', None, subChapter31)
matcher.add('subChapter', None, subChapter32)
matcher.add('subChapter', None, subChapter33)
matcher.add('subChapter', None, subChapter34)
matcher.add('subChapter', None, subChapter35)
matcher.add('subChapter', None, subChapter36)
matcher.add('subChapter', None, subChapter37)
matcher.add('subChapter', None, subChapter38)
matcher.add('subChapter', None, subChapter39)
matcher.add('subChapter', None, subChapter40)
matcher.add('subChapter', None, subChapter41)
matcher.add('subChapter', None, subChapter42)
matcher.add('subChapter', None, subChapter43)
matcher.add('subChapter', None, subChapter44)
matcher.add('subChapter', None, subChapter45)
matcher.add('subChapter', None, subChapter46)
matcher.add('subChapter', None, subChapter47)
matcher.add('subChapter', None, subChapter48)
matcher.add('subChapter', None, subChapter49)
matcher.add('subChapter', None, subChapter50)
matcher.add('subChapter', None, subChapter51)
matcher.add('subChapter', None, subChapter52)
matcher.add('subChapter', None, subChapter53)
matcher.add('subChapter', None, subChapter54)
matcher.add('subChapter', None, subChapter55)
matcher.add('subChapter', None, subChapter56)
matcher.add('subChapter', None, subChapter57)
matcher.add('subChapter', None, subChapter58)
matcher.add('subChapter', None, subChapter59)
matcher.add('subChapter', None, subChapter60)
matcher.add('subChapter', None, subChapter61)
matcher.add('subChapter', None, subChapter62)
matcher.add('subChapter', None, subChapter63)
matcher.add('subChapter', None, subChapter64)
matcher.add('subChapter', None, subChapter65)
matcher.add('subChapter', None, subChapter66)
matcher.add('subChapter', None, subChapter67)
matcher.add('subChapter', None, subChapter68)
matcher.add('subChapter', None, subChapter69)
matcher.add('subChapter', None, subChapter70)
matcher.add('subChapter', None, subChapter71)
matcher.add('subChapter', None, subChapter72)
matcher.add('subChapter', None, subChapter73)
matcher.add('subChapter', None, subChapter74)
matcher.add('subChapter', None, subChapter75)
matcher.add('subChapter', None, subChapter76)
matcher.add('subChapter', None, subChapter77)
matcher.add('subChapter', None, subChapter78)
matcher.add('subChapter', None, subChapter79)
matcher.add('subChapter', None, subChapter80)
matcher.add('subChapter', None, subChapter81)
matcher.add('subChapter', None, subChapter82)
matcher.add('subChapter', None, subChapter83)
matcher.add('subChapter', None, subChapter84)
matcher.add('subChapter', None, subChapter85)
matcher.add('subChapter', None, subChapter86)
matcher.add('subChapter', None, subChapter87)
matcher.add('subChapter', None, subChapter88)
matcher.add('subChapter', None, subChapter89)
matcher.add('subChapter', None, subChapter90)
matcher.add('subChapter', None, subChapter91)
matcher.add('subChapter', None, subChapter92)
matcher.add('subChapter', None, subChapter93)
matcher.add('subChapter', None, subChapter94)
matcher.add('subChapter', None, subChapter95)
matcher.add('subChapter', None, subChapter96)
matcher.add('subChapter', None, subChapter97)
matcher.add('subChapter', None, subChapter98)
matcher.add('subChapter', None, subChapter99)
matcher.add('subChapter', None, subChapter100)
matcher.add('subChapter', None, subChapter101)
matcher.add('subChapter', None, subChapter102)
matcher.add('subChapter', None, subChapter103)
matcher.add('subChapter', None, subChapter104)
matcher.add('subChapter', None, subChapter105)
matcher.add('subChapter', None, subChapter106)
matcher.add('subChapter', None, subChapter107)
matcher.add('subChapter', None, subChapter108)
matcher.add('subChapter', None, subChapter109)
matcher.add('subChapter', None, subChapter110)



####(subchapter initiation)######
subChapter111 = [{'LIKE_NUM': False, IS_Nr: False}]
subChapter112 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Nr: False}]
subChapter113 = [{'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}]
subChapter114 = [{'POS': 'ADJA', 'IS_PUNCT': True}]
subChapter115 = [{'POS': 'XY', 'IS_PUNCT': True}]
subChapter116 = [{'POS': 'VVFIN', 'IS_PUNCT': True}]
subChapter117 = [{'ORTH': '$'}]
subChapter118 = [{'ORTH': ':'}]
subChapter119 = [{'ORTH': ','}]
subChapter120 = [{'ORTH': '-'}]
subChapter121 = [{'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}]
subChapter122 = [{'ORTH': 'bzw'}, {'ORTH': '.'}]
subChapter123 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}]
subChapter124 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}]
subChapter125 = [{'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}]
subChapter126= [{'ORTH': ';'}]
subChapter127 = [{'ORTH': '('}, {'ORTH': ')'}]
subChapter128 = [{'ORTH': '('}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}]
subChapter129 = [{'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}]
subChapter130 = [{'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '!'}, {'ORTH': ')'}]
subChapter131 = [{'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}]
####################################################################################################################################
#################**************************************SubTocSubSUbChapterExtractor*****************############################
IS_spec_list = nlp.vocab.add_flag(lambda text: text in ['Abs', 'Rn', 'Nr', 'Auf1'])

subTocSubSubChapterNumber1 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_spec_list: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber2 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, IS_spec_list: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber3 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber4 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber5 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber6 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber7 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber8 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '$'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber9 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ':'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber10 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber11 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber12 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber13 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber14 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber15 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '-'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber16 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ';'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber17 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber18 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber19 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber20 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber21 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber22 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
#####################################
subTocSubSubChapterNumber23 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_spec_list: False}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber24 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, IS_spec_list: False}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber25 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber26 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber27 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber28 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber29 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber30 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '$'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber31 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ':'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber32 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber33 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber34 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber35 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber36 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber37 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '-'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber38 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ';'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber39 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber40 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber41 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber42 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber43 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber44 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': False, IS_Rn_Nr_Art: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
##################################
subTocSubSubChapterNumber45 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_spec_list: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber46 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, IS_spec_list: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber47 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber48 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber49 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber50 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'XY', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber51 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber52 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '$'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber53 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ':'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber54 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber55 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber56 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber57 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber58 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber59 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '-'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber60 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ';'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber61 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber62 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber63 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber64 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber65 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber66 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'IS_PUNCT': True, stop: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
###############################
subTocSubSubChapterNumber67 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_spec_list: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber68 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, IS_spec_list: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber69 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber70 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber71 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber72 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'XY', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber73 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber74 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '$'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber75 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ':'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber76 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber77 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber78 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber79 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber80 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber81 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '-'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber82 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ';'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber83 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber84 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber85 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber86 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber87 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber88 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
###############################################
subTocSubSubChapterNumber89 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': False, IS_spec_list: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber90 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, IS_spec_list: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber91 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber92 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'IS_PUNCT': True, IS_STARTPUNCT: True, 'POS': 'CARD', IS_BRACK: False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber93 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'ADJA', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber94 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'XY', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber95 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'POS': 'VVFIN', 'IS_PUNCT': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber96 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '$'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber97 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ':'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber98 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'LIKE_NUM': False, 'POS': 'CARD'}, {'ORTH': '.', 'OP': '!'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber99 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'bzw'}, {'ORTH': '.'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber100 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber101 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'LIKE_NUM': False}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber102 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ','}, {'LIKE_NUM': True}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber103 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '-'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber104 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': ';'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber105 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber106 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber107 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber108 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {stop: False, 'OP': '*'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber109 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]
subTocSubSubChapterNumber110 = [{'LIKE_NUM': True, 'POS': 'ADJA', 'LENGTH': 2}, {'ORTH': '('}, {'ORTH': 'Nr'}, {'ORTH': '.'}, {'LIKE_NUM': True}, {'ORTH': 'u'}, {'ORTH': '.'}, {'ORTH': ')'}, {'ORTH': '.', 'OP': '+'}, {'LIKE_NUM': True}]

matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber1)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber2)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber3)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber4)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber5)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber6)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber7)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber8)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber9)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber10)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber11)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber12)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber13)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber14)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber15)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber16)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber17)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber18)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber19)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber20)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber21)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber22)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber23)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber24)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber25)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber26)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber27)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber28)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber29)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber30)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber31)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber32)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber33)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber34)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber35)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber36)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber37)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber38)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber39)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber40)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber41)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber42)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber43)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber44)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber45)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber46)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber47)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber48)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber49)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber50)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber51)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber52)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber53)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber54)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber55)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber56)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber57)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber58)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber59)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber60)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber61)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber62)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber63)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber64)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber65)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber66)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber67)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber68)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber69)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber70)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber71)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber72)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber73)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber74)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber75)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber76)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber77)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber78)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber79)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber80)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber81)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber82)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber83)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber84)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber85)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber86)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber87)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber88)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber89)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber90)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber91)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber92)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber93)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber94)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber95)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber96)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber97)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber98)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber99)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber100)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber101)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber102)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber103)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber104)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber105)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber106)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber107)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber108)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber109)
matcher.add('subTocSubSubChapterNumber', None, subTocSubSubChapterNumber110)


# **********************Rule: Reference**********************
IS_OMITSIGN = nlp.vocab.add_flag(lambda text: text in ['(', ')', '\'', '/', ';', 'Rn', 'nach', 'gemäß'])

ref_Extractor = [{'ORTH': "§", 'OP': '+'}, {IS_OMITSIGN: True, 'IS_TITLE': False, 'POS': 'VAFIN', 'OP': '!'},
                 {IS_OMITSIGN: False, 'IS_UPPER': False, 'OP': '?'}, {IS_OMITSIGN: False, 'IS_UPPER': False, 'OP': '?'},
                 {IS_OMITSIGN: False, 'IS_UPPER': False, 'OP': '?'}, {IS_OMITSIGN: False, 'IS_UPPER': False, 'OP': '?'},
                 {IS_OMITSIGN: False, 'IS_UPPER': False, 'OP': '?'}, {'IS_UPPER': True}]
ref_Extractor2 = [{'ORTH': "Art"}, {'ORTH': "."}, {IS_OMITSIGN: True, 'POS': 'VAFIN', 'OP': '!'},
                  {'IS_UPPER': True, 'OP': '+'}]
ref_Extractor3 = [{'ORTH': "Art"}, {'ORTH': "."}, {IS_OMITSIGN: True, 'POS': 'VAFIN', 'OP': '!'},
                  {'IS_UPPER': False, 'IS_LOWER': False, 'OP': '+'}]
ref_Extractor4 = [{'LIKE_NUM': True, 'SHAPE': 'dddd'}, {'ORTH': "/"}, {'IS_UPPER': True}]
ref_Extractor5 = [{'LIKE_NUM': True, 'SHAPE': 'dddd'}, {'POS': 'NUM'}, {'ORTH': "/"}, {'IS_UPPER': True}]
ref_Extractor6 = [{'POS': 'NUM'}, {'ORTH': "/"}, {'POS': 'NUM'}, {'ORTH': "/"}, {'IS_UPPER': True}]

matcher.add('gesetz1', None, ref_Extractor)
matcher.add('gesetz2', None, ref_Extractor2)
matcher.add('gesetz2', None, ref_Extractor3)
matcher.add('gesetz3', None, ref_Extractor4)
matcher.add('gesetz4', None, ref_Extractor5)
matcher.add(' ', None, ref_Extractor5)
# **************************************************************

matches = matcher(doc)

for match_id, start, end in matches:
    LocalRule = []
    string_id = nlp.vocab.strings[match_id]  # get string representation
    span = doc[start:end]  # the matched span

    try:
        annotations = spotlight.annotate('http://api.dbpedia-spotlight.org/de/annotate', span.text, confidence=0.9,
                                         support=10)
        # print("Dbpedia: ", annotations)
    except:
        annotations = ""
        # print ("Exception")

    LocalRule.append(span.text)
    LocalRule.append(str(start) + "-" + str(end))

    if string_id in SubRule:
        LocalRule.append("Reference")
        LocalRule.append(string_id)
    else:
        LocalRule.append(string_id)
        LocalRule.append(" ")

    LocalRule.append(annotations)

    RuleList.append(LocalRule)
    print("")
    print(string_id, start, end, span.text)

print("The final Rules are: ")
print(RuleList)

for i in RuleList:
    # Logging
    with open('output.txt', 'a') as f:
        print("", file=f)
        print("Rule", i, file=f)


matches = matcher(doc)
for ent_id, start, end in matches:
    print(doc[start: end], start, end)