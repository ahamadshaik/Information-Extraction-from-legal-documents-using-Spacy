import csv
import numpy as np
import codecs
import preProcessing

with open('lookup.csv')as csv2_file:
    lookup_list = list(csv.reader(csv2_file))

lookup_array = np.array(lookup_list)

file_names = lookup_array[:,0]
major_types = lookup_array[:,1]
minor_types = lookup_array[:,2]
languages = lookup_array[:,3]
readerObj = []
for file in file_names:
    types_of_encoding = ["cp1252"]
    for encoding_type in types_of_encoding:
        with codecs.open('gazetteer/'+file, encoding=encoding_type, errors='replace') as csv_file:
            readerObj.append(list(csv.reader(csv_file)))
print('initialization')

matched_data = []
toc_num = 0
for toc in preProcessing.new_token_list:
    data_list_num = 0
    for data_list in readerObj:
        m = len(data_list)
        #print(toc_num,data_list_num)
        for data in range(0,len(data_list)):
            temp = ''
            temp = temp.join(data_list[data])
            if temp==toc:
                matched_data.append([data_list[data],toc_num,file_names[data_list_num],major_types[data_list_num],minor_types[data_list_num],languages[data_list_num]])
        data_list_num = data_list_num + 1
    toc_num = toc_num + 1




