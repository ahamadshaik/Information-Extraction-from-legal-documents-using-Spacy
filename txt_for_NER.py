import preProcessing

# Program to show various ways to read and
# write data in a file.
file1 = open("myfile.txt","wb")
temp = preProcessing.token_list

L = [x.encode('utf-8') for x in temp]


# \n is placed to indicate EOL (End of Line)
for toc in L:
    toc = toc + "\n".encode('ascii')
    file1.write(toc)
 #to change file access modes

