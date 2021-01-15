# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 11:23:47 2019

@author: mike
"""

import pandas as pd


dfEcommerce = pd.read_csv('Data/Ecommerce Purchases')

dfStudent = pd.read_csv('Data/student-mat.csv', ';')

dfStudent.head()
type(dfStudent)


## Store SQL
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

dfStudent.to_sql('my_table', engine)

## Read from SQL
sqldf = pd.read_sql("select * from my_table where sex = 'F'", con=engine)


sqldf = sqldf.set_index('index')

sqldf.head()
dfStudent.head()


