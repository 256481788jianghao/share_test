# -*- coding: utf-8 -*-
import DataBaseModule
import pandas as pd




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
