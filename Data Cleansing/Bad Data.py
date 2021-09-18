# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:05:13 2021

@author: hayes
"""

import pandas as pd
import re
import datetime



data = {'key':['Deductible', 'Deductible', 'Deductible', 'Deductible', 'Deuctible','Deductible'],
        'value':[1000, 200, 500, 600, 700, '800'],
        'lookup':['$1,000.00', '2%', 'N/A', 'Included', '750', '4/1/2021']}

df = pd.DataFrame(data)



# mystring = '$1,00,010.99'
mystring = '10.99%'

def cleanse_formatting(val = str):
    digit_only = re.compile(r'[^\d.]+')
            
    if val.startswith('$'):
        result = digit_only.sub('', val)
        fmt = 'money'
    elif val.endswith('%'):
        result = float(digit_only.sub('', val)) / 100
        fmt ='percentage'
    elif val.isnumeric():
        result = val
        fmt = 'numeric'
    else:
        result = val
        fmt = 'string'
    return [result, fmt]




def cleanse_formattingv2(df = pd.DataFrame(), col = str):
    digit_only = re.compile(r'[^\d.]+')
    result = df.copy()
    
    for index, row in df.iterrows():
        # tmp = pd.DataFrame()
        val = row[col]
        print(val)    
        if val.startswith('$'):
            cleansedcol = digit_only.sub('', val)
            formatcol = 'money'
        elif val.endswith('%'):
            cleansedcol = float(digit_only.sub('', val)) / 100
            formatcol = 'percentage'
        elif val.isnumeric():
            cleansedcol = val
            formatcol = 'numeric'
        else:
            cleansedcol = val
            formatcol = 'string'
            
        result.loc[index, col + '_cleansed'] = cleansedcol
        result.loc[index, col + '_format'] = formatcol
        
        # result = result.append(tmp)
    return(result)

result = cleanse_formattingv2(df, 'lookup')



print(result)

        










