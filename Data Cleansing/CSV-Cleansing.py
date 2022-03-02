# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:03:34 2022

@author: hayes
"""

import pandas as pd
import csv


df = pd.read_excel('TestFile.xlsx')
df.info()


df.to_csv('comma.csv', index=False)



df.to_csv('pipe-v1.csv', index=False, sep='|')



df.to_csv('pipe-v2.csv', index=False, sep='|', na_rep='N/A')



df.to_csv('pipe-v3.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f')



df.to_csv('pipe-v4.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f', quoting=csv.QUOTE_MINIMAL) # DEFAULT


df.to_csv('pipe-v5.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f', quoting=csv.QUOTE_NONNUMERIC)



df.to_csv('pipe-v6.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f', quoting=csv.QUOTE_ALL )



df.to_csv('pipe-v7.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f', quoting=csv.QUOTE_NONE, escapechar='\\' )



df['dates'] = pd.to_datetime(df['dates']) # convert the column to datetime
df.to_csv('pipe-v8.csv', index=False, sep='|', na_rep='N/A', float_format='%.5f', date_format='%Y-%m-%d' )


# Official Data Cleansing

df['dates'] = pd.to_datetime(df['dates']) # convert the column to datetime

df['example'] = df['example'].fillna('N/A')
df[['currency','percentages']] = df[['currency','percentages']].fillna(0)
df['dates'] = df['dates'].fillna('')


df['currency'].replace(regex=r'[,$]', value='', inplace=True)
df['currency'] = df['currency'].astype('float64')
df['currency'] = df['currency'].apply('${:,.2f}'.format)


df.to_csv('pipe-v9.csv', index=False, sep='|', float_format='%.5f', date_format='%Y-%m-%d' )


