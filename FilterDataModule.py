# -*- coding: utf-8 -*-
import DataBaseModule
import pandas as pd
import ToolModule as tm
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
esp,每股收益
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

printTime(2)
#所有股票代码
all_share_codes = list(all_share_list.index)
all_share_list['code'] = all_share_codes

tmp_list = []
for code in all_share_codes:
    tmp = dataBase.get_share_history_data(code)
    if not isinstance(tmp,pd.DataFrame):
        continue
    tmp['date'] = tmp.index
    tmp['code'] = code
    tmp = pd.merge(tmp,all_share_list.loc[[code]],on='code')
    tmp['dateToMarket'] = tmp.timeToMarket.apply(tm.numToDate)
    tmp_list.append(tmp)

printTime(3)

#将所用的零散信息整理到一张表上
all_data = pd.concat(tmp_list,ignore_index= True)

printTime(4)

print('---filter data end---')
 
if __name__ == '__main__':
    print(all_data.columns)
