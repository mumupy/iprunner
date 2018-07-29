#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:54
# @Author  : ganliang
# @File    : TaskExecution.py
# @Desc    : 任务执行器
import logging
import threading

from src.config.TaskConfig import TaskConfig
from src.task.NmapTask import NmapTask
from src.task.ZmapTask import ZmapTask

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class TaskExecution(threading.Thread):
    """每个线程只处理其中几个端口号数据"""

    def __init__(self, taskInfo, allocatePorts, ipFilePaths, everyFileIpCount):
        super(TaskExecution, self).__init__()
        self.taskInfo = taskInfo
        self.taskInstanceId = taskInfo["taskInstanceId"]
        self.allocatePorts = allocatePorts
        self.ipFilePaths = ipFilePaths
        self.everyFileIpCount = everyFileIpCount
        self.nmapTask = NmapTask(self.taskInstanceId)
        self.zmapTask = ZmapTask(self.taskInstanceId)
        logging.info("任务执行器-初始化任务执行器 %s" % self.taskInstanceId)

    def run(self):
        for portStr in self.allocatePorts:
            # 执行zmap任务
            zmapPaths = self.zmapTask.execute(portStr, self.ipFilePaths)
            # 合并zmap文件
            mergeZmapPaths = self.zmapTask.mergeZmapTask(portStr, zmapPaths, self.everyFileIpCount)
            # 执行nmap任务
            nmapPaths = self.nmapTask.execute(portStr, mergeZmapPaths)
            # 执行xml解析
            result_files = self.nmapTask.parseNmapXmlResult(portStr, nmapPaths)
            logging.info(result_files)
