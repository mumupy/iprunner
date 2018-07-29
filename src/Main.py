#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:30
# @Author  : ganliang
# @File    : Main.py
# @Desc    : 程序入口
import logging
import Config as config
config.initInstallComponent()

from src.config.TaskConfig import TaskConfig
from src.core.TaskManager import TaskManager

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


def main():
    taskManager = TaskManager(runingTaskCount=3, taskScanInterval=60, everyTaskThreadCount=3, everyFileIpCount=100)
    taskManager.executeTaskManager()


if __name__ == "__main__":
    main()
