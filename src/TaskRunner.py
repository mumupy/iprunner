#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 22:58
# @Author  : ganliang
# @File    : TaskRunner.py
# @Desc    : 任务启动

from src.task.TaskManager import TaskManager


def runner():
    taskManager = TaskManager(3, 3)
    taskManager.executeTaskManager()


if __name__ == "__main__":
    runner()
