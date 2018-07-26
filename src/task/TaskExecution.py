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

    def __init__(self, taskInfo, allocatePorts, ipFilePaths):
        super(TaskExecution, self).__init__()
        self.taskInfo = taskInfo
        self.taskInstanceId = taskInfo["taskInstanceId"]
        self.allocatePorts = allocatePorts
        self.ipFilePaths = ipFilePaths
        self.nmapTask = NmapTask()
        self.zmapTask = ZmapTask()
        logging.info("任务执行器-初始化任务执行器 %s" % self.taskInstanceId)

    def executeZmapTask(self, port, ipFilePaths):
        """执行zmap任务"""
        zmapPaths = self.zmapTask.execute(port, ipFilePaths)
        return zmapPaths

    def mergeZmapTask(self, port, zmapPaths):
        """将多个zmap任务结果合并"""
        mergeZmapPaths = self.zmapTask.mergeZmapTask(port, zmapPaths)
        return mergeZmapPaths

    def executeNmapTask(self, port, zmapPaths):
        """执行nmap任务"""
        self.nmapTask.execute(port, zmapPaths)

    def run(self):
        for port in self.allocatePorts:
            # 执行zmap任务
            zmapPaths = self.executeZmapTask(port, self.ipFilePaths)
            # 合并zmap文件
            mergeZmapPaths = self.mergeZmapTask(port, zmapPaths)
            # 执行nmap任务
            nmapPaths = self.executeNmapTask(port, mergeZmapPaths)
            logging.info(nmapPaths)
