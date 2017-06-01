# -*- coding: utf-8 -*-
import DataBaseModule
import pandas as pd
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
"""

#原始数据库
dataBase = DataBaseModule.DataBase()

#股票代码，市盈率等信息列表
all_share_list = dataBase.get_share_list_form_local()

#所有股票代码
all_share_codes = list(all_share_list.index)

tmp_list = []
for code in all_share_codes:
    tmp = dataBase.get_share_history_data(code)
    if not isinstance(tmp,pd.DataFrame):
        continue
    tmp['date'] = tmp.index
    tmp['code'] = code
    for item in all_share_list.columns:
        tmp[item] = all_share_list.loc[[code],item][0]
    tmp_list.append(tmp)

#将所用的零散信息整理到一张表上
all_data = pd.concat(tmp_list,ignore_index= True)


if __name__ == '__main__':
    print(all_data.columns)
