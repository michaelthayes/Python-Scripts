
import pandas as pd
import numpy as np
import scipy.stats as stats


if __name__ == '__main__':

    
    # frequency distribution table

    df_ex2 = pd.read_csv('al_bundy.csv')
    df_ex2['Date'] = pd.to_datetime(df_ex2['Date'])
    df_ex2.head()
    df_ex2['Year'] = df_ex2['Date'].dt.year

    # use conditions to filter the data down    
    df_ex2 = df_ex2[(df_ex2['Country'] == 'United States') & (df_ex2['Gender'] == 'Male') & (df_ex2['Year']==2016)]
    
    # build cross table
    freq = pd.crosstab(index=df_ex2['Size (US)'], columns=df_ex2['Month'], margins='True')
    col_cnt = len(freq.columns) - 1 # remove 1 to account for All
    
    freq['All'] = freq['All']/col_cnt
    freq = freq.rename(columns={'All':'mean'})
    # stdev per row
    std = pd.DataFrame()
    std['stdev'] = np.std(freq.loc[:, freq.columns !='mean'], axis=1)
    std['stderr'] = stats.sem(freq.loc[:, freq.columns != 'mean'], axis=1)
    
    freq = pd.concat([freq, std], axis=1)
    
    # Sample
    # lookup student's t
    percent = .95
    alpha = (1-percent)/2
    t_value = stats.t.ppf(1-alpha, col_cnt-1)

    # stdev * student's t
    freq['mrgn_err'] = t_value * freq['stderr']
    
    freq['CI_min'] = freq['mean'] - freq['mrgn_err']
    freq['CI_max'] = freq['mean'] + freq['mrgn_err']
    
    
    
    