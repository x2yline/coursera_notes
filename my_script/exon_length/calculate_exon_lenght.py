# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
file = r'E:\r\biotrainee_demo1\CCDS.current.txt'


def calculate_exon(file):
  data = pd.read_csv(file, sep='\t',\
    usecols=[0,9])

#data.loc[1:10,:]
#  data[0:3]
#  data.iloc[1:3]
#  data.iloc[3]
  all_length = 0

  for i in data.iloc[:,0].unique():
    # get the data of chrosome i
    # iloc[row_vector,col_vect]
    # iloc[row_vector]
    data_i = data.loc[data.iloc[:,0] == i]
    type(data_i)
    type(data_i.iloc[:,1])
    # remove the '[]' in column2
    data_j = data_i.iloc[:,1].apply(lambda x: x[1:-1])
    data_p = data_j.apply(lambda x: x.split(', '))
    data_g = data_p.apply(lambda x: pd.Series(x))
    # 把nan填充为 0-0
    data_f = np.array(data_g.fillna('0-0'))
    # 去除重复的外显子
    data_f = np.unique(data_f.reshape((data_f.shape[0]*data_f.shape[1], 1)))
    data_f = pd.DataFrame(data_f)
    data_m = data_f.apply(lambda x: \
      x.apply(lambda y: (y.split('-')[0])))
    data_n = data_f.apply(lambda x: \
      x.apply(lambda y: (y.split('-')[-1])))
    # pd.to_numeric can only apply to a 1-d array
    data_mi = data_m.apply(lambda x: pd.to_numeric(x, downcast='float'))
    data_ni = data_n.apply(lambda x: pd.to_numeric(x, downcast='float'))
    all_length += (data_ni - data_mi).sum().sum()
  return(all_length)

length = calculate_exon(file)
print(length)
