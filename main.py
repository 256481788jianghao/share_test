import DataBaseModule
import pandas as pd
import ToolModule as tm
import datetime

print('初始化开始')

dataBase = DataBaseModule.DataBase() 

#包括今天在内过去30个交易日的日期列表，不包括周六日
days30 = tm.getDateList(29)


all_share_list = dataBase.get_share_list_form_local()

#剔除未上市的新股,剔除交易时间小于1个月的股票
#limitDateNum = tm.dateToNum(days30[29])
#Filter = (all_share_list.timeToMarket != 0) & (all_share_list.timeToMarket <= limitDateNum)
Filter = (all_share_list.timeToMarket != 0)
share_list_in_market = all_share_list[Filter]

print('过滤个股结束')
all_codes = list(share_list_in_market.index) #所有股票的代码

all_hist_data = []#所用历史数据临时列表

for code in all_codes:
    share = dataBase.get_share_history_data(code)
    if not isinstance(share,pd.DataFrame):
        continue
    share['code'] = [code]*len(share)#增加股票代码
    share_name = share_list_in_market.loc[code,'name'][0]
    share['name'] = [share_name]*len(share)
    share['date'] = share.index
    all_hist_data.append(share)
    
g_all_data = pd.concat(all_hist_data,ignore_index=True) #所有历史数据Frame
                 
g_hs300_data = dataBase.get_hs300_data() #hs300历史数据

print('初始化结束')

#得到某股的上市时间和上市天数
def getToMarketDateAndDays(code):
    date_num = share_list_in_market[share_list_in_market.code == code].timeToMarket.iloc[0]
    date_str = tm.numToDate(date_num)
    dayObjNow = datetime.datetime.now()
    dayObjx   = datetime.datetime.strptime(date_str,'%Y-%m-%d')
    diff = dayObjNow - dayObjx
    return [date_str,diff.days]
    

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

#得到最近n天的数据，0表示今天
def getLastData(n):
    g_all_data[g_all_data.date.apply(tm.dateToNum) >= tm.dateToNum(days30[n])]

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

"""
#得到近几日的交易变化
def p_change_sum(x):
    p_change = x.p_change+100
    ans = 1
    for p in p_change:
        ans = ans * p
    return p

last5_data = g_all_data[g_all_data.date.apply(tm.dateToNum) > tm.dateToNum(days30[3])]
p_change_data = last5_data.groupby('code').apply(p_change_sum)
p_change_code = p_change_data[p_change_data > 105].index
ans_share_list = share_list_in_market.loc[[c in p_change_code for c in share_list_in_market.code]]
print(ans_share_list)
"""
