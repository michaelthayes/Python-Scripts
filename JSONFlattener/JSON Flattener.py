# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 10:21:44 2020

@author: Mike
"""





import json
#import csv
#import os
from flatten_json  import flatten
import pandas as pd
#from pandas.io.json import json_normalize


json_data = []
#with open('example1.json') as f:
#with open('example2.json') as f:
with open('example3.json') as f:
#with open('example4.json') as f:  # example causes issues since it should just be rows
    for jsonObj in f:
        json_dict = json.loads(jsonObj)
        json_data.append(json_dict)



json_flatten = (flatten(d, separator='.') for d in json_data)


df = pd.DataFrame(json_flatten)


df.to_csv('output.csv', index=False)



#for d in range(len(data)):
#    i=d    
#    flatten1.append(json_normalize(flatten(data[i])))    
#    df.append(pd.DataFrame(flatten1[i]))

"""
item_keys=[]
#loop in the normalized list to get the header key
for item in df:
    for key in item:
        item_keys.append(key)       
        
#convert the header to list to print to csv file        
header = list(dict.fromkeys(item_keys))        
order=[header.sort()]      
csv_data=[header]
print(header)    
hl=len(header)
csvdata=[]
   
csv_file= open('outputcsv1.csv','w',newline='')
writer=csv.writer(csv_file,delimiter=',',lineterminator='\n\n')
#write the headers to output file
writer.writerow(header)

#loop in normalized data in list df and header. 
#Compare the header value and key to print corresponding data
#if any key is not available print as None. Finally print all data to csv
for r in df:       
    for h in header:
        if h not in r.columns:
            csvdata.append('None')
        else:
            csvdata.append(r[h].rename_axis(None).rename(None))
    writer.writerow(list(csvdata)) 
    csvdata.clear()
                          
csv_file.close()

#Read the csv to dataframe and use replace functionality to remove dtype 
#and preceding '0' and write back final data to another output file

df=pd.read_csv('outputcsv1.csv')
print(df)
df1=df.replace(regex=['\ndtype: object'],value=" ")
df2=df1.replace(regex=['0  '],value="")
df2.to_csv('OutputCSVdata.csv',index=False)
os.remove('outputcsv1.csv')
       
print('just completed')               
        
"""
