# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:42:23 2019

@author: mike
"""

#Create connection string to connect DBTest database with windows authentication
#con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + Database + ';Trusted_Connection=yes')
#cur = con.cursor()
def readSQLScriptFromFile(scriptPath, con):
    with open(scriptPath, 'r') as inp:
        i=0
        sqlQuery=''
        for line in inp:
            if line == 'GO\n':
                i=i+1
                print(f'Query #{i}')
                con.execute(sqlQuery)
#                print(sqlQuery)
#                print('****')
                sqlQuery = ''
            elif 'PRINT' in line:
                disp = line.split("'")[1]
                print(f'{disp}')
            else:
                sqlQuery = sqlQuery + line
    inp.close()



## Function in order to retrieve the results and add them to the results
def PullResults(cur):
    column_names = [col[0] for col in cur.description]
    Result = []
    for row in cur.fetchall():
        Result.append({name: row[i] for i, name in enumerate(column_names)})
    return Result



######################################################################################
# paramters
#url_base = 'http://url-here.doman-here.com/path'
#headers = {'content-type':'application/json'}
#userID = 'username'
#pwdID = 'possword'


#url_data =  'Bulkd JSON Payload here'

#print(url_data)

#response = requests.post(url_base, data=url_data, auth=(userID, pwdID), headers=headers)



