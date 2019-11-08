# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 11:23:47 2019

@author: mike
"""

import pandas as pd

df = pd.read_csv('Data/Ecommerce Purchases')

df = pd.read_csv('Data/student-mat.csv', ';')

df.head()



## SQL Retrieval
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

df.to_sql('my_table', engine)
sqldf = pd.read_sql('my_table', con=engine)

df.head()
sqldf