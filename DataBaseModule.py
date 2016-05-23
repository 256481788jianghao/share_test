import tushare as ts
import os
import pandas as pd
import time
import threading

class DataBase:

    updateAllShareHistoryDataSum = 0
    updateAllShareHistoryDataCount = 0

    def update_share_history_data_by_codes(self,codes):
        for code in codes:
            self.updateAllShareHistoryDataCount += 1
            self.update_share_history_data(code)
            self._log("finish "+str(self.updateAllShareHistoryDataCount)+"/"+str(self.updateAllShareHistoryDataSum))

    def update_all_share_history_data(self):
        self._log("update all share history data");
        self.update_share_list()
        data = self.get_share_list()
        dataCodes = data.code
        self.updateAllShareHistoryDataSum = len(dataCodes)
        data1 = dataCodes[0:int(self.updateAllShareHistoryDataSum/2)]
        data2 = dataCodes[int(self.updateAllShareHistoryDataSum/2):]
        threading.Thread(target=self.update_share_history_data_by_codes,args=([data1])).start()
        threading.Thread(target=self.update_share_history_data_by_codes,args=([data2])).start()
        #self.update_share_history_data_by_codes(dataCodes)

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
        if self.has_share_history_local_data(code):
            return pd.read_csv(self._makeLocalShareDataPath(code))
        else:
            return None
 
    def has_share_history_local_data(self,codestr):
        code = self._formtInputCode(codestr)
        return os.path.exists(self._makeLocalShareDataPath(code))

    def update_share_history_data(self,codestr):
        code = self._formtInputCode(codestr)
        self._log("update data from internet code="+code)
        data = ts.get_hist_data(code)
        if isinstance(data,pd.DataFrame):
            data.to_csv(self._makeLocalShareDataPath(code),encoding='utf-8')
        else:
            self._log("update data from internet code="+code+" but not get data")

    def _makeLocalShareDataPath(self,code):
        timestr = ''#time.strftime('%Y-%m-%d', time.localtime())
        codestr = self._formtInputCode(code)
        if not os.path.exists("./localShareData/"):
            os.mkdir("./localShareData/")
        return "./localShareData/"+codestr+"_"+timestr+".csv"
        
    def _formtInputCode(self,code):
        codestr = str(code)
        dlen = 6-len(codestr)
        while(dlen > 0):
            codestr = '0'+codestr
            dlen -= 1
        return codestr
            
    
    def _log(self,str):
        print("DataBase:"+str)

    def __init__(self):
        self._log("---init---")

if __name__ == "__main__":
    dataBase = DataBase()
    #dataBase._makeLocalShareDataPath(100)
    #dataBase.get_share_history_data(300512)
    dataBase.update_all_share_history_data()
    #data = dataBase.get_share_list()
    #print(data)
