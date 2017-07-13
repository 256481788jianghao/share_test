# -*- coding: utf-8 -*-
import DataBaseModule
import pandas as pd
import ToolModule as tm
import datetime
import gc
"""
date：日期
open：开盘价
high：最高价
close：收盘价
low：最低价
volume：成交量
price_change：价格变动
p_change：涨跌幅
ma5：5日均价
ma10：10日均价
ma20:20日均价
v_ma5:5日均量
v_ma10:10日均量
v_ma20:20日均量
turnover:换手率[注：指数无此项]
code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益(%)
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数
dateToMarket 上市时间字符串
daysToMarket 截止到目前的上市时间
"""

print('---filter data start---')
startM0 = tm.getNow()
def printTime(n):
    global startM0
    print(str(n)+':'+str(tm.getNow()-startM0))
    startM0 = tm.getNow()
    
#原始数据库
dataBase = DataBaseModule.DataBase()

printTime(1)
#股票代码，市盈率等信息列表
all_share_list = dataBase.get_share_list_form_local()
all_share_list = all_share_list[all_share_list.timeToMarket != 0]
all_share_list['dateToMarket'] = all_share_list.timeToMarket.apply(tm.numToDate)

def __daysToMarket(date):
    if type(date) != type('str') or len(date) < 10:
        return -1
    dateToM = datetime.datetime.strptime(date,'%Y-%m-%d')
    delta = datetime.datetime.now() - dateToM
    return delta.days
all_share_list['daysToMarket'] = all_share_list.dateToMarket.apply(__daysToMarket)

all_share_list['esp'] = all_share_list['esp'].apply(tm.strToFloat) 

printTime(2)
#所有股票代码
all_share_codes = list(all_share_list.index)
all_share_list['code'] = all_share_codes
          
printTime(3)
def getHisDataByCode(code,startDate=None,endDate=None):
    tmp = dataBase.get_share_history_data(str(code),startDate,endDate)
    if not (isinstance(tmp,pd.DataFrame) and not tmp.empty):
        return None
    return tmp
"""
tmp_list = []
for code in all_share_codes:
    tmp = dataBase.get_share_history_data(code)
    if not isinstance(tmp,pd.DataFrame):
        continue
    tmp['date'] = tmp.index
    tmp['code'] = code
    tmp = pd.merge(tmp,all_share_list.loc[[code]],on='code')
    #tmp['dateToMarket'] = tmp.timeToMarket.apply(tm.numToDate)
    tmp_list.append(tmp)
"""
printTime(4)

"""
#将所用的零散信息整理到一张表上
all_data = pd.concat(tmp_list,ignore_index= True)
"""
#all_data_json = all_data.to_json()

#all_data_json_len = len(all_data_json)

#del all_data
#gc.collect()


printTime(5)

print('---filter data end---')
 

"""
if __name__ == '__main__':
    from socket import *
    #from time import ctime
    from time import localtime
    import time
    
    HOST=''
    PORT=1122  #设置侦听端口
    BUFSIZE=1024*10
    ADDR=(HOST, PORT)
    sock=socket(AF_INET, SOCK_STREAM)
    
    sock.bind(ADDR)
    
    sock.listen(5)
    #设置退出条件
    STOP_CHAT=False
    
    data_send_count = 0
    
    while not STOP_CHAT:
        print('等待接入，侦听端口:%d' % (PORT))
        tcpClientSock, addr=sock.accept()
        print('接受连接，客户端地址：',addr)
        while True:
            try:
                data=tcpClientSock.recv(BUFSIZE)
            except:
                #print(e)
                tcpClientSock.close()
                break
            if not data:
                break
            #python3使用bytes，所以要进行编码
            #s='%s发送给我的信息是:[%s] %s' %(addr[0],ctime(), data.decode('utf8'))
            #对日期进行一下格式化
            ISOTIMEFORMAT='%Y-%m-%d %X'
            stime=time.strftime(ISOTIMEFORMAT, localtime())
            #s='[Server] %s发送给我的请求是:%s' %(addr[0],data.decode('utf8'))
            #tcpClientSock.send(s.encode('utf8'))
            print([stime], ':', data.decode('utf8'))
            
            CMD = data.decode('utf8').upper()
            if CMD == 'QUIT':
                STOP_CHAT = True
                break
            elif CMD == 'DATA_LEN':
                data_send_count = 0
                s = 'DATA_LEN:'+str(all_data_json_len)
                tcpClientSock.send(s.encode('utf8'))
            elif CMD == 'DATA_SEND':
                start = BUFSIZE*data_send_count
                if start >= all_data_json_len:
                    s = 'ALL_DATA_END'
                    tcpClientSock.send(s.encode('utf8'))
                    continue
                not_send_len = all_data_json_len - start
                if not_send_len < BUFSIZE:
                    s = all_data_json[start:(start+not_send_len)]
                else:
                    s = all_data_json[start:(start+BUFSIZE)]
                s = 'DATA_SEND:'+s
                data_send_count = data_send_count + 1
                tcpClientSock.send(s.encode('utf8'))
            elif CMD == 'DATA_RESET':
                data_send_count = 0
            else:
                s = 'CMD_NOT_FIND'
                tcpClientSock.send(s.encode('utf8'))
    tcpClientSock.close()
    sock.close()
"""