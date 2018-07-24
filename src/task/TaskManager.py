#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:25
# @Author  : ganliang
# @File    : TaskManager.py
# @Desc    : 任务管理
import logging

logging.basicConfig(level=logging.INFO)

import time

from TaskAssign import TaskAssign
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig


class TaskManager:
    """任务管理器"""

    def __init__(self, runingTaskCount=10):
        self.runingTaskCount = runingTaskCount
        self.taskContainer = {}  # 任务的容器
        self.taskThreads = []  # 没执行一个任务 保存线程

    def lookupTask(self):
        """从redis中可运行的查询任务"""

        # 判断该任务管理器是否已经满了 如果满载 则退出任务管理
        if len(self.taskContainer.keys()) == self.runingTaskCount:
            logging.info("任务管理器中的任务已经满载,任务挂起！")
            return

        connection = RedisConfig().connection()
        # 从redis中获取到所有的任务
        taskInstances = connection.lrange(TaskConfig.TASK_INSTANCE_QUEUE, 0, -1)
        if len(taskInstances) > 0:
            for taskInstanceId in taskInstances:
                # 判断该任务是否已经在执行了 如果已经在执行了 则过滤该任务
                if taskInstanceId in self.taskContainer.keys():
                    logging.info("任务正在执行，请等候....")
                    continue
                # 判断该任务管理器是否已经满了 如果满载 则退出任务管理
                if len(self.taskContainer.keys()) == self.runingTaskCount:
                    logging.info("任务管理器中的任务已经满载,任务挂起！")
                    break
                # 根据任务实例id查询数据库

                # 执行任务 开启一个新的线程
                taskAssign = TaskAssign(taskInstanceId)
                taskAssign.start()
                logging.info("执行任务 %d" % taskInstanceId)
                self.taskThreads.append(taskAssign)

                # 将任务id填充到任务字典中
                self.taskContainer.setdefault(taskInstanceId, {})
                self.runingTaskCount += 1

    def executeTaskManager(self):
        """执行任务管理器"""

        # 循环扫描任务
        while True:
            self.lookupTask()
            time.sleep(60)

            # 如果任务管理器任务已经满载 则停止接收任务 等待任务完成
            if len(self.taskThreads) == self.runingTaskCount:
                for taskAssign in self.taskThreads:
                    taskAssign.join()
                    # self.taskThreads.remove(taskAssign)
                    # self.taskContainer.pop(taskAssign.taskInstanceId)

                    # 待一半的任务已经执行完毕 则结束任务等待
                    if len(self.taskThreads) <= self.runingTaskCount // 2:
                        break
