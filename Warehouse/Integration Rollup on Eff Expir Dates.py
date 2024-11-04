# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 18:31:17 2023

@author: hayes
"""


import pandas as pd
# import numpy as np

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


df = pd.read_excel('CDC Rows.xlsx',dtype='str')
orig_columns = df.columns
eff_ts_tmp = 'row_eff_ts_tmp'
expir_ts_tmp = 'row_expir_ts_tmp'



no workie

df[eff_ts_tmp] = df['row_eff_ts'].shift(-1)
df[expir_ts_tmp] = df['row_expir_ts'].shift(-1)





df_merge = pd.merge(df, df, left_on=['ID','row_expir_ts'], right_on=['ID','row_eff_ts'], how='inner')

# data match
new_cols = {x: y for x, y in zip(['ID','row_eff_ts_x','row_expir_ts_x'], ['ID','row_eff_ts_y','row_expir_ts_y'])}
df_datacheck = pd.concat([df_merge[['ID','row_eff_ts_x','row_expir_ts_x']], df_merge[['ID','row_eff_ts_y','row_expir_ts_y']]], axis=0, ignore_index=True)

df_notfound = df[df.isin(df_merge[['ID','row_eff_ts_x','row_expir_ts_x']]).all(axis=1)]

                          

df['row_eff_ts'] = df['row_eff_ts_x']

df['row_expir_ts'] = df['row_expir_ts_y']
df['row_expir_ts'] = df.apply(lambda x: x['row_expir_ts'] if not pd.isnull(x['row_expir_ts']) else x['row_expir_ts_x'], axis=1)
df = df[orig_columns]


# Example
# ID	row_eff_ts	row_expir_ts
# 2323	1/1/2000	2/15/2010
# 2323	2/15/2010	5/10/2015
# 2323	9/10/2018	11/4/2019
# 2323	11/4/2019	10/30/2020
# 2323	10/31/2020	12/31/9999

# Expected output
# ID	row_eff_ts	row_expir_ts
# 2323	1/1/2000	5/10/2015
# 2323	9/10/2018	10/30/2020
# 2323	10/31/2020	12/31/9999






from pandas import  DataFrame

df1 = DataFrame({'col1':[1,2,3], 'col2':[2,3,4]})
df2 = DataFrame({'col1':[4,2,5], 'col2':[6,3,5]})


print(df2[~df2.isin(df1).all(1)])
print(df2[(df2!=df1)].dropna(how='all'))
print(df2[~(df2==df1)].dropna(how='all'))

