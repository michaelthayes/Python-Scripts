# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 13:10:17 2022

@author: hayes
"""

import pandas as pd
import datetime
import numpy as np


dti = pd.to_datetime(
    ["1/1/2018", np.datetime64("2018-01-01"), datetime.datetime(2018, 1, 1)]
)

df = pd.date_range("2018-01-01", periods=20, freq="H")
df = df.to_frame(index=False)
df.dtypes



dti = pd.concat([df, df, df], axis=1)
dti.columns = ['a','b','c']


# Assign 1 column to UTC
dti['a'] = pd.to_datetime(dti['a'], utc=True)
dti.dtypes

# Assign the same column to eastern
dti['a'] = dti['a'].dt.tz_convert('US/Eastern')
dti.dtypes


# now do it for all column
# first, get the list of datetimes
df_tz = dti.select_dtypes('datetime64')

# assign all the datetime columns as UTC
dti[df_tz.columns] = df_tz.apply(lambda x: pd.to_datetime(x, utc=True))
dti.dtypes

# assign all the datetime columns as US/Eastern
dti[df_tz.columns] = df_tz.apply(lambda x: pd.to_datetime(x, utc=True).dt.tz_convert('US/Eastern'))
dti.dtypes



dti['a'].dt.normalize()
dti['a'].dt.date
