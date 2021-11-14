# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 13:14:27 2021

@author: hayes
"""

import pandas as pd



def create_cdc_dataframe(df : pd.DataFrame(), key : [], time_series : [], compare_columns : []) -> pd.DataFrame():
    change_list = []
    # loop through the list by uniqueness
    for i in df[key].unique():
        change_list.append(df[df[key] == i][compare_columns].diff())
    df2 = pd.concat(change_list)
        
    df_final = df.loc[(df2!=0).any(axis=1)].copy()
    # add in the row_expir_dt
    df_final['row_expir_dt'] = df_final.groupby(key)[time_series].shift(periods=-1, fill_value='12/31/9999 00:00:00.000')
    return df_final



df = pd.read_csv('user_info.csv')



# make these variables to use below
key = 'user_id'
time_series = 'eff_dt'
compare_columns = [i for i in df.columns if i not in key + time_series]
 
df_final = create_cdc_dataframe(df, key, time_series, compare_columns)

