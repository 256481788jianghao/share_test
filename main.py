import DataBaseModule
import pandas as pd

print('初始化开始')

dataBase = DataBaseModule.DataBase() 

share_list = dataBase.get_share_list_form_local()

all_codes = share_list.code #所有股票的代码

all_hist_data = {}#所用历史数据

for code in all_codes:
    share = dataBase.get_share_history_data(code)
    all_hist_data[code] = share

print('初始化结束')

#得到某一天的数据
def getShareDataByDate(code,date):
    share = all_hist_data[code]
    if type(share) == type(None):
        return None
    tmp = share[share.date == date]
    if not tmp.empty:
        return tmp
    else:
        return None

#得到某一天所用股票的历史数据，剔除当日没有数据的股票
def getAllSharesDataByDate(date):
    ansFrame = pd.DataFrame()
    code_list =[]
    for code in all_codes:
        share = getShareDataByDate(code,date)
        if type(share) == type(None):
            continue
        code_list.append(code)
        ansFrame = pd.concat([ansFrame,share],ignore_index=True)
        ansFrame['code'] = code_list
    return ansFrame
    
#得到某一天的平均和中值换手率
def getMidTurnoverByData(date):
    all_shares = getAllSharesDataByDate(date).sort_values(by='turnover')
    num = len(all_shares)
    mean_data = all_shares.mean()
    mid_turnover = all_shares.turnover[int(num/2)]
    mean_turnover = mean_data.turnover
    part_shares = all_shares[all_shares.turnover >= mean_turnover]
    print(part_shares)
    return [mean_turnover,mid_turnover]
    
    
print(getMidTurnoverByData('2017-05-15'))
