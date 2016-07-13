import DataBaseModule
import pandas as pd

dataBase = DataBaseModule.DataBase() 

share_list = dataBase.get_share_list()

def computeAttention(code, length):
    data = dataBase.get_share_history_data(code)
    if not isinstance(data,pd.DataFrame):
        return [0,0]
        
    data_len = len(data)
    if data_len <= length:
        return [0,0]
    else:
        ans = [0,0]
        highValue = data.high*data.volume*100
        lowValue = data.low*data.volume*100
        ans[0] = sum(highValue[0:length])
        ans[1] = sum(lowValue[0:length])
        return ans

def getAttentionList(codelist,length):
    dicttmp = {'highSum':[],'lowSum':[]}
    for code in codelist:
        ans = computeAttention(code,length)
        dicttmp['highSum'].append(ans[0])
        dicttmp['lowSum'].append(ans[1])
    return pd.DataFrame(dicttmp)

tmp = getAttentionList(share_list.code,30)

share_list['highSum'] = tmp.highSum
share_list['lowSum'] = tmp.lowSum

sortedList = share_list.sort_values(by='lowSum',ascending=False)[0:20]

print(sortedList[['name','industry']])


