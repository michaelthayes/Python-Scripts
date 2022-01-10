# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 20:01:16 2022

@author: hayes

INFO:  replicates what the sproc uspGetEmployeeManagers does. Works through the hierarchyid datatype
"""

import pandas as pd
import pyodbc as db

def ConnectToDBServer(ServerName : str) -> db.connect:
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')


con = ConnectToDBServer('localhost')


qry = 'SELECT BusinessEntityID, JobTitle, BirthDate, MaritalStatus, Gender, HireDate, CONVERT(VARCHAR(25), OrganizationNode) as \'OrganizationNode\' FROM AdventureWorks2019.HumanResources.Employee'
df_emp = pd.read_sql(qry, con)
# df_emp.info()

qry = 'SELECT BusinessEntityID, Title, FirstName, MiddleName, LastName, Suffix FROM AdventureWorks2019.Person.Person'
df_pers = pd.read_sql(qry, con)
# df_pers.info()

# cleanses the list
def cleanse_org(l: list):
    if l == None:
        return ''
    l = list(filter(len, l))
    return(list(filter(None, l)))

#parse out the hierarchyid datatype
df_org = pd.merge(df_pers, df_emp, on='BusinessEntityID')
df_org['OrganizationNode'] = df_org['OrganizationNode'].str.split('/')
df_org['OrganizationNode'] = df_org['OrganizationNode'].apply(cleanse_org)



# setup the columns
df_org['employee'] = ''
df_org['manager'] = ''




def get_manager(l: list):
    if len(l) > 0:
        return ''.join(map(str, l[:-1]))
    else:
        return('')
    
    
def get_employee(l: list):
    if len(l) > 0:
        return ''.join(map(str, l))
    else:
        return('')


# assign out the manager and employee
df_org['manager'] = df_org['OrganizationNode'].apply(get_manager)
df_org['employee'] = df_org['OrganizationNode'].apply(get_employee)

# build an employee mapping table, then apply it
emp = dict(zip(df_org['employee'], df_org['BusinessEntityID']))
df_org['manager'] = df_org['manager'].map(emp)
df_org['employee'] = df_org['employee'].map(emp)

# restructure the columns
df_emp = df_org[['employee', 'manager', 'Title', 'FirstName', 'MiddleName', 'LastName',
       'Suffix', 'JobTitle', 'BirthDate', 'MaritalStatus', 'Gender',
       'HireDate']]
df_mgr = df_org[['employee', 'Title', 'FirstName', 'MiddleName', 'LastName', 'Suffix', 'JobTitle']]

# put it all together
df_final = df_emp.merge(df_mgr, how='inner', left_on=['manager'], right_on=['employee'], suffixes=('','_mgr'))






