#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:54
# @Author  : ganliang
# @File    : TaskExecution.py
# @Desc    : 任务执行器
import logging
import threading

from NmapTask import NmapTask
from ZmapTask import ZmapTask
from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class TaskExecution(threading.Thread):
    """每个线程只处理其中几个端口号数据"""

    def __init__(self, taskInfo, allocatePorts, ipFilePath):
        super(TaskExecution, self).__init__()
        self.taskInfo = taskInfo
        self.taskInstanceId = taskInfo["taskInstanceId"]
        self.allocatePorts = allocatePorts
        self.ipFilePath = ipFilePath
        self.nmapTask = NmapTask()
        self.zmapTask = ZmapTask()
        logging.info("任务执行器-初始化任务执行器 %s" % self.taskInstanceId)

    def executeZmapTask(self, port, ipFilePath):
        """执行zmap任务"""
        zmappath = self.zmapTask.execute(port, self.ipFilePath)
        return zmappath

    def executeNmapTask(self, port, zmappath):
        """执行nmap任务"""
        self.nmapTask.execute(port, zmappath)

    def run(self):
        for port in self.allocatePorts:
            zmappath = self.executeZmapTask(port, self.ipFilePath)
            nmappath = self.executeNmapTask(port, zmappath)
            logging.info(nmappath)
