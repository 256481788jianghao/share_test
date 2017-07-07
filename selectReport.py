# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:03:53 2017

@author: Administrator
"""
import pandas as pd
g_store = pd.HDFStore("hdf_store.hd5")

print(g_store['report_2017_1'])

if g_store.is_open:
    g_store.close()