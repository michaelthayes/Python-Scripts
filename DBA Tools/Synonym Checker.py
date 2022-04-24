# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 19:19:55 2021

@author: michael.hayes
 
Scripts scans through all synonyms and servers, looking for sprocs which
access linked servers
"""

import pandas as pd
import pyodbc as db


server_lst = [ 'PRVAMDBRPT01.CLOUD.ICG360.NET',
                'PRVAMDBRPT02.CLOUD.ICG360.NET',
                'PRVAMDBRPT03.CLOUD.ICG360.NET',
                'PRVAMDBRPT04.CLOUD.ICG360.NET',
                'PRVAMRPTME01.CLOUD.ICG360.NET',
                'PRVAMIVANSAPP01.CLOUD.ICG360.NET',
                'PRVAMIVANSAPP02.CLOUD.ICG360.NET',
                'DVVAMDBRPT01.CLOUD.ICG360.NET', # DM Dev Box
                'STVAMDBRPT01.CLOUD.ICG360.NET', # DM Staging box
                'DVVAMDBDEV01.CLOUD.ICG360.NET', # Actuarial Server
                'PRVAMDBDSS02.CLOUD.ICG360.NET']


system_db = ['master',
             'model',
             'msdb',
             'SSISDB',
             'tempdb',
             'ReportServer',
             'ReportServer_1',
             'ReportServer_1TempDB',
             'ReportServer_3',
             'ReportServer_3TempDB',
             'ReportServerTempDB']



search_list = ['PRVAMDBRPT01',
                'PRVAMDBRPT02',
                'PRVAMDBRPT03',
                'PRVAMDBRPT04'
                'PRVAMIVANSAPP01',
                'PRVAMIVANSAPP02',
                'DVVAMDBDEV01',
                'PRVAMDBDSSPRI', # ICM Server to be shut off 12/31
                'PRVAMDBDSS02']  # ICM Server to be shut off 12/31


sproc_search = "SELECT	DB_NAME() as 'database', \
                    ssc.name as 'schema_name', \
                    sp.name AS 'object_name', \
                    'sproc' as 'object_type', \
                    UPPER(object_definition(sp.object_id)) as 'object_txt' \
                FROM sys.procedures sp WITH (NOLOCK) \
                    INNER JOIN sys.schemas ssc WITH (NOLOCK) ON sp.schema_id = ssc.schema_id \
                WHERE sp.name not like 'dt_%' \
                AND object_definition(sp.object_id) <> '' "

view_search = "SELECT	DB_NAME() as 'database', \
                    ssc.name as 'schema_name',  \
                    ss.name AS 'object_name', \
                    'view' as 'object_type', \
                    UPPER(object_definition(ss.object_id)) as 'object_txt' \
                FROM sys.views ss WITH (NOLOCK) \
                    INNER JOIN sys.schemas ssc WITH (NOLOCK) ON ss.schema_id = ssc.schema_id \
                WHERE ss.name not like 'dt_%' \
                AND object_definition(ss.object_id) <> '' "                


trigger_search = "SELECT	DB_NAME() as 'database', \
                    ssc.name as 'schema_name', \
                    st.name AS 'object_name', \
                    'trigger' as 'object_type', \
                    UPPER(object_definition(st.object_id)) as 'object_txt' \
                from sys.triggers st \
                    INNER JOIN sys.tables stbl \
                        INNER JOIN sys.schemas ssc ON stbl.schema_id = ssc.schema_id \
                    ON st.parent_id = stbl.object_id \
                WHERE object_definition(st.object_id) <> '' "

function_search = "SELECT  DB_NAME() as 'database', \
                    SU.name as 'schema_name', \
                    sf.name AS 'object_name', \
                    'function' as 'object_type', \
                    object_definition(sf.id) as 'object_txt' \
                from  sysobjects sf \
                    INNER JOIN sysusers su ON sf.uid = su.uid \
                WHERE sf.xtype IN ('FN', 'IF', 'TF') \
                AND object_definition(sf.id) <> '' "

synonym_qry = "SELECT DB_NAME() as 'database', \
                    name AS 'synonym_name', \
                    base_object_name AS 'synonym_definition', \
                    COALESCE (PARSENAME (base_object_name, 4), @@servername) AS 'server_name', \
                    COALESCE (PARSENAME (base_object_name, 3), DB_NAME (DB_ID ())) AS 'DB_name', \
                    COALESCE (PARSENAME (base_object_name, 2), SCHEMA_NAME (SCHEMA_ID ())) AS 'schema_name', \
                    PARSENAME (base_object_name, 1) AS 'table_name' \
                FROM sys.synonyms WITH (NOLOCK) "
                

def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')





df_all_obj = pd.DataFrame()
df_all_syn = pd.DataFrame()
df_no_access = pd.DataFrame(columns=['server','database'])
for srvr in server_lst:
    
    con = ConnectToDBServer(srvr)
    print('Connecting to: ' + srvr)

    qry = 'SELECT name FROM sys.databases'

    df = pd.read_sql(qry, con)


    cur = con.cursor()

    df_obj = pd.DataFrame()
    obj = []
    df_syn = pd.DataFrame()
    for database in df['name']:

        # skip these due to system databases 
        if database in system_db:
            continue
        
        try:
            qry = 'USE ' + database
            cur.execute(qry)
            print('Access to: ' + srvr + '.' + database)
        except:
            df_no_access = df_no_access.append(pd.DataFrame([[srvr, database]], columns=['server','database']), ignore_index=True)
            print('NO Access to: ' + srvr + '.' + database)
            continue

        # get synomyms, and return them to the search_list
        df_syn_tmp = pd.read_sql_query(synonym_qry, con)
        if not df_syn_tmp.empty:
             search_list_plus = search_list + df_syn_tmp['synonym_name'].drop_duplicates().tolist()
        
        df_syn = df_syn.append(df_syn_tmp)

        # get all the sproc contents
        df_result = pd.read_sql_query(sproc_search, con)
        df_result = df_result.append(pd.read_sql_query(view_search, con))
        df_result = df_result.append(pd.read_sql_query(trigger_search, con))
        df_result = df_result.append(pd.read_sql_query(function_search, con))

        # scan the objects for matches
        for search_string in search_list_plus:
            # print(search_string)
            # df_tmp = pd.read_sql_query(sproc_search.format(search_string=search_string), con)
            df_tmp = df_result[df_result['object_txt'].str.contains(search_string, case=False)]
            
            if not df_tmp.empty:
                df_tmp = df_tmp[df_tmp.columns[:-1]]  # remove the sproc txt
                if search_string in df_syn_tmp['synonym_name'].tolist():
                    df_tmp[search_string] = df_syn_tmp[df_syn_tmp['synonym_name']==search_string]['server_name'].iloc[0]
                else:
                     df_tmp[search_string] = search_string
                obj.append(df_tmp)
            
            # proc.append(df_tmp)
            # df_obj = df_obj.append(df_tmp)
        #end search loop
    # end database loop
    
    # build out sproc dataframe
    if obj != []:
        df_obj = df_obj.append(pd.concat(obj))
        df_obj['Server'] = srvr
        df_all_obj = df_all_obj.append(df_obj)
    
    #build out synonym dataframe
    df_syn['Server'] = srvr
    df_all_syn = df_all_syn.append(df_syn)
# end  server loop




main_cols = ['Server','database','schema_name','object_name','object_type']
value_cols = list(set(df_all_obj.columns) - set(main_cols))

#  collapse rows
df_all_obj = df_all_obj.fillna('')
df_all_obj = df_all_obj.groupby(main_cols).agg(''.join)
df_all_obj.sort_values(main_cols, inplace=True)
df_all_obj.reset_index(inplace=True)



# df_all_obj = pd.read_excel('sprocs_with_linked_servers.xlsx', sheet_name='Chart')

df_all_obj_list = df_all_obj.melt(id_vars=main_cols, value_vars=value_cols)
df_all_obj_list= df_all_obj_list[df_all_obj_list['value'] != '']
df_all_obj_list.columns = main_cols + ['server_syn_match', 'server_name']
df_all_obj_list.sort_values(main_cols, inplace=True)


# write out the files

with pd.ExcelWriter('db objects_with_linked_servers.xlsx', engine='xlsxwriter') as writer:
    df_all_obj.to_excel(writer, sheet_name='Chart', index=False)
    df_all_obj_list.to_excel(writer, sheet_name='List', index=False)
    df_no_access.to_excel(writer, sheet_name='No Access', index=False)
    
    
df_all_syn.to_excel('DB_Synonyms.xlsx', index=False)


