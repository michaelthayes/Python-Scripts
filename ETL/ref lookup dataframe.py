# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 21:29:00 2022

@author: hayes
"""

import pandas as pd


df_ref = pd.read_csv('ref.csv')


df = pd.read_csv('source.csv')


def key_lookup(x):
    # print(x)
    return(df_ref[df_ref['Key']==x]['Value'].iloc[0])


df_ref.where(df_ref['Key']==3 and df_ref['Lookup']=='product')


df.applymap(key_lookup)

def conv_str(x):
    return(str(x))
def key_lookup(x):
    return(x.name)

df = df.applymap(conv_str)
df.applymap(key_lookup)


x=10
str(x).upper()

x.upper()
