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

        
share_list_code = share_list.code
for code in share_list_code:
    
    
