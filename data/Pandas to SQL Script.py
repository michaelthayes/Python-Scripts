# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 08:27:29 2021

@author: Mike
"""

import pandas as pd
import numpy as np
import sqlalchemy

dates = pd.date_range('20130101',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))



print(pd.io.sql.get_schema(df.reset_index(), 'data'))


# The below can be used to generate it specific to a DB
url = 'mssql+pyodbc://?trusted_connection=yes'
con = sqlalchemy.create_engine(url)
print(pd.io.sql.get_schema(df.reset_index(), 'data', con=con))




def SQL_INSERT_STATEMENT_FROM_DATAFRAME(SOURCE, TARGET):
    sql_texts = []
    for index, row in SOURCE.iterrows():       
        sql_texts.append('INSERT INTO '+TARGET+' ('+ str(', '.join(SOURCE.columns))+ ') VALUES '+ str(tuple(row.values)))        
    return sql_texts

rslt = SQL_INSERT_STATEMENT_FROM_DATAFRAME(df, 'results')
print('\n'.join(rslt))