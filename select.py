# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

def getData(code=None,startDate=None,endDate=None,ft=None):
    data_list = []
    code_list = []
    turnover_rate_list = []
    if code is None:
        allCode = fd.all_share_codes
    else:
        allCode = code
    #allCode = [x for x in allCode if (int(x) > 300999 or int(x) < 300000)]
    #print(len(allCode))
    for code in allCode:
        data = fd.getHisDataByCode(code,startDate,endDate)
        if isinstance(data,pd.DataFrame) and not data.empty and (ft is None or ft(data)):
            data = data[data.turnover > 0]
            turnover_rate_list.extend(list(data.turnover/data.turnover.min()))
            code_list.extend([code]*len(data))
            data_list.append(data)
            #print('==================')
            #print(data)
    #print(len(data_list))    
    frame = pd.concat(data_list)#,ignore_index=True)
    frame.loc[:,'code'] = code_list
    frame.loc[:,'turnover_rate'] = turnover_rate_list
    return frame

#data = getData('300024','2017-07-04')
def FT(data):
    if len(data) == 3:
        return True
    else:
        return False
data = getData(None,'2017-07-05','2017-07-03',ft=FT)
data2 = data.groupby('code').apply(lambda x:x.p_change)

k1 = data2[(data2['2017-07-04'] > 0) & (data2['2017-07-03']>8)]
k2 = data2[data2['2017-07-03']>8]

print(len(k1)/len(k2))