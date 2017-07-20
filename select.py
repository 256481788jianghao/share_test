# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd
import statsmodels.api as sm

def getData(code=None,startDate=None,endDate=None,ft=None):
    data_list = []
    code_list = []
    turnover_rate_list = []
    #volume_rate_list = []
    close_rate_list = []
    if code is None:
        allCode = fd.all_share_codes
    else:
        allCode = code
    #allCode = [x for x in allCode if (int(x) > 300999 or int(x) < 300000)]
    #print(len(allCode))
    for code in allCode:
        data = fd.getHisDataByCode(code,startDate,endDate)
        if isinstance(data,pd.DataFrame) and not data.empty and (ft is None or ft(data)):
            data = data[(data.turnover > 0) & (data.close > 0)]
            turnover_rate_list.extend(list(data.turnover/data.turnover.min()))
            #volume_rate_list.extend(list(data.volume/data.volume.min()))
            close_rate_list.extend(list(data.close/data.close.min()))
            code_list.extend([code]*len(data))
            data_list.append(data)
            #print('==================')
            #print(data)
        else:
            pass
            #print("code="+str(code)+" is not good")
    #print(len(data_list))    
    frame = pd.concat(data_list)#,ignore_index=True)
    frame.loc[:,'code'] = code_list
    frame.loc[:,'turnover_rate'] = turnover_rate_list
    #frame.loc[:,'volume_rate'] = volume_rate_list
    frame.loc[:,'close_rate'] = close_rate_list
    return frame

def DetectData(factor,startDate,endDate,baseNth = 1):
    infoData = fd.all_share_list
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
    data1th = data1th.loc[(data1th.p_change > 7) & (data1th.p_change < 10)]
    data = data0Group[data0Group.index.isin(data1th.index)]
    infoDataSub = infoData[infoData.index.isin(data.index)]
    print(data)
    #print(pd.concat([data,infoDataSub],axis=1,join='inner'))
    
def DetectData2(factor,startDate,endDate,baseNth = 1):
    infoData = fd.all_share_list
    infoData = infoData[(infoData.code_int > 300999) | (infoData.code_int < 300000) ]
    allData = getData(infoData.index,startDate,endDate)
    allDataGroup = allData.groupby('code')
    def getOLSCoef(data):
        datalen = len(data)
        X = [x-1 for x in range(datalen,0,-1)]
        X = sm.add_constant(X)
        res = sm.OLS(data,X).fit()
        if len(res.params) == 2:
            return res.params.x1
        else:
            return 0
    def app(item):
        return  getOLSCoef(item.turnover_rate)
    data0Group = allDataGroup.apply(app)
    print(data0Group[data0Group > 0])
    
DetectData2(1,'2017-07-19','2017-06-15')
    
"""
def buyProcess(curPrice,myPrice,myVolume,priceDownRate=0.9,priceTargetRate=1.05):
    if curPrice <= priceDownRate*myPrice:
        buyVolume = (1-priceDownRate*priceTargetRate)/priceDownRate/(priceTargetRate-1)*myVolume
        buyVolume = int(buyVolume/100+1)*100
        myPrice = (myPrice*myVolume+curPrice*buyVolume)/(myVolume+buyVolume)
        myVolume = myVolume+buyVolume
    return myPrice,myVolume
    
def test():
    priceDownRate=0.9
    priceTargetRate=0.5*(1-priceDownRate)/priceDownRate+1
    myPrice = 20
    myVolume = 100
    allData = [0.01*x for x in range(myPrice*100,100*10,-1)]
    for price in allData:
        #print(price)
        myPriceCur,myVolumeCur = buyProcess(price,myPrice,myVolume,priceDownRate,priceTargetRate)
        if myPriceCur != myPrice:
            myPrice = myPriceCur
            myVolume = myVolumeCur
            print(myPrice)
            print(myVolume)
            print(myPrice*myVolume)
            print("=====")
"""   
