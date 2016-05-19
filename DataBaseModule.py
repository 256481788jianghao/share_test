import tushare as ts
import os
import pandas as pd

class DataBase:
    def update_all_share_history_data(self):
        self._log("update all share history data");
        self.update_share_list()
        data = self.get_share_list()
        dataCodes = data.code
        sumCount = len(dataCodes)
        count = 0
        for code in dataCodes:
            count += 1
            self.update_share_history_data(code)
            self._log("finish "+str(count)+"/"+str(sumCount))

    def update_share_list(self):
        self._log("updata share list form internet")
        data = ts.get_stock_basics()
        data.to_csv("share_list.csv",encoding='utf-8')

    def has_share_list_local(self):
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

    def update_share_history_data(self,codestr):
        code = self._formtInputCode(codestr)
        self._log("update data from internet code="+code)
        data = ts.get_hist_data(code)
        data.to_csv(code+".csv",encoding='utf-8')
        
    def _formtInputCode(self,code):
        codestr = str(code)
        dlen = 6-len(codestr)
        while(dlen > 0):
            codestr = '0'+codestr;
            dlen -= 1
        return codestr
            
    
    def _log(self,str):
        print("DataBase:"+str)

    def __init__(self):
        self._log("---init---")

if __name__ == "__main__":
    dataBase = DataBase()
    dataBase.update_all_share_history_data()
    #data = dataBase.get_share_list()
    #print(data)
