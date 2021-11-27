# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 09:32:23 2021

@author: hayes
"""


import pandas as pd
import pyodbc as db

def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')#.execution_options(stream_results=True)


def process_sql_using_pandas(con):
    for chunk_dataframe in pd.read_sql_query('select * from GoogleAnalytics..SiteVisitsLog', con, chunksize=1000):
        print(f"Got dataframe w/{len(chunk_dataframe)} rows")
    return(chunk_dataframe)

con = ConnectToDBServer('localhost')
df = process_sql_using_pandas(con)

chunk = pd.read_sql_query('select * from GoogleAnalytics..SiteVisitsLog', con, chunksize=1000, parse_dates=True)
df = pd.concat(chunk)


df = pd.read_sql_query('select name from sys.databases', con)
for i, d in df.iterrows():
    print('The database name is {}'.format(d['name']))