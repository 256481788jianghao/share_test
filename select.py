# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

g_all_data = fd.all_data


def p_change_sum(x):
        p_change = x.p_change+100
        ans = 1
        for p in p_change:
            ans = ans * p
        return p
    
def filterDate(date):
    dateNum = tm.dateToNum(date)
    return dateNum >= startDate and dateNum <= endDate

startDate = 20170526
endDate = 20170601
p_change_min = 102

data1 = g_all_data[g_all_data.npr > 0 ]#净利润
data2 = data1[data1.date.apply(filterDate)]
data3 = data2.groupby('code').apply(p_change_sum)
data4 = data3[data3 > p_change_min]

codes = data4.index
print(codes)
