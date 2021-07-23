# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 20:27:03 2021

@author: hayes
"""

import pandas as pd
import pyodbc as db
import sql


def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')






con = ConnectToDBServer('localhost')

qry = 'SELECT name FROM sys.databases'

df = pd.read_sql(qry, con)


cur = con.cursor()


df_tbl = pd.DataFrame()
df_vw = pd.DataFrame()
df_proc = pd.DataFrame()
for database in df['name']:
    qry = 'USE ' + database
    cur.execute(qry)
    
    df_tbl = df_tbl.append(pd.read_sql(sql.tbl_qry, con))
    df_vw = df_vw.append(pd.read_sql(sql.vw_qry, con))
    df_proc = df_proc.append(pd.read_sql(sql.proc_qry, con))


# now what?





















