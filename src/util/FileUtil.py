#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 23:55
# @Author  : ganliang
# @File    : FileUtil.py
# @Desc    : 文件工具类

def writeFile(filePath, ipList):
    if filePath and ipList:
        file = open(filePath)
        for ip in ipList:
            file.write(ip + "\n")
        file.close()
