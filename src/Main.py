#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:30
# @Author  : ganliang
# @File    : Main.py
# @Desc    : 程序入口
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig
from src.util.IPUtil import IPUtil


def startTask():
    # 添加任务
    connection = RedisConfig().connection()
    taskInstanceId = "1"
    connection.lpush(TaskConfig.TASK_INSTANCE_QUEUE, taskInstanceId)

    # 添加端口列表
    taskPorts = [80, 2181, 9000, 9200, 9300]
    connection.lpush(TaskConfig.TASK_INSTANCE_PORT_PREFIX + taskInstanceId, *taskPorts)

    ## 添加ip列表数据
    taskIps = IPUtil().iplist("27.128.214.0", "27.128.214.255")
    connection.lpush(TaskConfig.TASK_INSTANCE_IP_PREFIX + taskInstanceId, *taskIps)


if __name__ == "__main__":
    # startTask()
    print(IPUtil().ipToLong("27.128.214.0"))
    print(IPUtil().ipToLong("27.128.214.255"))
    print(IPUtil().iplist("27.128.214.0", "27.128.214.255"))
