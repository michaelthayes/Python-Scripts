# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:12:30 2021

@author: hayes
"""

import pandas as pd






# sets the index of a dataframe based on the mapper
def set_index_mapper(df, mapper, col='source'):

    idx = mapper[mapper['idx'] == 'Y']

    if not idx.empty:
        for i, data in idx.iterrows():
            if col == 'source':
                if data['source'] not in df.columns:
                    raise ValueError('WARNING: dataframe.columns is missing: ' + data['source'])
            else:
                if data['target'] not in df.columns:
                    raise ValueError('WARNING: dataframe columns is missing: ' + data['target'])
    
        df = df.set_index(idx['source'].to_list())
    return(df)


# compares 2 dataframes with different columns, requires a mapper
def compare_df_cols(source, target, mapper, eq_ne = 'eq'):
    # df = pd.DataFrame(columns=source.columns.to_list(), index=source.index.names.to_list())
    df = pd.DataFrame(index=source.index)
    # df.set_index(source.index.names)
    
    for i, data in mapper[mapper['idx'] != 'Y'].iterrows():
        if data['source'] not in source.columns:
            raise ValueError('WARNING: source columns is missing: ' + data['source'])
        
        if data['target'] not in target.columns:
            raise ValueError('WARNING: target columns is missing: ' + data['target'])
        
        if eq_ne == 'eq':
            df_tmp = source[data['source']].eq(target[data['target']])
        else:
            df_tmp = source[data['source']].ne(target[data['target']])
        df_tmp.name = data['source']
        df = pd.concat([df, df_tmp], axis=1)
        
    return(df)


def return_diffs(source, target, result, mapper):
    
    cols = mapper[mapper['idx']!='Y'][["source","target"]]
    target = target.rename(columns=cols.set_index('target')['source'])
    
    
    df = source[result == True].dropna(axis=0, how='all') # drops only when all are NaN
    df = df.append(target[result == True].dropna(axis=0, how='all'))
    
    
    # idx = mapper[mapper['idx']=='Y']
    # df.set_index(mapper[mapper['idx']=='Y']['source'].to_list())
    
    return(df.sort_index())



df = pd.DataFrame({'cost': [250, 150, 100],
                   'revenue': [100, 250, 300],
                   'letters':['A', 'B', 'C'],
                   'numbers':['1', '2', '3']})


df2 = pd.DataFrame({'cost.new': [250, 160, 100],
                   'revenue.new': [100, 250, 300],
                   'letters':['A', 'B', 'D'],
                   'numbers':['1', '2', '4']})

# Dependent on a mapper config file
# must be in the format of:
# source,target,idx
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>



df_map = pd.read_csv('mapper_config.csv')

df_idx = set_index_mapper(df, df_map, col='source')
df2_idx = set_index_mapper(df2, df_map, col='target')

result = compare_df_cols(df_idx, df2_idx, df_map, 'ne')


return_diffs(df_idx, df2_idx, result, df_map)



idx = df_map[df_map['idx'] == 'Y']
df_idx.index.names


# eq
df = df_idx[result == True].dropna(axis=0, how='all') # drops only when all are NaN
df.append(df2_idx[result == True].dropna(axis=0, how='all'))

# ne
df_idx[result == True]
df2_idx[result == True]


# are these returning the right responses?
df_idx[result == True]
df2_idx[result == True]


