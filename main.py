import DataBaseModule
import pandas as pd
import ToolModule as tm
import datetime

import FilterDataModule as fd

print('初始化开始')

dataBase = DataBaseModule.DataBase() 

g_all_data = fd.all_data

g_hs300_data = dataBase.get_hs300_data() #hs300历史数据

print('初始化结束')

"""
#得到某股的上市时间和上市天数
def getToMarketDateAndDays(code):
    date_num = share_list_in_market[share_list_in_market.code == code].timeToMarket.iloc[0]
    date_str = tm.numToDate(date_num)
    dayObjNow = datetime.datetime.now()
    dayObjx   = datetime.datetime.strptime(date_str,'%Y-%m-%d')
    diff = dayObjNow - dayObjx
    return [date_str,diff.days]
"""

#得到某一天的数据
def getShareDataByDate(code,date):
    return g_all_data[(g_all_data.code == code) & (g_all_data.date == date)]

#得到某一天所用股票的历史数据，剔除当日没有数据的股票
def getAllSharesDataByDate(date):
    print("get all shares data of "+date)
    return g_all_data[g_all_data.date == date]
    
#得到某一天的平均和中值换手率以及有交易信息的股票数量
def getTurnover(all_shares):
    #all_shares = getAllSharesDataByDate(date)
    if not all_shares.empty:
        tmp = all_shares.sort_values(by='turnover')
        #print(tmp)
    else:
        return None
    num = len(tmp)
    mean_data = tmp.mean()
    #print(type(tmp.turnover))
    mid_turnover = tmp.turnover.iloc[int(num/2)]
    mean_turnover = mean_data.turnover
    return [mean_turnover,mid_turnover,num]

    
#得到最近N天价格变化超过p的股票
def getShareListNP(dataList,P):
    def p_change_sum(x):
        p_change = x.p_change+100
        ans = 1
        for p in p_change:
            ans = ans * p
        return p
    lastNData = g_all_data[[date in dataList for date in g_all_data.date]]
    p_change_data = lastNData.groupby('code').apply(p_change_sum)
    p_change_code = p_change_data[p_change_data > P].index
    ansData = lastNData[[code in p_change_code for code in lastNData.code]]
    print(ansData.groupby('code').mean()[['pe','turnover']])

getShareListNP(['2017-05-31','2017-05-26','2017-05-25'],105)



"""
#计算从今天到过去30个交易日内的，每天换手率的平均值和中位数
mid_turnover_list = []
mean_turnover_list = []
num_list = []
days_list = []
for day in days30:
    info = getTurnover(getAllSharesDataByDate(day))
    if info == None:
        continue
    days_list.append(day)
    mid_turnover_list.append(info[1])
    mean_turnover_list.append(info[0])
    num_list.append(info[2])
    
ans = pd.DataFrame({"day":days_list,'mean_turnover':mean_turnover_list,'mid_turnover':mid_turnover_list,'num':num_list})
print(ans)
"""
