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
    
def turnover_sum(x):
    ans = 0
    for t in x:
        ans = ans + t
    return ans

def p_change_sum(x):
        ans = 1
        for p in x:
            ans = ans * ((p+100)/100)
        return (ans-1)*100

def getDataFrom(date1,date2):
    p = []
    t = [] 
    for code in fd.all_share_codes:
        data = getData(code,date1,date2)
        p.append(p_change_sum(data.p_change))
        t.append(turnover_sum(data.turnover))
    ans = pd.DataFrame({'p':p,'code':fd.all_share_codes,'t':t,'d':fd.all_share_list.daysToMarket,'n':fd.all_share_list.name})
    return ans

data1 = getDataFrom('2017-06-09','2017-06-07')
data2 = getDataFrom('2017-06-06','2017-05-01')

data2_up = data2[data2.p > 0]
data2_down = data2[data2.p <= 0]
data1_up = data1[data1.p > 5]

data2_up_codes = set(list(data2_up.index))
data2_down_codes = set(list(data2_down.index))
data1_up_codes = set(list(data1_up.index))

data2_up_len = len(data2_up_codes)
data2_down_len = len(data2_down_codes)

print(len(data1_up_codes))
print(len(data2_up_codes & data1_up_codes)/len(data2_down_codes & data1_up_codes))
#print(len(data2_down_codes & data1_up_codes)/data2_down_len)