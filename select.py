# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:28:17 2017

@author: Administrator
"""

import pandas as pd
import ToolModule as tm
#import datetime
import FilterDataModule as fd

def getData(code,startDate=None,endDate=None):
    if startDate is None and endDate is None:
        return fd.getHisDataByCode(code)
    elif startDate is not None and endDate is None:
        return fd.getHisDataByCode(code)[startDate:startDate]
    else:
        return fd.getHisDataByCode(code)[startDate:endDate]
