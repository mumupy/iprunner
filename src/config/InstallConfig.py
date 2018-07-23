#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:28
# @Author  : ganliang
# @File    : InstallConfig.py
# @Desc    : 项目中使用到的组件管理

import os


def initInstallComponent():
    """"项目运行之前安装必备的组件"""
    os.system("pip install redis")
