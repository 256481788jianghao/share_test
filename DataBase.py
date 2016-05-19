import tushare as ts
import os
import pandas as pd

class DataBase:
    def get_share_history_data(self,code):
        if not self.has_share_history_local_data(code):
            self.update_share_history_data(code)
        return pd.read_csv(code+'.csv')
 
    def has_share_history_local_data(self,code):
        return os.path.exists(code+'.csv')

    def update_share_history_data(self,code):
        self._log("update data from internet")
        data = ts.get_hist_data(code)
        data.to_csv(code+".csv")

    def _log(self,str):
        print("DataBase:"+str)

    def __init__(self):
        self._log("---init---")

if __name__ == "__main__":
    dataBase = DataBase()
    data = dataBase.get_share_history_data('600845')
    print(data)
