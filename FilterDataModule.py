# -*- coding: utf-8 -*-
import DataBaseModule
import pandas as pd

#将所用的零散信息整理到一张表上

#原始数据库
dataBase = DataBaseModule.DataBase()

#股票代码，市盈率等信息列表
all_share_list = dataBase.get_share_list_form_local()


if __name__ == '__main__':
    print(all_share_list)
