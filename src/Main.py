#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:30
# @Author  : ganliang
# @File    : Main.py
# @Desc    : 程序入口

import Config as config

config.initInstallComponent()

import logging
from src.config.TaskConfig import TaskConfig
from src.core.TaskManager import TaskManager

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


def main():
    taskManager = TaskManager(3, 3)
    taskManager.executeTaskManager()


if __name__ == "__main__":
    main()
