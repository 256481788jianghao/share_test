# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

def turnover_sum(x):
    ans = 0
    for t in x.turnover:
        ans = ans + t
    return ans

def p_change_sum(x):
        p_change = x.p_change+100
        ans = 1
        for p in p_change:
            ans = ans * p
        return ans
    
def filterDate(data,startDate,endDate):
    return data[(data.date.apply(tm.dateToNum) >= startDate) & (data.date.apply(tm.dateToNum) <= endDate)]


print(fd.all_share_list)
