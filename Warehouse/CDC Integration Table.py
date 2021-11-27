# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 13:14:27 2021

@author: hayes
"""

import pandas as pd

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
    df_result = df.drop_duplicates(subset=key + compare_columns, keep='first').reset_index(drop=True)
    df_result.rename(columns = {eff_dt[0]:eff_dttm}, inplace=True)
    
    # generate the expiration date
    df_result[expir_dttm] = df_result.groupby(key)[eff_dttm].shift(periods=-1, fill_value=max_dttm)

    # rearrange columns and return it
    return(df_result[key + [eff_dttm, expir_dttm] + compare_columns])






df = pd.read_csv('user_info.csv')
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)

df.info()

# make these variables to use below
key = ['user_id','position_number']
time_series_eff_dt = ['eff_dt']
compare_columns = [i for i in df.columns if i not in key + time_series_eff_dt]
 



# Performs, but does not return valid output with more than one key field
df = pd.read_csv('user_info.csv')
# df = pd.read_csv('user_info_large.csv')
df_final = create_cdc_dataframe(df, key[0], time_series_eff_dt[0], compare_columns)



# does not pick up the correct row_expir_dttm value
# df = pd.read_csv('user_info.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
df_final2 = create_cdc_dataframe_v2(df, key, time_series_eff_dt, compare_columns)


# Proper data quality, but does not work if the source dttm field is of datetime[64]
# df = pd.read_csv('user_info.csv')
df = pd.read_csv('user_info_large.csv')
# df = pd.read_csv('user_info_large.csv', parse_dates=['eff_dt'], infer_datetime_format=True)
df_final3 = create_cdc_dataframe_v3(df, key, time_series_eff_dt, compare_columns)






