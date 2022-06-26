# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 12:26:55 2021

@author: hayes
"""



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



import pandas as pd
import sqlalchemy
from sqlalchemy.engine import URL


@timefunc
# connects to the server and database
def ConnectToDBServer(ServerName, DatabaseName='master'):
#Create connection string to connect DBTest database with windows authentication
    odbc_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + ServerName + ';Database=' + DatabaseName + ';Trusted_Connection=yes;'
    connection_url = URL.create("mssql+pyodbc", query={'odbc_connect': odbc_str})
    return sqlalchemy.create_engine(connection_url, fast_executemany=True).connect()



@timefunc
# if you get an error below: pip install xlsxwriter
def write_out_files(df, filename, sheet):
    writer = pd.ExcelWriter(filename) 
    df.to_excel(writer, sheet_name=sheet, index=False)
    
    # Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet].set_column(col_idx, col_idx, column_width)
    writer.save()
