import DataBaseModule
import pandas as pd

dataBase = DataBaseModule.DataBase() 

share_list = dataBase.get_share_list_form_local()

all_codes = share_list.code #所有股票的代码

#得到某一天的数据
def getShareDataByDate(code,date):
    share = dataBase.get_share_history_data(code)
    if type(share) == type(None):
        return None
    return share[share.date == date]

#得到某一天的平均和中值换手率
def getMidTurnoverByData(date):
    ans_list = ""
    for code in all_codes:
        slist = getShareDataByDate(code,date)
        if type(slist) == type(None):
            continue
        slist['code'] = code
        print(code)
        if type(ans_list) == type(""):
            ans_list = slist
        if not slist.empty:
            ans_list.append(slist.iloc[0])
    return ans_list
    
print(getMidTurnoverByData('2017-05-23'))
