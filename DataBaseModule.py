import tushare as ts
import os
import pandas as pd
import time
import threading

class DataBase:

    updateAllShareHistoryDataSum = 0
    updateAllShareHistoryDataCount = 0
    indexNameMap = {'hs300':399300}
    store = None
    
    """===============================公有函数========================="""
    
    """
    获得沪深300成份股的列表，以权重降序排序
    """
    def get_hs300_sharelist(self):
        return self.store["hs300_share_list"]
        
  
    """
    更新所有的股票信息
    """
    def update_all_share_history_data(self):
        self.__log("update all share history data");
        self.__update_share_list_from_internet()
        data = self.get_share_list_form_local()
        #剔除所有未上市股票
        data = data[data.timeToMarket != 0]
        dataCodes = list(data.index)
        for key in self.indexNameMap:
            #print(self.indexNameMap[key])
            dataCodes.append(self.indexNameMap[key])
        #print(dataCodes)
        self.updateAllShareHistoryDataSum = len(dataCodes)
        #data1 = dataCodes[0:int(self.updateAllShareHistoryDataSum/2)]
        #data2 = dataCodes[int(self.updateAllShareHistoryDataSum/2):]
        #threading.Thread(target=self.__update_share_history_data_by_codes,args=([data1])).start()
        #threading.Thread(target=self.__update_share_history_data_by_codes,args=([data2])).start()
        self.__update_share_history_data_by_codes(dataCodes)
        
    """
    获取个股信息，如果有本地数据，先拿本地数据,如果没有本地数据，先更新，再拿本地数据
    """
    def get_share_history_data(self,code):
        try:
            data = self.store['share_'+code]
            if not isinstance(data,pd.DataFrame):
                return None
            else:
                return data
        except:
            return None
        
    """
    获取沪深300指数信息
    """
    def get_hs300_data(self):
        return self.get_share_history_data(self.indexNameMap['hs300'])

    """
    更新个股信息
    """
    def update_share_history_data(self,codestr):
        code = self.__formtInputCode(codestr)
        self.__log("update data from internet code="+code)
        data = ts.get_hist_data(code)
        if isinstance(data,pd.DataFrame) and not data.empty:
            self.store['share_'+code] = data
        else:
            self.store['share_'+code] = pd.DataFrame()
            self.__log("update data from internet code="+code+" but not get data")
            
    """
    得到股票名称，代码，等信息列表
    """        
    def get_share_list_form_local(self):
        return self.store['all_share_list']
            
    def update_all(self):
        self.__update_hs300_sharelist()
        self.update_all_share_history_data()
        self.store.close()
    """==================================私有函数============================"""
    
    def __update_hs300_sharelist(self):
        print("更新hs300数据")
        data = ts.get_hs300s()
        if not isinstance(data,pd.DataFrame):
            data = pd.DataFrame()
        self.store['hs300_share_list'] = data
        
    """
    获取codes列表指明的股票数据
    """
    def __update_share_history_data_by_codes(self,codes):
        for code in codes[0:5]:
            self.updateAllShareHistoryDataCount += 1
            self.update_share_history_data(code)
            self.__log("finish "+str(self.updateAllShareHistoryDataCount)+"/"+str(self.updateAllShareHistoryDataSum))


    def __update_share_list_from_internet(self):
        self.__log("updata share list form internet")
        data = ts.get_stock_basics()
        self.store['all_share_list'] = data
        
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
        self.store = pd.HDFStore("hdf_store.hd5")
        print(self.store)
    
    def __del__(self):
        self.__log("---del---")
        if self.store.is_open:
            self.__log("close store")
            self.store.close()

if __name__ == "__main__":
    dataBase = DataBase()
    #dataBase.update_all()
    #print(dataBase.get_hs300_sharelist())
    #dataBase._makeLocalShareDataPath(100)
    #dataBase.get_share_history_data(300512)
    #dataBase.update_all_share_history_data()
    #data = ts.get_hist_data('399300')
    #print(data)
    #print(dataBase.get_hs300_info())
