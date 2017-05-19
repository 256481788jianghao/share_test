import tushare as ts
import os
import pandas as pd
import time
import threading

class DataBase:

    updateAllShareHistoryDataSum = 0
    updateAllShareHistoryDataCount = 0
    indexNameMap = {'hs300':399300}
    
    """
    获得沪深300成份股的列表，以权重降序排序
    """
    def get_hs300_info(self):
        data = ts.get_hs300s()
        if isinstance(data,pd.DataFrame):
            return data.sort_values(by='weight',ascending=False)
        else:
            return None
        
    """
    获取codes列表指明的股票数据
    """
    def __update_share_history_data_by_codes(self,codes):
        for code in codes:
            self.updateAllShareHistoryDataCount += 1
            self.update_share_history_data(code)
            self.__log("finish "+str(self.updateAllShareHistoryDataCount)+"/"+str(self.updateAllShareHistoryDataSum))

    """
    更新所有的股票信息
    """
    def update_all_share_history_data(self):
        self.__log("update all share history data");
        self.__get_share_list_from_internet()
        data = self.__get_share_list()
        dataCodes = data.code
        for key in self.indexNameMap:
            #print(self.indexNameMap[key])
            dataCodes[len(dataCodes)] = self.indexNameMap[key]
        #print(dataCodes)
        self.updateAllShareHistoryDataSum = len(dataCodes)
        data1 = dataCodes[0:int(self.updateAllShareHistoryDataSum/2)]
        data2 = dataCodes[int(self.updateAllShareHistoryDataSum/2):]
        threading.Thread(target=self.__update_share_history_data_by_codes,args=([data1])).start()
        threading.Thread(target=self.__update_share_history_data_by_codes,args=([data2])).start()
        #self.update_share_history_data_by_codes(dataCodes)

    def __get_share_list_from_internet(self):
        self.__log("updata share list form internet")
        data = ts.get_stock_basics()
        data.to_csv("share_list.csv",encoding='utf-8')

    def __has_share_list_local(self):
        return os.path.exists("share_list.csv")

    def __get_share_list(self):
        if self.__has_share_list_local():
            return pd.read_csv("share_list.csv")
        else:
            self.__log("can not find share_list.csv")
            return None

    """
    获取个股信息，如果有本地数据，先拿本地数据,如果没有本地数据，先更新，再拿本地数据
    """
    def get_share_history_data(self,code):
        if not self.__has_share_history_local_data(code):
            self.update_share_history_data(code)
        if self.__has_share_history_local_data(code):
            return pd.read_csv(self.__makeLocalShareDataPath(code))
        else:
            return None
 
    def __has_share_history_local_data(self,codestr):
        code = self.__formtInputCode(codestr)
        return os.path.exists(self.__makeLocalShareDataPath(code))

    """
    更新个股信息
    """
    def update_share_history_data(self,codestr):
        code = self.__formtInputCode(codestr)
        self.__log("update data from internet code="+code)
        data = ts.get_hist_data(code)
        if isinstance(data,pd.DataFrame):
            data.to_csv(self.__makeLocalShareDataPath(code),encoding='utf-8')
        else:
            self.__log("update data from internet code="+code+" but not get data")

    def __isInIndexNameMap(self,name):
        if name in indexNameMap.keys:
            return True
        return False

    def __getIndexCode(self,name):
        return indexNameMap[name]

    def __makeLocalShareDataPath(self,code):
        timestr = ''#time.strftime('%Y-%m-%d', time.localtime())
        codestr = self.__formtInputCode(code)
        if not os.path.exists("./localShareData/"):
            os.mkdir("./localShareData/")
        return "./localShareData/"+codestr+"_"+timestr+".csv"
        
    def __formtInputCode(self,code):
        codestr = str(code)
        dlen = 6-len(codestr)
        while(dlen > 0):
            codestr = '0'+codestr
            dlen -= 1
        return codestr
            
    
    def __log(self,str):
        print("DataBase:"+str)

    def __init__(self):
        self.__log("---init---")

if __name__ == "__main__":
    dataBase = DataBase()
    #dataBase._makeLocalShareDataPath(100)
    #dataBase.get_share_history_data(300512)
    dataBase.update_all_share_history_data()
    #data = ts.get_hist_data('399300')
    #print(data)
    #print(dataBase.get_hs300_info())
