# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 16:54:52 2021

@author: hayes
"""

import pandas as pd
import numpy as np

df1 = pd.read_csv('df1.csv')

df2 = pd.read_csv('df2.csv')

# horizontal concat
pd.concat([df1, df2], axis=1)


# vertical concat
pd.concat([df1, df2])

# Inner Join
df1.merge(df2, how='inner', left_on=['Year','Hour'], right_on=['Year','Hour'])

# Left Join
df1.merge(df2, how='left', left_on=['Year','Hour'], right_on=['Year','Hour'])

# right Join
df1.merge(df2, how='right', left_on=['Year','Hour'], right_on=['Year','Hour'])

# full Join
df1.merge(df2, how='outer', left_on=['Year','Hour'], right_on=['Year','Hour'])




# build out the key and cross join it together
def build_year_hour_df(yr_min, yr_max):
    Yr = pd.DataFrame({'Year':np.arange(yr_min,yr_max,1)})
    Hr = pd.DataFrame({'Hour':np.arange(0,24,1)})
    Yr['key']=0
    Hr['key']=0
    key = pd.merge(Yr, Hr, on='key').drop('key', axis=1)
    return key




# merge the dataframes, and redo the key to fill in missing rows
df = df1.merge(df2, how='outer', left_on=['Year','Hour'], right_on=['Year','Hour'], suffixes=('_1','_2'), sort=True)
key = build_year_hour_df(df.min()['Year'], df.max()['Year']+1)

df = pd.merge(df, key, how='outer', on=['Year','Hour'], sort=True)

# dataframe cleanup
df.fillna('0', inplace=True)
df['Count_1'] = df['Count_1'].astype(int)
df['Count_2'] = df['Count_2'].astype(int)



df_combined = df.melt(id_vars=['Year','Hour'], value_vars=['Count_1','Count_2'], value_name='Count')

