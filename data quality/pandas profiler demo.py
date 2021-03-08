# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 11:48:10 2021

@author: hayes
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from pandas_profiling import ProfileReport
import pyodbc




server = 'localhost'
database = 'GoogleAnalytics'


cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')

# qry = 'SELECT * FROM SiteVisitsLog'
qry = 'SELECT * FROM eCommerce..Product'

df = pd.read_sql(qry, cnxn)


# some info but not sophisticated
df.describe()



# https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/pages/introduction.html
# Install:  conda install -c conda-forge pandas-profiling


# generates an HTML file
profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
profile.to_file('GoogleAnalytics.html')