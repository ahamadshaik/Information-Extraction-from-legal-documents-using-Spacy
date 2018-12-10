from German_gazetter import matched_data
from preProcessing import new_token_list,doc

import numpy as np
for toc in matched_data:
    day_name = (toc[5] == 'day')
    one_digit = ((len(doc[toc[1]].text)==1)and((doc[toc[1]].like_num)))
    if(day_name==True):
        print(toc[0])
    #if(one_digit==True):
        #print((toc[0]))





