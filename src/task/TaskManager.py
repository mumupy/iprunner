#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:25
# @Author  : ganliang
# @File    : TaskManager.py
# @Desc    : 任务管理

import time

from TaskAssign import TaskAssign
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig


class TaskManager:
    """任务管理器"""

    def __init__(self, runingTaskCount=10):
        self.runingTaskCount = runingTaskCount
        self.taskContainer = {}

    def lookupTask(self):
        """从redis中可运行的查询任务"""

        # 判断该任务管理器是否已经满了 如果满载 则退出任务管理
        if len(self.taskContainer.keys()) == self.runingTaskCount:
            return

        connection = RedisConfig().connection()
        # 从redis中获取到所有的任务
        taskInstances = connection.lrange(TaskConfig.TASK_INSTANCE_QUEUE, 0, -1)
        if len(taskInstances) > 0:
            for taskInstanceId in taskInstances:
                # 判断该任务是否已经在执行了 r如果已经在执行了 则过滤该任务
                if taskInstanceId in self.taskContainer.keys():
                    continue
                # 判断该任务管理器是否已经满了 如果满载 则退出任务管理
                if len(self.taskContainer.keys()) == self.runingTaskCount:
                    break
                # 根据任务实例id查询数据库

                # 执行任务 开启一个新的线程
                taskExecution = TaskAssign()
                taskExecution.start()
                # 将任务id填充到任务字典中
                self.taskContainer.setdefault(taskInstanceId, {})
                self.runingTaskCount += 1

    def executeTaskManager(self):
        """执行任务管理器"""

        # 循环扫描任务
        while True:
            self.lookupTask()
            time.sleep(60)
