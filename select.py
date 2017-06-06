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

p = []
t = []  
for code in fd.all_share_codes:
    data = getData(code,'2017-06-01','2017-05-26')
    p.append(p_change_sum(data.p_change))
    t.append(turnover_sum(data.turnover))

ans = pd.DataFrame({'p':p,'code':fd.all_share_codes,'t':t})
filter_ans = ans[(ans.p > 2) & (ans.p < 5)]
print(filter_ans.mean())
print(filter_ans.median())
print('============================================')
print(ans.mean())
print(ans.median())
print(filter_ans)
