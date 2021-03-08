# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import pyodbc
import pydqc



server = 'localhost'
database = 'GoogleAnalytics'


cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

qry = 'SELECT * FROM SiteVisitsLog'

df = pd.read_sql(qry, cnxn)


df.describe()


####  NOTHING BELOW WORKS


pydqc.infer_schema(df, 'hello', output_root='.', sample_size=1.0, type_threshold=0.5, n_jobs=1, base_schema=None)


pydqc.data_summary.data_summary('hello', df, 'hello', sample_size=1.0, sample_rows=100, output_root='', n_jobs=1)

