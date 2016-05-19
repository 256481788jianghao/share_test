import tushare as ts
import os
import pandas as pd

class DataBase:
    def update_share_list(self):
        self._log("updata share list form internet")
        data = ts.get_stock_basics()
        data.to_csv("share_list.csv")

    def has_share_list_local(self);
        return os.path.exists("share_list.csv")

    def get_share_list(self):
        if not self.has_share_list_local():
            self.update_share_list()
        return pd.read_csv("share_list.csv")

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
    data = dataBase.get_share_list()
    print(data)
