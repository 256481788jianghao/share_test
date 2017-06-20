# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:09:53 2017

@author: Administrator
"""

#import FilterDataModule as fd
import pandas as pd
import tushare as ts

dateDict = {2017:[1],2016:[1,2,3,4]}

g_store = pd.HDFStore("hdf_store.hd5")

for key in dateDict:
    for index in dateDict[key]:
        name = 'report_'+str(key)+'_'+str(index)
        print('start get '+name)
        report = ts.get_report_data(key,index)
        if isinstance(report,pd.DataFrame):
            g_store[name] = report
        else:
            print('report is not a dataframe')

if g_store.is_open:
    g_store.close()