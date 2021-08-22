# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 20:27:03 2021

@author: hayes
"""

import pandas as pd
import sql
import shared_funcs as sf



df_all_tbl = pd.DataFrame()
df_all_proc = pd.DataFrame()
for srvr in sql.server_lst:
    con = sf.ConnectToDBServer(srvr)

    qry = 'SELECT name FROM sys.databases'

    df = pd.read_sql(qry, con)


    cur = con.cursor()


    df_tbl = pd.DataFrame()
    df_vw = pd.DataFrame()
    df_proc = pd.DataFrame()
    for database in df['name']:
        
        if database in sql.system_db:
            continue
        
        try:
            qry = 'USE ' + database
            cur.execute(qry)
        except:
            print('No access to: ' + srvr + '.' + database)
            continue
    
    
        df_tbl = df_tbl.append(pd.read_sql(sql.tbl_qry, con))
        df_vw = df_vw.append(pd.read_sql(sql.vw_qry, con))
        df_proc = df_proc.append(pd.read_sql(sql.proc_qry, con))
    # end database loop
    
    df_tbl['Type'] = 'Table'
    df_vw['Type'] = 'View'
    df_tbl = df_tbl.append(df_vw)
    df_tbl['Server'] = srvr

    df_proc['Server'] = srvr

    df_all_tbl = df_all_tbl.append(df_tbl[['Server', 'db_nm', 'schema_nm', 'table_nm', 'column_nm', 'data_type', 'nullable', 'column_ordr', 'Type']])
    df_all_proc = df_all_proc.append(df_proc[['Server', 'db_nm', 'schema_name', 'sproc_name']])
# end loop
del df_tbl, df_proc





sf.write_out_files(df_all_tbl, 'database_tables.xlsx', 'tables')
sf.write_out_files(df_all_proc, 'database_sprocs.xlsx', 'sprocs')









