# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 20:35:40 2021

@author: hayes
"""

import pyodbc as db
import pandas as pd

# https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/pages/introduction.html
# Install:  conda install -c conda-forge pandas-profiling
# if run into issues, uninstall pandas and pandas-profiling, then install pandas-profiling
from pandas_profiling import ProfileReport
# import visions

sample_size = str(10000)


def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')


df = pd.read_excel('database_tables.xlsx')[['Server', 'db_nm', 'schema_nm', 'table_nm']].drop_duplicates()

for srvr in df['Server'].drop_duplicates():

    print(srvr)
    con = ConnectToDBServer(srvr)

    for i in df[df['Server'] == srvr].index:

        if df['db_nm'][i] in ['master', 'msdb', 'pubs']:
            continue
        
        tbl_nm = '[' + df['db_nm'][i] + '].[' + df['schema_nm'][i] + '].[' + df['table_nm'][i] + ']'
        print(tbl_nm)
        qry = 'SELECT TOP ' + sample_size + ' * FROM ' + tbl_nm + ' ORDER BY NEWID()'
        
        df_tbl_data = pd.read_sql(qry, con)
        
        # issue here
        profile = ProfileReport(
            df_tbl_data,
            title=srvr + ': ' + tbl_nm,
            explorative=True)
        
        profile.to_file('results\\' + srvr + '-' + tbl_nm + '.html')
        
    con.close()





