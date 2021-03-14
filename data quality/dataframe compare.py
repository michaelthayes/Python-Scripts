# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:12:30 2021

@author: hayes
"""

import pandas as pd







def set_index_mapper(data : pd.DataFrame, mapper : pd.DataFrame, col : str ='control') -> pd.DataFrame:
    """Sets the index of the dataframe based on the mapper
    

    Parameters
    ----------
    data : pd.DataFrame
        Control or Test frame to be assigned an index.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from control to test.
    col : str ('control', 'test'), optional
        Specifies the passed in DataFrame is the control or the test (default is 'control').

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
            if col == 'control':
                if d['control'] not in data.columns:
                    raise ValueError('WARNING: dataframe.columns is missing: ' + d['control'])
            else:
                if d['test'] not in data.columns:
                    raise ValueError('WARNING: dataframe.columns is missing: ' + d['test'])

        data = data.set_index(idx['control'].to_list())
    return data



def compare_df_cols(control : pd.DataFrame, test : pd.DataFrame, mapper : pd.DataFrame, eq_ne : str = 'eq') -> pd.DataFrame:
    """Compares 2 dataframes with different columns using the mapping to link them together
    

    Parameters
    ----------
    control : pd.DataFrame
        Control frame to be compared.
    test : pd.DataFrame
        Test frame to be compared.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from control to test.
    eq_ne : str (eq, ne), optional
        eq for equal comparison, ne for not equal comparison is the control or the test (default is 'eq').

    Raises
    ------
    ValueError
        WARNING: control columns is missing: <field name>
        WARNING: test columns is missing: <field name>

    Returns
    -------
    pd.DataFrame
        Results will be in a True/False format.

    """
 
    df = pd.DataFrame(index=control.index)


    for i, data in mapper[mapper['idx'] != 'Y'].iterrows():
        if data['control'] not in control.columns:
            raise ValueError('WARNING: control columns is missing: ' + data['control'])

        if data['test'] not in test.columns:
            raise ValueError('WARNING: test columns is missing: ' + data['test'])

        if eq_ne == 'eq':
            df_tmp = control[data['control']].eq(test[data['test']])
        else:
            df_tmp = control[data['control']].ne(test[data['test']])
        df_tmp.name = data['control']
        df = pd.concat([df, df_tmp], axis=1)

    return df



def return_diffs(control : pd.DataFrame, test : pd.DataFrame, result : pd.DataFrame, mapper : pd.DataFrame) -> pd.DataFrame:
    """Takes in a control and test dataframe, uses the results and mappers to return back a single dataframe with all actual differences
    

    Parameters
    ----------
    control : pd.DataFrame
        control frame uto be assigned an index.
    test : pd.DataFrame
        test frame to be assigned an index.
    result : pd.DataFrame
        True/False results of comparison check.
    mapper : pd.DataFrame
        Mapping which contains the columns mapped from control to test.

    Returns
    -------
    pd.DataFrame
        All matching results

    """

    cols = mapper[mapper['idx']!='Y'][['control','test']]
    test = test.rename(columns=cols.set_index('test')['control'])

    df = control[result == True].dropna(axis=0, how='all') # drops only when all are NaN
    df = df.append(test[result == True].dropna(axis=0, how='all'))
    
    return df.sort_index()



def quick_mapper_gen(control : pd.DataFrame, test : pd.DataFrame) -> pd.DataFrame:
    """
    Quickly generates a mapper dataframe, works best when both dataframes 
    columns are in the same order

    Parameters
    ----------
    control : pd.DataFrame
        The control dataframe
    test : pd.DataFrame
        The test dataframe

    Returns
    -------
    pd.DataFrame
        a quick mapper dataframe based on the 2 inputted dataframes

    """
    file = pd.DataFrame({'control':list(control.reset_index(drop=True).columns), 'test':list(test.reset_index(drop=True).columns)})

    
    if control.index.name is not None:
        nm = control.index.name.split(',')
    else:
        nm = ['']

    idx = file['control'].isin(nm).replace({True:'Y',False:''}).to_frame()
    idx.columns = ['idx']

    file = pd.concat([file,idx], axis=1)

    return file


# Dependent on a mapper config file
# must be in the format of:
# control,test,idx
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>
# <value>,<value>,<y or nothing>



# TEST 1


df = pd.DataFrame({'cost': [250, 150, 100],
                   'revenue': [100, 250, 300],
                   'letters':['A', 'B', 'C'],
                   'numbers':['1', '2', '3']})


df2 = pd.DataFrame({'cost.new': [250, 160, 100],
                   'revenue.new': [100, 250, 300],
                   'letters':['A', 'B', 'D'],
                   'numbers':['1', '2', '4']})


df_map = pd.read_csv('mapper_config.csv')

df_idx = set_index_mapper(df, df_map, col='control')
df2_idx = set_index_mapper(df2, df_map, col='test')

result = compare_df_cols(df_idx, df2_idx, df_map, 'ne')


findings = return_diffs(df_idx, df2_idx, result, df_map)



# TEST 2



# below will be a function to build starter mapper table
df = pd.read_csv('Ecommerce Purchases')
df2 = pd.read_csv('Ecommerce Purchases v2')


# from pandas_profiling import ProfileReport
# profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
# profile.to_file('test.html')

df_map = quick_mapper_gen(df, df2)

df_map.at[11,'idx'] = 'Y'


df_idx = set_index_mapper(df, df_map, col='control')
df2_idx = set_index_mapper(df2, df_map, col='test')

result = compare_df_cols(df_idx, df2_idx, df_map, 'ne')


findings = return_diffs(df_idx, df2_idx, result, df_map)






