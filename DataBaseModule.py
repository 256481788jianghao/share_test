import tushare as ts
#import os
import pandas as pd
#import time
#import threading
import datetime as dtime

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
    def get_share_history_data(self,code,startDate=None,endDate=None):
        try:
            if startDate is None and endDate is None:
                data = self.store.select('share_'+str(code))
                if not isinstance(data,pd.DataFrame):
                    return None
                else:
                    return data
            else:
                topData = self.store.select('share_'+str(code),start=0,stop=1)
                if topData.empty:
                    return None
                topDateStr = topData.index[0]
                topDateObj = dtime.datetime.strptime(topDateStr,"%Y-%m-%d")
                startDateObj = dtime.datetime.strptime(startDate,"%Y-%m-%d")
                del_time = topDateObj - startDateObj
                if del_time.days <=0:
                    start = 0
                else:
                    start = int(del_time.days*0.5)
                if endDate is None:
                    stop = start+10
                else:
                    endDateObj = dtime.datetime.strptime(endDate,"%Y-%m-%d")
                    del_time2 = startDateObj - endDateObj
                    stop = int(del_time2.days+3)+start
                print(start)
                print(stop)
                data = self.store.select('share_'+str(code),start=start,stop=stop)
                if not isinstance(data,pd.DataFrame):
                    return None
                else:
                    #print(data)
                    if endDate is None:
                        return data.loc[startDate:startDate]
                    else:
                        return data.loc[startDate:endDate]
        except Exception as e:
            print(" get_share_history_data except code="+str(code)+" e="+str(e))
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
    
    def update_all_report_data(self):
        timeset = self.__get_Q_list()
        for time in timeset:
            self.__update_report_data(time[0],time[1])
            
    def update_all(self):
        self.__update_hs300_sharelist()
        self.update_all_share_history_data()
        self.store.close()
    """==================================私有函数============================"""
    def __date_to_q(self,date):
        tmp = date.split('-')
        q = 1
        if tmp[1] in ['01','02','03']:
            q = 1
        elif tmp[1] in ['04','05','06']:
            q = 2
        elif tmp[1] in ['07','08','09']:
            q = 3
        else:
            q = 4
        return (int(tmp[0]),q)
    
    def __get_Q_list(self):
        now = dtime.datetime.now()
        deltalist = [dtime.timedelta(days=-x*30) for x in range(36)]
        n_days = [ now + delta for delta in deltalist]
        time_list = [ x.strftime('%Y-%m') for x in n_days ]
        q_list = [self.__date_to_q(x) for x in time_list]
        return set(q_list)
        
    def __update_report_data(self,year,index):
        try:
            data1 = ts.get_report_data(year,index)
            data2 = ts.get_profit_data(year,index)
            data3 = ts.get_operation_data(year,index)
            data4 = ts.get_growth_data(year,index)
            data5 = ts.get_debtpaying_data(year,index)
            data6 = ts.get_cashflow_data(year,index)
            self.store['report_data_'+str(year)+'_'+str(index)] = data1
            self.store['profit_data_'+str(year)+'_'+str(index)] = data2
            self.store['operation_data_'+str(year)+'_'+str(index)] = data3
            self.store['growth_data_'+str(year)+'_'+str(index)] = data4
            self.store['debtpaying_data_'+str(year)+'_'+str(index)] = data5
            self.store['cashflow_data_'+str(year)+'_'+str(index)] = data6
        except:
            print("xxxx")
    
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
        for code in codes:
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
        self.__log('---init end---')
        #print(self.store)
    
    def __del__(self):
        self.__log("---del---")
        if self.store.is_open:
            self.__log("close store")
            self.store.close()

if __name__ == "__main__":
    dataBase = DataBase()
    #dataBase.update_all_report_data()
    dataBase.update_all()
    #print(dataBase.get_hs300_sharelist())
    #dataBase._makeLocalShareDataPath(100)
    #data = dataBase.get_share_history_data(300024,'2017-07-03','2017-06-03')
    #dataBase.update_all_share_history_data()
    #data = ts.get_hist_data('399300')
    #print(data)
    #print(dataBase.get_hs300_info())
