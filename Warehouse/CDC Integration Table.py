# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 13:14:27 2021

@author: hayes
"""

import pandas as pd
import numpy as np

import time
import functools



def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure




@timefunc
def create_cdc_dataframe(df : pd.DataFrame(), key : [], time_series : [], compare_columns : []) -> pd.DataFrame():
    change_list = []
    # loop through the list by uniqueness
    for i in df[key].unique():
        change_list.append(df[df[key] == i][compare_columns].diff())
    df2 = pd.concat(change_list)
        
    df_final = df.loc[(df2!=0).any(axis=1)].copy()
    # add in the row_expir_dt
    df_final['row_expir_dt'] = df_final.groupby(key)[time_series].shift(periods=-1, fill_value='9999-12-31 00:00:00')
    return df_final


@timefunc
# New test which performs faster
def create_cdc_dataframe_v2(df : pd.DataFrame(), key : [], eff_dt : [], compare_columns : []) -> pd.DataFrame():
    max_dttm = '9999-12-31 00:00:00'
    eff_dttm = 'row_eff_dttm'
    expir_dttm = 'row_expir_dttm'

    # change data type
    # df[eff_dt[0]] = pd.to_datetime(df[eff_dt[0]])
    
    # find first effective date
    df_eff = df.drop_duplicates(subset=key+compare_columns, keep='first').reset_index(drop=True)
    df_eff.rename(columns = {eff_dt[0]:eff_dttm}, inplace=True)
    
    # find expiration date
    df_expir = df.drop_duplicates(subset=key+compare_columns, keep='last').reset_index(drop=True)[eff_dt]
    df_expir.columns = [expir_dttm]
    
    # combine it
    df_result = pd.concat([df_eff, df_expir], axis=1)
    
    # assign the top most row the 12/31/9999
    idx = df_result.groupby(key)[expir_dttm].transform(max) == df_result[expir_dttm]
    df_result.loc[idx,[expir_dttm]] = max_dttm

    
    return(df_result[key + [eff_dttm, expir_dttm] + compare_columns])



@timefunc
# New test which performs faster
def create_cdc_dataframe_v3(df : pd.DataFrame(), key : [], eff_dt : [], compare_columns : []) -> pd.DataFrame():
    max_dttm = '9999-12-31 00:00:00.000'
    eff_dttm = 'row_eff_dttm'
    expir_dttm = 'row_expir_dttm'
    
    # find first effective date
    df.sort_values(key + eff_dt, inplace=True) #sort first
    df = df.drop_duplicates(subset=key + compare_columns, keep='first').reset_index(drop=True)
    df.rename(columns = {eff_dt[0]:eff_dttm}, inplace=True)
    
    # generate the expiration date
    df[expir_dttm] = df.groupby(key)[eff_dttm].shift(periods=-1, fill_value=max_dttm)

    # rearrange columns and return it
    return(df[key + [eff_dttm, expir_dttm] + compare_columns])




@timefunc
# v4 works based on cdc_ind including D for delete
def create_cdc_dataframe_v4(df : pd.DataFrame(), key : [], eff_dt : [], compare_columns : [], cdc_ind : str) -> pd.DataFrame():
    max_dttm = '9999-12-31 00:00:00.000'
    eff_dttm = 'row_eff_dttm'
    expir_dttm = 'row_expir_dttm'
        
    ####  all of the below works perfectly
    lst = []
    for i in df[key[0]].unique():
        df_tmp = df[df[key[0]] == i]
        a = df_tmp.shift() # works but needs to shift based on key
        b = df_tmp[df_tmp.ne(a)][key + compare_columns].dropna(axis=0, how='all')
        lst.append(df_tmp.loc[b.index])
    df_chg = pd.concat(lst)
    
    
    # create the row_expir_dttm column & assign the dates
    df_chg['sort'] = df_chg[time_series_eff_dt[0]]
    df_chg[expir_dttm] = df_chg.apply(lambda x: x[time_series_eff_dt[0]] if x['cdc_ind']=='D' else np.nan, axis=1)
    df_chg[time_series_eff_dt[0]] = df_chg.apply(lambda x: np.nan if x['cdc_ind']=='D' else x[time_series_eff_dt[0]], axis=1)
    
    # resort the table
    df_chg.sort_values([key[0], 'sort'], axis=0, inplace=True)
    df_chg.reset_index(drop=True, inplace=True)
    
    
    
    lst = []
    for i in df_chg[key[0]].unique():
        df_tmp = df_chg[df_chg[key[0]] == i].reset_index(drop=True)
        df_shift = df_tmp.shift(periods=-1).reset_index(drop=True)
        
        # Fix the missing expiration dates
        df_tmp['tmp'] = df_shift[time_series_eff_dt]
        df_tmp[expir_dttm] = df_tmp.apply(lambda x: x['tmp'] if pd.isnull(x[expir_dttm]) else x[expir_dttm], axis=1)
        df_tmp['tmp'] = df_shift[expir_dttm]
        df_tmp[expir_dttm] = df_tmp.apply(lambda x: x['tmp'] if pd.isnull(x[expir_dttm]) else x[expir_dttm], axis=1)
        
        
        # fix the missing effective dates
        df_shift = df_tmp.shift(periods=1).reset_index(drop=True)
        df_tmp['tmp'] = df_shift[time_series_eff_dt]
        df_tmp[time_series_eff_dt[0]] = df_tmp.apply(lambda x: x['tmp'] if pd.isnull(x[time_series_eff_dt[0]]) else x[time_series_eff_dt[0]], axis=1)
        lst.append(df_tmp)
    df_chg = pd.concat(lst)
    
    
    df_chg[expir_dttm] = df_chg[expir_dttm].fillna(max_dttm)
    df_chg.rename(columns = {time_series_eff_dt[0]:eff_dttm}, inplace=True)
    df_chg = df_chg[key + [eff_dttm, expir_dttm] + compare_columns]
    df_chg = df_chg.drop(columns=[cdc_ind]).drop_duplicates()
    
    return(df_chg)






# df = pd.read_csv('user_info.csv')
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
df = pd.read_csv('user_info v2.csv')

df.info()

# make these variables to use below
key = ['user_id']#,'position_number']
time_series_eff_dt = ['eff_dt']
cdc_ind = 'cdc_ind'
compare_columns = [i for i in df.columns if i not in key + time_series_eff_dt]
 




# Performs, but does not return valid output with more than one key field
# df = pd.read_csv('user_info.csv')
# df = pd.read_csv('user_info_large.csv')
df_final = create_cdc_dataframe(df, key[0], time_series_eff_dt[0], compare_columns)



# does not pick up the correct row_expir_dttm value
# df = pd.read_csv('user_info.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
df_final2 = create_cdc_dataframe_v2(df, key, time_series_eff_dt, compare_columns)


# Proper data quality, but does not work if the source dttm field is of datetime[64]
# df = pd.read_csv('user_info.csv')
# df = pd.read_csv('user_info_large.csv')
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
df_final3 = create_cdc_dataframe_v3(df, key, time_series_eff_dt, compare_columns)





df = pd.read_csv('user_info v2.csv', dtype=str)
# make these variables to use below
key = ['user_id']#,'position_number']
time_series_eff_dt = ['eff_dt']
cdc_ind = 'cdc_ind'
compare_columns = [i for i in df.columns if i not in key + time_series_eff_dt]
df_final4 = create_cdc_dataframe_v4(df, key, time_series_eff_dt, compare_columns, cdc_ind)



