# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 11:15:40 2022

@author: hayes
"""

import sqlalchemy
from sqlalchemy.engine import URL
import pandas as pd


def ConnectToDBServerV2(ServerName : str, DatabaseName : str ='master'):
#Create connection string to connect DBTest database with windows authentication
    odbc_str = 'DRIVER={SQL Server};SERVER=' + ServerName + ';Database=' + DatabaseName + ';Trusted_Connection=yes;'
    connection_url = URL.create("mssql+pyodbc", query={'odbc_connect': odbc_str})
    return sqlalchemy.create_engine(connection_url)

con = ConnectToDBServerV2('localhost')

df = pd.read_excel('output.xlsx')



def sql_drop_create_statement(df : pd.DataFrame, tablename : str, schema : str = 'dbo'):
    s = 'DROP TABLE IF EXISTS ' + schema + '.' + tablename + ';'
    s += pd.io.sql.get_schema(df, name = tablename, con = con, schema = schema)
    s = s.replace('TEXT', 'VARCHAR(255)')
    s = s.replace('FLOAT(53)', 'DECIMAL(20,9)')
    return s

s = sql_drop_create_statement(df, 'SuperOutput')

df = pd.read_sql_query('SELECT * FROM eCommerce.dbo.OnlineSales', con)

df['OrderDate'] = pd.to_datetime(df['OrderDate'])

s = sql_drop_create_statement(df, 'SuperOutput')

df.info()
dfn = df.convert_dtypes()
sn = sql_drop_create_statement(df, 'SuperOutput')