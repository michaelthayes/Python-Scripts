# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 20:51:00 2022

@author: hayes
"""

# This is a quick script to guess at which fields are populated by an ETL process and which are not



import pandas as pd
import pyodbc as db

def ConnectToDBServer(ServerName : str) -> db.connect:
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')


con = ConnectToDBServer('localhost')

qry = 'SELECT *  FROM [Insurance].[dbo].[factMemberClaims]'
df = pd.read_sql(qry, con)#.astype('str')
df.info()


def empty_or_not(s):
    # print(s)
    if not bool(s):
        return('empty')
    else:
        return('etl')

check = pd.DataFrame()
for col in df.columns:
    check[col] = df[col].apply(empty_or_not)
# check

a = df.value_counts()

df.to_excel('hello.xlsx')

df_pivot = df.pivot_table(index=[['etl','empty']], columns=df.columns, aggfunc='count')


# get unique list of values
val = []
for col in df:
    val = df[col].unique()
    
a = df.groupby(col).count()
    






