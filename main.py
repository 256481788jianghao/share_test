import DataBaseModule
import pandas as pd
import ToolModule as tm

print('初始化开始')

dataBase = DataBaseModule.DataBase() 

share_list = dataBase.get_share_list_form_local()

all_codes = share_list.code #所有股票的代码

all_hist_data = {}#所用历史数据

for code in all_codes:
    share = dataBase.get_share_history_data(code)
    all_hist_data[code] = share
                 
hs300_hist_data = dataBase.get_hs300_data() #hs300历史数据


#包括今天在内过去30个交易日的日期列表，不包括周六日
days30 = tm.getDateList(29)

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
    print("get all shares data of "+date)
    ansFrame = pd.DataFrame()
    code_list = []
    share_list = []
    for code in all_codes:
        share = getShareDataByDate(code,date)
        if type(share) == type(None):
            continue
        code_list.append(code)
        share_list.append(share)
        #ansFrame = pd.concat([ansFrame,share],ignore_index=True)
    if len(share_list) > 0 :
        ansFrame = pd.concat(share_list,ignore_index=True)
        ansFrame['code'] = code_list
    print("get all shares data of "+date+" end")
    return ansFrame
    
#得到某一天的平均和中值换手率以及有交易信息的股票数量
def getTurnover(all_shares):
    #all_shares = getAllSharesDataByDate(date)
    if not all_shares.empty:
        all_shares.sort_values(by='turnover')
    else:
        return None
    num = len(all_shares)
    mean_data = all_shares.mean()
    mid_turnover = all_shares.turnover[int(num/2)]
    mean_turnover = mean_data.turnover
    #part_shares = all_shares[all_shares.turnover >= mean_turnover]
    #print(part_shares)
    return [mean_turnover,mid_turnover,num]
    

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
