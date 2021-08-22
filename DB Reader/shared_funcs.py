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
import pyodbc as db


@timefunc
def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')


@timefunc
# if you get an error below: pip install xlsxwriter
def write_out_files(df, filename, sheet):
    writer = pd.ExcelWriter(filename) 
    df.to_excel(writer, sheet_name=sheet, index=False)
    
    # Auto-adjust columns' width
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet]. set_column(col_idx, col_idx, column_width)
    writer.save()
