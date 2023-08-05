#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
File Name   : df.py .

Author      : biolxy
E-mail      : biolxy@aliyun.com
Created Time: 2019-01-29 10:43:44
version     : 1.0
Function    : The author is too lazy to write nothing
Usage       :
"""

def dfTitleName(indf):
    u"""
    使dataframe的title，首字母大写
    """
    columnList = indf.columns.values.tolist()
    dict1 = {}
    for item in columnList:
        item2 = item.title()
        dict1[item] = item2
    print(dict1)
    # str1 = json.dumps(dict1, separators=(',', ':'))
    outdf = indf.rename(columns = dict1)
    return outdf