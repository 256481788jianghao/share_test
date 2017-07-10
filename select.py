# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

def getData(code,startDate=None,endDate=None):
    if startDate is None and endDate is None:
        return fd.getHisDataByCode(code)
    elif startDate is not None and endDate is None:
        return fd.getHisDataByCode(code)[startDate:startDate]
    else:
        return fd.getHisDataByCode(code)[startDate:endDate]

def getAllData(startDate,endDate=None):
    data_list = []
    for code in fd.all_share_codes:
        data = getData(code,startDate,endDate)
        #print(type(data))
        if isinstance(data,pd.DataFrame) and not data.empty:
            data_list.append(data)
            #print('==================')
            #print(data)
    #print(len(data_list))    
    frame = pd.concat(data_list,ignore_index=True)
    return frame

frame = getAllData('2017-07-04')
print('==========================')
print(frame.sort_values(by='turnover').code)