#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:30
# @Author  : ganliang
# @File    : Main.py
# @Desc    : 程序入口

import logging

logging.basicConfig(level=logging.INFO)

from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig
from src.util.IPUtil import IPUtil


def startTask(taskInstanceId):
    if not isinstance(taskInstanceId, int) or taskInstanceId <= 0:
        message = "taskInstanceId %s IllegalArgument" % str(taskInstanceId)
        logging.error(message)
        return

    # 添加任务
    connection = RedisConfig().connection()
    # 从任务队列中查看该任务是否存在
    taskInstances = connection.lrange(TaskConfig.TASK_INSTANCE_QUEUE, 0, -1)
    for taskInstance in taskInstances:
        if int(taskInstance) == taskInstanceId:
            logging.info("任务 %d 已启动，请等待任务完成" % taskInstanceId)
            return

    connection.lpush(TaskConfig.TASK_INSTANCE_QUEUE, taskInstanceId)
    logging.info("添加任务 : %s" % taskInstanceId)

    # 添加端口列表
    taskPorts = ["80_http_iot", "2181_http_iot", "9000_tcp_iot", "9200_http_iot", "9300_udp_iot"]
    connection.lpush(TaskConfig.TASK_INSTANCE_PORT_PREFIX + str(taskInstanceId), *taskPorts)  # 端口号列表 任务启动之前弹出端口号
    connection.set(TaskConfig.TASK_INSTANCE_COUNTER_PREFIX + str(taskInstanceId), len(taskPorts))  # 端口号数量
    logging.info("添加任务端口 : %s" % taskPorts)

    ## 添加ip列表数据
    taskIps = IPUtil().iplist("27.128.214.0", "27.128.214.255")
    connection.lpush(TaskConfig.TASK_INSTANCE_IP_PREFIX + str(taskInstanceId), *taskIps)

    logging.info("添加任务ip列表 : %s" % taskIps)


if __name__ == "__main__":
    startTask(1)
    startTask(2)
    startTask(3)
    startTask(4)
    startTask(5)
    startTask(6)
    startTask(7)
    startTask(8)
    startTask(9)
    startTask(10)
