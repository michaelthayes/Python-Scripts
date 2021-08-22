# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 21:03:28 2021

@author: hayes
"""

import pandas as pd
import numpy as np
from os import path



# build out the temp table. Takes a bit.
n_rows = 1_000_000
n_cols = 1000
for i in range(1, 3):
    filename = 'analysis_%d.csv' % i
    file_path = path.join('csv_files', filename)
    df = pd.DataFrame(np.random.uniform(0, 100, size=(n_rows, n_cols)), columns=['col%d' % i for i in range(n_cols)])
    print('Saving', file_path)
    df.to_csv(file_path, index=False)
df.head()

del df, file_path, filename, i, n_cols, n_rows



# dask example
import dask.dataframe as dd
ds = dd.read_csv('csv_files/*.csv')

# convert to hdf5 file
ds.to_hdf('hdf5_files_dask/analysis_01_01.hdf5', key='table')


# convert to Parquet file
ds.to_parquet('parquet_files_dask/analysis_01_01.parquet')



ds.head()


quantile = ds.col1.quantile(0.1).compute()

ds['col1_binary'] = ds.col1 > ds.col1.quantile(0.1)

ds = ds[(ds.col2 > 10)]

group_res = ds.groupby('col1_binary').col3.mean().compute()

suma = ds.sum().sum().compute()

del ds
