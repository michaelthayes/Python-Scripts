# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 20:03:20 2021

@author: hayes
"""

import pandas as pd
import numpy as np
from scipy import stats


if __name__ == '__main__':

    
    # frequency distribution table

    df_ex = pd.read_csv('weightloss.csv')

    df_ex['Difference'] = df_ex['After (lbs)'] - df_ex['Before (lbs)']
    
    
    sample_mean = df_ex['Difference'].mean()
    std = np.std(df_ex['Difference'])
    stderr = stats.sem(df_ex['Difference'])
    
    # gets T value
    T = sample_mean / stderr
    
    # gets statistic & pvalue
    stats.ttest_1samp(df_ex['Difference'], abs(sample_mean))
    
    