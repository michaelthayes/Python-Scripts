# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 17:48:38 2021

@author: hayes
"""


import pandas as pd
import pyodbc as db

def ConnectToDBServer(ServerName):
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')




def readSQLScriptFromFile(scriptPath, cur):
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




con = ConnectToDBServer('localhost')

cur = con.cursor()

result = readSQLScriptFromFile('Test-Reading-From-SQL-File.sql', cur)

con.close()


df = pd.concat(result)


# Save the result array into a single spreadsheet
wrksht_names = ['Calendar','SiteVisitsLog','Categories']

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
#write each DataFrame to a specific sheet
i=0
for df_sheet in result:
    df_sheet.to_excel(writer, wrksht_names[i], index=True)
    i+=1




