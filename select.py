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
    volume_rate_list = []
    if code is None:
        allCode = fd.all_share_codes
    else:
        allCode = code
    #allCode = [x for x in allCode if (int(x) > 300999 or int(x) < 300000)]
    #print(len(allCode))
    for code in allCode:
        data = fd.getHisDataByCode(code,startDate,endDate)
        if isinstance(data,pd.DataFrame) and not data.empty and (ft is None or ft(data)):
            data = data[(data.turnover > 0) & (data.volume > 0)]
            turnover_rate_list.extend(list(data.turnover/data.turnover.min()))
            volume_rate_list.extend(list(data.volume/data.volume.min()))
            code_list.extend([code]*len(data))
            data_list.append(data)
            #print('==================')
            #print(data)
    #print(len(data_list))    
    frame = pd.concat(data_list)#,ignore_index=True)
    frame.loc[:,'code'] = code_list
    frame.loc[:,'turnover_rate'] = turnover_rate_list
    frame.loc[:,'volume_rate'] = volume_rate_list
    return frame

"""
factor 大势因子，要根据宏观环境给出一个估计（0,1],0表示整个市场不具有任何投资机会，
       1表示随机投资就可以赚钱
startDate ，endDate 基于那段区间的历史数据做出的判断
"""
def DetectData(factor,startDate,endDate,baseNth = 1):
    infoData = fd.all_share_list
    #排除创业板
    infoData = infoData[(infoData.code_int > 300999) | (infoData.code_int < 300000) ]
    allData = getData(infoData.index,startDate,endDate)
    allDataGroup = allData.groupby('code')
    def getMaxMin(item):
        pChangeMax = None
        pChangeMin = None
        pChangeMean = None
        turnoverRateMean = None
        volumeRateMean = None
        pChangeArray = item.p_change
        turnoverRateArray = item.turnover_rate
        volumeRateArray = item.volume_rate
        if len(pChangeArray) >= baseNth+1+5:
            pChangeSub = pChangeArray.iloc[0:baseNth]
            turnoverRateSub = turnoverRateArray[baseNth:(baseNth+5)]
            volumeRateSub = volumeRateArray[baseNth:(baseNth+5)]
            pChangeMax = pChangeSub.max()
            pChangeMin = pChangeSub.min()
            pChangeMean = pChangeSub.mean()
            turnoverRateMean = turnoverRateSub.mean()
            volumeRateMean = volumeRateSub.mean()
        return pd.Series({"volume_Rate_mean":volumeRateMean,"turnoverRate_mean":turnoverRateMean,"p_change_max":pChangeMax,'p_change_min':pChangeMin,'p_change_mean':pChangeMean})
    data0Group = allDataGroup.apply(getMaxMin)
    data1th = allDataGroup.nth(baseNth)
    data1th = data1th.loc[(data1th.p_change > 5) & (data1th.p_change < 10)]
    data = data0Group[data0Group.index.isin(data1th.index)]
    infoDataSub = infoData[infoData.index.isin(data.index)]
    print(data)
    #print(pd.concat([data,infoDataSub],axis=1,join='inner'))
    
DetectData(1,'2017-07-05','2017-06-01',baseNth = 5)