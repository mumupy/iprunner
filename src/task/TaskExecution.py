#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:54
# @Author  : ganliang
# @File    : TaskExecution.py
# @Desc    : 任务执行器
import threading

from NmapTask import NmapTask
from ZmapTask import ZmapTask


class TaskExecution(threading.Thread):
    """每个线程只处理其中几个端口号数据"""

    def __init__(self, taskInstanceId, port_paths):
        super(TaskExecution, self).__init__()
        self.taskInstanceId = taskInstanceId
        self.port_paths = port_paths
        self.NmapTask = NmapTask()
        self.ZmapTask = ZmapTask()
        self.port_dir = self.TaskConfig.TASK_TEMP_DIR + self.taskInstanceId + "/"

    def executeZmapTask(self):
        """执行zmap任务"""

        zmaplist = []
        for port_path in self.port_paths:
            zmaplist.extend(self.ZmapTask.execute(port_path))
        return set(zmaplist)

    def executeNmapTask(self, iplist):
        """执行nmap任务"""
        self.NmapTask.execute()

    def run(self):
        pass
