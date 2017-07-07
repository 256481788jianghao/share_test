# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:09:53 2017

@author: Administrator
"""
"""
code,代码
name,名称
esp,每股收益
eps_yoy,每股收益同比(%)
bvps,每股净资产
roe,净资产收益率(%)
epcf,每股现金流量(元)
net_profits,净利润(万元)
profits_yoy,净利润同比(%)
distrib,分配方案
report_date,发布日期

code,代码
name,名称
roe,净资产收益率(%)
net_profit_ratio,净利率(%)
gross_profit_rate,毛利率(%)
net_profits,净利润(万元)
esp,每股收益
business_income,营业收入(百万元)
bips,每股主营业务收入(元)

code,代码
name,名称
arturnover,应收账款周转率(次)
arturndays,应收账款周转天数(天)
inventory_turnover,存货周转率(次)
inventory_days,存货周转天数(天)
currentasset_turnover,流动资产周转率(次)
currentasset_days,流动资产周转天数(天)

code,代码
name,名称
mbrg,主营业务收入增长率(%)
nprg,净利润增长率(%)
nav,净资产增长率
targ,总资产增长率
epsg,每股收益增长率
seg,股东权益增长率

code,代码
name,名称
currentratio,流动比率
quickratio,速动比率
cashratio,现金比率
icratio,利息支付倍数
sheqratio,股东权益比率
adratio,股东权益增长率

code,代码
name,名称
cf_sales,经营现金净流量对销售收入比率
rateofreturn,资产的经营现金流量回报率
cf_nm,经营现金净流量与净利润的比率
cf_liabilities,经营现金净流量对负债比率
cashflowratio,现金流量比率
"""
#import FilterDataModule as fd
import pandas as pd
import tushare as ts

dateDict = {2017:[1],2016:[1,2,3,4]}

g_store = pd.HDFStore("hdf_store.hd5")

for key in dateDict:
    for index in dateDict[key]:
        name = 'report_'+str(key)+'_'+str(index)
        print('start get '+name)
        report = ts.get_report_data(key,index)
        if isinstance(report,pd.DataFrame):
            g_store[name] = report
        else:
            print('report is not a dataframe')
        name = 'cashflow_'+str(key)+'_'+str(index)
        print('start get '+name)
        cashflow = ts.get_cashflow_data(key,index)
        if isinstance(cashflow,pd.DataFrame):
            g_store[name] = cashflow
        else:
            print('cashflow is not a dataframe')
        name = 'profit_'+str(key)+'_'+str(index)
        print('start get '+name)
        profit = ts.get_profit_data(key,index)
        if isinstance(profit,pd.DataFrame):
            g_store[name] = profit
        else:
            print('profit is not a dataframe')
        name = 'operation_'+str(key)+'_'+str(index)
        print('start get '+name)
        operation = ts.get_operation_data(key,index)
        if isinstance(operation,pd.DataFrame):
            g_store[name] = operation
        else:
            print('operation is not a dataframe')
        name = 'growth_'+str(key)+'_'+str(index)
        print('start get '+name)
        growth = ts.get_growth_data(key,index)
        if isinstance(growth,pd.DataFrame):
            g_store[name] = growth
        else:
            print('growth is not a dataframe')
        name = 'debtpaying_'+str(key)+'_'+str(index)
        print('start get '+name)
        debtpaying = ts.get_debtpaying_data(key,index)
        if isinstance(debtpaying,pd.DataFrame):
            g_store[name] = debtpaying
        else:
            print('debtpaying is not a dataframe')

if g_store.is_open:
    g_store.close()