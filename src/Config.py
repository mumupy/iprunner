#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/25 23:25
# @Author  : ganliang
# @File    : Config.py
# @Desc    : 项目中使用到的组件管理

import logging,os,sys

current_project = os.path.split(os.getcwd())[0]
sys.path.append(current_project)
from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


def initInstallComponent():
    """"项目运行之前安装必备的组件"""
    logging.info("初始化环境.......")
    logging.info("当前项目工作环境 : %s" % current_project)
    logging.info("当前系统python环境变量: %s" % sys.path)

    logging.info("初始化组件.......")
    os.system("pip install redis")
    os.system("pip install elasticsearch")


if __name__ == "__main__":
    initInstallComponent()
