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

"""
factor 大势因子，要根据宏观环境给出一个估计（0,1],0表示整个市场不具有任何投资机会，
       1表示随机投资就可以赚钱
startDate ，endDate 基于那段区间的历史数据做出的判断
"""
def selectData(factor,startDate,endDate):
    infoData = fd.all_share_list
    infoData = infoData[(infoData.code_int > 300999) | (infoData.code_int < 300000) ]
    print(infoData)
    pass
    
selectData(1,'2017-07-05','2017-06-01')