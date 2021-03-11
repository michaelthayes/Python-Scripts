# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:12:30 2021

@author: hayes
"""

import pandas as pd






# compares 2 dataframes with different columns, requires a mapper
def set_index_mapper(source, target, mapper):

    idx = mapper[mapper['idx'] == 'Y']

    if not idx.empty:
        for i, data in idx.iterrows():
            if data['source'] not in source.columns:
                raise ValueError('WARNING: source.columns is missing: ' + data['source'])
            
            if data['target'] not in target.columns:
                raise ValueError('WARNING: target columns is missing: ' + data['target'])
    
        source = source.set_index(idx['source'].to_list())
        target = target.set_index(idx['target'].to_list())
    return(source, target)


def compare_df_cols(source, target, mapper):
    df = pd.DataFrame()

    idx = mapper[mapper['idx'] == 'Y']

    if not idx.empty:
        for i, data in idx.iterrows():
            if data['source'] not in source.columns:
                raise ValueError('WARNING: source.columns is missing: ' + data['source'])
            
            if data['target'] not in target.columns:
                raise ValueError('WARNING: target columns is missing: ' + data['target'])
    
        source = source.set_index(idx['source'].to_list())
        target = target.set_index(idx['target'].to_list())
    
    for i, data in mapper[mapper['idx'] != 'Y'].iterrows():
        if data['source'] not in source.columns:
            raise ValueError('WARNING: source columns is missing: ' + data['source'])
        
        if data['target'] not in target.columns:
            raise ValueError('WARNING: target columns is missing: ' + data['target'])
        
        df_tmp = source[data['source']].eq(target[data['target']])
        df_tmp.name = data['source']
        df = pd.concat([df, df_tmp], axis=1)
        
    return(df)



df = pd.DataFrame({'cost': [250, 150, 100],
                   'revenue': [100, 250, 300],
                   'letters':['A', 'B', 'C']})


df2 = pd.DataFrame({'cost.new': [250, 150, 100],
                   'revenue.new': [100, 250, 300],
                   'letters':['A', 'B', 'D']})

# Dependent on a mapper config file
# must be in the format of:
# source,target,idx
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>





df_map = pd.read_csv('mapper_config.csv')

df_idx, df2_idx = set_index_mapper(df, df2, df_map)

result = compare_df_cols(df, df2, df_map)

result

# are these returning the right responses?
df_idx[result == False]
df2_idx[result == False]


