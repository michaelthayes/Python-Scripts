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




df_all_tbl = pd.DataFrame()
df_all_proc = pd.DataFrame()
for srvr in sql.server_lst:
    con = ConnectToDBServer(srvr)

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
    # end database loop
    
    df_tbl['Type'] = 'Table'
    df_vw['Type'] = 'View'
    df_tbl = df_tbl.append(df_vw)
    df_tbl['Server'] = srvr

    df_proc['Server'] = srvr

    df_all_tbl = df_all_tbl.append(df_tbl[['Server', 'db_nm', 'schema_nm', 'table_nm', 'column_nm', 'column_ordr', 'Type']])
    df_all_proc = df_all_proc.append(df_proc[['Server', 'db_nm', 'schema_name', 'sproc_name']])
# end loop
del df_tbl, df_proc






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


write_out_files(df_all_tbl, 'database_tables.xlsx', 'tables')
write_out_files(df_all_proc, 'database_sprocs.xlsx', 'sprocs')









