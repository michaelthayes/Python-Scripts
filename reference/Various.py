# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:42:23 2019

@author: mike
"""
import pandas as pd
import pyodbc as db


def ConnectToDBServer(ServerName : str) -> db.connect:
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')




def readSQLScriptFromFile(scriptPath : str, cur : db.Cursor) -> []:
    result = []
    with open(scriptPath, 'r') as inp:
        i=0
        sqlQuery=''
        for line in inp:
            if line == 'GO\n':
                i=i+1
                print(f'Query #{i}')
                # print(sqlQuery)
                
                cur.execute(sqlQuery)
                
                try:
                    result.append(pd.DataFrame.from_records(cur.fetchall(), columns=[x[0] for x in cur.description]))
                except:
                    print('no results')


#                print('****')
                sqlQuery = ''
            elif 'PRINT' in line:
                disp = line.split("'")[1]
                print(f'{disp}')
            else:
                sqlQuery = sqlQuery + line
    inp.close()
    return(result)
    
# End readSQLScriptFromFile



## Function in order to retrieve the results and add them to the results
def PullResults(cur):
    column_names = [col[0] for col in cur.description]
    Result = []
    for row in cur.fetchall():
        Result.append({name: row[i] for i, name in enumerate(column_names)})
    return Result


# connection information
# quoted = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=(localDb)\ProjectsV14;DATABASE=database")
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
def ReadFileStoretoSQLServer(file, schema, tableName, engine):
    df = pd.read_csv(file)
    
    df.to_sql(tableName, schema=schema, con = engine)
    return df


# connection information
# quoted = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=(localDb)\ProjectsV14;DATABASE=database")
# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
def ReadSQLServertoFileStore(file, schema, tableName, engine):
    df = pd.read_sql(tableName, schema=schema, con=engine)

    df = pd.write_csv(file)
    return df




######################################################################################
# paramters
#url_base = 'http://url-here.doman-here.com/path'
#headers = {'content-type':'application/json'}
#userID = 'username'
#pwdID = 'possword'


#url_data =  'Bulkd JSON Payload here'

#print(url_data)

#response = requests.post(url_base, data=url_data, auth=(userID, pwdID), headers=headers)







## not complete
####  BELOW iterates through multiple results sets.
def loop_through_results(cur, sqlQuery : str, df : pd.DataFrame):
    i=0
    #Fetch all rows using a while loop
    while i < int(df.count()):
        
        
        # loop through the results
        cur.execute(sqlQuery + str(df.iloc[i,0]))
        print(str(df.iloc[i,0]))
    
    
        # Results set 1
        Result1 = PullResults(cur)
    
        
        cur.nextset ()
        # Results set 2
        cur.nextset ()
        
        #Results set 3
        Result3 = PullResults(cur)
        
        # update the below to be an array
        PolicyResults = PolicyResults.append(pd.DataFrame(Result1))
        CoverageResults = CoverageResults.append(pd.DataFrame(Result3))
        
        i = i + 1

    return df



