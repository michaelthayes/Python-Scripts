# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:55:02 2021

@author: hayes
"""


# script will take columns with numbers in them turn them into row-wise data

import pandas as pd
import re

df = pd.DataFrame({'key': ['one', 'two', 'three', 'four', 'five',
                           'six'],
                   'location1name': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'location1count': [1, 2, 3, 4, 5, 6],
                   'location1place': ['x', 'y', 'z', 'q', 'w', 't'],
                   'locationname10': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'locationcount10': [1, 2, 3, 4, 5, 6],
                   'locationplace10': ['x', 'y', 'z', 'q', 'w', 't'],
                   '2locationname': ['A', 'B', 'C', 'A', 'B', 'C'],
                   '2locationcount': [1, 2, 3, 4, 5, 6],
                   '2locationplace': ['x', 'y', 'z', 'q', 'w', 't'],
                   'location3name': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'location3count': [1, 2, 3, 4, 5, 6],
                   'location3place': ['x', 'y', 'z', 'q', 'w', 't']})


# Find all the columns with numbers in them
r = re.compile(r'\d')
# number_columns = []
# for col in df.columns:
#     if r.search(col):
#         # print(col)
#         number_columns.append(col)
number_columns = list(filter(r.search, df.columns))
# print(number_columns)




# Flip the columns of data into rows of data
df_tmp = df.melt(id_vars=['key'], value_vars=number_columns)


def extract_numbers_from_columns(txt):
    
    # regular expression containing all numbers
    result = re.findall(r'\d+', txt)
      
    # form a string
    string = ''.join(result)
      
    # list of strings return
    return string
    
# yank out the numbers
df_tmp['seq'] = df_tmp['variable'].apply(lambda x : extract_numbers_from_columns(x))

# replace the numbers in the columns
df_tmp["variable"] = df_tmp.apply(lambda row: row['variable'].replace(row['seq'], ''), axis = 1)

# flip the rows back to columns
df_final = df_tmp.pivot(index=['key','seq'], columns=['variable'])['value'].reset_index()

# df_final.sort_values(by=['key','seq'])



















