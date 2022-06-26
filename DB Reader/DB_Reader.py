
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 20:27:03 2021
@author: hayes

Script uses two local python scripts refer to those on what they do.
Rolls through a list of Database Servers accessing each database to get:  
    Table names
    View names
    stored prcoedure names
    
Then it combines the Views and Tables into a single Excel file
Then outputs the stored procedures into a singel excel file
    

"""

import pandas as pd
import sql
import shared_functions as sf



all_tbl = []
all_proc = []
for srvr in sql.server_lst:
    con = sf.ConnectToDBServer(srvr)

    qry = 'SELECT name FROM sys.databases'

    df = pd.read_sql(qry, con)



    tbl = []
    vw = []
    proc = []
    for database in df['name']:
        # skip these due to system databases 
        if database in sql.system_db:
            continue
        
        try:
            qry = 'USE ' + database
            con.execute(qry)
        except:
            print('no access to:  ' + srvr + '.' + database)
            continue
        
        tbl.append(pd.read_sql(sql.tbl_qry, con))
        vw.append(pd.read_sql(sql.vw_qry, con))
        proc.append(pd.read_sql(sql.proc_qry, con))
            
    # end database loop
    
    df_tbl = pd.concat(tbl)
    df_vw = pd.concat(vw)
    df_proc = pd.concat(proc)
    
    
    df_tbl['Type'] = 'Table'
    df_vw['Type'] = 'View'
    df_tbl = pd.concat([df_tbl, df_vw])
    df_tbl['Server'] = srvr

    df_proc['Server'] = srvr

    all_tbl.append(df_tbl[['Server', 'db_nm', 'schema_nm', 'table_nm', 'column_nm', 'data_type', 'nullable', 'column_ordr', 'Type']])
    all_proc.append(df_proc[['Server', 'db_nm', 'schema_name', 'sproc_name']])
# end loop
del tbl, vw, proc, df_tbl, df_vw, df_proc


df_all_tbl = pd.concat(all_tbl)
df_all_proc = pd.concat(all_proc)

sf.write_out_files(df_all_tbl, 'database_tables.xlsx', 'tables')
sf.write_out_files(df_all_proc, 'database_sprocs.xlsx', 'sprocs')
