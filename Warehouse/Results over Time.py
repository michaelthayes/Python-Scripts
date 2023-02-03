# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:21:04 2023

@author: hayes
"""


import pandas as pd
from datetime import date
import sqlite3

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


begin_date = date(2006, 1, 1)
end_date = date(2007, 12, 31)
df_dates = pd.DataFrame({'dt':pd.date_range(begin_date, periods=((end_date - begin_date).days))})
df_dates.info()



df = pd.read_csv('integration_table.csv')

df['row_eff_dttm'] = pd.to_datetime(df['row_eff_dttm'])
df['row_expir_dttm'] = pd.to_datetime(df['row_expir_dttm'], errors='coerce') # need coerce for 9999-12-31
df.fillna(pd.Timestamp.max, inplace=True)


#Make the db in memory
conn = sqlite3.connect(':memory:')
#write the tables
df_dates.to_sql('dates', conn, index=False)
df.to_sql('data', conn, index=False)

qry = '''SELECT d.dt, data.*
            FROM dates d
            INNER JOIN data data ON d.dt > data.row_eff_dttm AND d.dt <= data.row_expir_dttm '''

df_result1 = pd.read_sql(qry, conn)

qry = '''SELECT d.dt, COUNT(*)
            FROM dates d
            INNER JOIN data data ON d.dt > data.row_eff_dttm AND d.dt <= data.row_expir_dttm
        GROUP BY d.dt '''

df_result2 = pd.read_sql(qry, conn)


conn.close()







