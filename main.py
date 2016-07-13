import DataBaseModule
import pandas as pd

dataBase = DataBaseModule.DataBase() 

share_list = dataBase.get_share_list()

def computeAttention(code, length, begin=0):
    data = dataBase.get_share_history_data(code)
    if not isinstance(data,pd.DataFrame):
        return [0,0]
        
    data_len = len(data)
    if data_len <= length+begin:
        return [0,0]
    else:
        ans = [0,0]
        highValue = data.high*data.volume*100
        lowValue = data.low*data.volume*100
        ans[0] = sum(highValue[begin:length])
        ans[1] = sum(lowValue[begin:length])
        return ans

def getAttentionList(codelist,length,begin=0):
    dicttmp = {'highSum':[],'lowSum':[]}
    for code in codelist:
        ans = computeAttention(code,length,begin)
        dicttmp['highSum'].append(ans[0])
        dicttmp['lowSum'].append(ans[1])
    return pd.DataFrame(dicttmp)

tmp = getAttentionList(share_list.code,30,5)

share_list['highSum'] = tmp.highSum
share_list['lowSum'] = tmp.lowSum
share_list['meanSum'] = (tmp.lowSum+tmp.highSum)*0.5

sortedList = share_list.sort_values(by='meanSum',ascending=False)[0:20]

print(sortedList[['name','industry']])


