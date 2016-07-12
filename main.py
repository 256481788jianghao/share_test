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
        for i in range(0,length):
            ans[0] += data.high[i]*data.volume[i]*100
            ans[1] += data.low[i]*data.volume[i]*100
        return ans

        
dataAttention = []
share_list_code = share_list.code
share_list_len = len(share_list)
for code in share_list_code:
    #print(code)
    if len(dataAttention) == 0:
        datatmp = computeAttention(code,30)
        datatmp.append(code)
        dataAttention.append(datatmp)
        #print(dataAttention)
    else:
        index = 0
        datalen = len(dataAttention)
        datatmp = computeAttention(code,30)
        datatmp.append(code)
        #print(datatmp)
        for i in range(0,datalen):
            if datatmp[1] > dataAttention[i][1]:
                dataAttention.insert(i,datatmp)
                break

print(dataAttention)
    

    
