# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 20:06:24 2022

@author: hayes
# script is to do similar operations as the sproc uspSearchCandidateResumes
"""


import pandas as pd
import pyodbc as db

def ConnectToDBServer(ServerName : str) -> db.connect:
#Create connection string to connect DBTest database with windows authentication
    return db.connect('DRIVER={SQL Server};SERVER=' + ServerName + ';Trusted_Connection=yes')


con = ConnectToDBServer('localhost')

qry = 'select * FROM AdventureWorks2019.HumanResources.JobCandidate jc'
df_cand = pd.read_sql(qry, con)

 
