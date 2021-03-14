# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:12:30 2021

@author: hayes
"""

import pandas as pd







def set_index_mapper(data : pd.DataFrame, mapper : pd.DataFrame, col : str ='source') -> pd.DataFrame:
    """Sets the index of the dataframe based on the mapper
    

    Parameters
    ----------
    data : pd.DataFrame
        Source or Target frame to be assigned an index.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from source to target.
    col : str ('source', 'target'), optional
        Specifies the passed in DataFrame is the source or the target (default is 'source').

    Raises
    ------
    ValueError
        WARNING: dataframe.columns is missing: <field name>

    Returns
    -------
    pd.DataFrame
        Altered DataFrame with appropriate index(es) assigned.

    """

    idx = mapper[mapper['idx'] == 'Y']

    if not idx.empty:
        for i, d in idx.iterrows():
            if col == 'source':
                if d['source'] not in data.columns:
                    raise ValueError('WARNING: dataframe.columns is missing: ' + d['source'])
            else:
                if d['target'] not in data.columns:
                    raise ValueError('WARNING: dataframe.columns is missing: ' + d['target'])

        data = data.set_index(idx['source'].to_list())
    return data



def compare_df_cols(source : pd.DataFrame, target : pd.DataFrame, mapper : pd.DataFrame, eq_ne : str = 'eq') -> pd.DataFrame:
    """Compares 2 dataframes with different columns using the mapping to link them together
    

    Parameters
    ----------
    source : pd.DataFrame
        Source frame to be compared.
    target : pd.DataFrame
        Target frame to be compared.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from source to target.
    eq_ne : str (eq, ne), optional
        eq for equal comparison, ne for not equal comparison is the source or the target (default is 'source').

    Raises
    ------
    ValueError
        WARNING: source columns is missing: <field name>
        WARNING: target columns is missing: <field name>

    Returns
    -------
    pd.DataFrame
        Results will be in a True/False format.

    """
 
    df = pd.DataFrame(index=source.index)


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

    return df



def return_diffs(source : pd.DataFrame, target : pd.DataFrame, result : pd.DataFrame, mapper : pd.DataFrame) -> pd.DataFrame:
    """Takes in a source and target dataframe, uses the results and mappers to return back a single dataframe with all actual differences
    

    Parameters
    ----------
    source : pd.DataFrame
        Source frame uto be assigned an index.
    target : pd.DataFrame
        Target frame to be assigned an index.
    result : pd.DataFrame
        True/False results of comparison check.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from source to target.

    Returns
    -------
    pd.DataFrame
        All matching results

    """

    cols = mapper[mapper['idx']!='Y'][['source','target']]
    target = target.rename(columns=cols.set_index('target')['source'])

    df = source[result == True].dropna(axis=0, how='all') # drops only when all are NaN
    df = df.append(target[result == True].dropna(axis=0, how='all'))
    
    return df.sort_index()



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


findings = return_diffs(df_idx, df2_idx, result, df_map)




