# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:05:13 2021

@author: hayes
"""

import pandas as pd
import re
from dateutil.parser import parse



data = {'key':['Deductible', 'Deductible', 'Deductible', 'Deductible', 'Deductible','Deductible'],
        'value':[1000, 200, 500, 600, 700, '800'],
        'lookup':['$1,000.00', '2%', 'N/A', 'Included', '750', '4/1/2021']}

df = pd.DataFrame(data)



def cleanse_formatting(val : str):
    digit_only = re.compile(r'[^\d.]+')
            
    if val.startswith('$'):
        result = digit_only.sub('', val)
        fmt = 'money'
    elif val.endswith('%'):
        result = str(float(digit_only.sub('', val)) / 100)
        fmt ='percentage'
    elif val.isnumeric():
        result = val
        fmt = 'numeric'
    else:
        result = val
        fmt = 'string'
    
    return zip(*(result, fmt))


df[['db_value', 'db_format']] = df['lookup'].apply(cleanse_formatting)






def cleanse_formattingv2(df : pd.DataFrame(), col : str) -> pd.DataFrame:
    digit_only = re.compile(r'[^\d.]+')
    result = df.copy()
    
    for index, val in result[col].items():

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
            try: 
                dt = parse(val, fuzzy=False)
                cleansedcol = dt.strftime('%m/%d/%Y')
                formatcol = 'date'
            except ValueError:
                formatcol = 'string'
                cleansedcol = val
            
        result.loc[index, col + '_cleansed'] = cleansedcol
        result.loc[index, col + '_format'] = formatcol
        
    return(result)

result = cleanse_formattingv2(df, 'lookup')




print(result)

        










