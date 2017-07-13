# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

def getData(code=None,startDate=None,endDate=None):
    data_list = []
    code_list = []
    turnover_rate_list = []
    if code is None:
        allCode = fd.all_share_codes
    else:
        allCode = code
    for code in allCode:
        data = fd.getHisDataByCode(code,startDate,endDate)
        if isinstance(data,pd.DataFrame) and not data.empty:
            data = data[data.turnover > 0]
            turnover_rate_list.extend(list(data.turnover/data.turnover.min()))
            code_list.extend([code]*len(data))
            data_list.append(data)
            #print('==================')
            #print(data)
    #print(len(data_list))    
    frame = pd.concat(data_list)#,ignore_index=True)
    frame['code'] = code_list
    frame['turnover_rate'] = turnover_rate_list
    return frame

#data = getData('300024','2017-07-04')
data = getData([300024,300021],'2017-07-04','2017-06-04')
print(data)