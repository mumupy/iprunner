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
    taskPorts = [80, 2181, 9000, 9200, 9300]
    connection.lpush(TaskConfig.TASK_INSTANCE_PORT_PREFIX + str(taskInstanceId), *taskPorts)
    logging.info("添加任务端口 : %s" % taskPorts)

    ## 添加ip列表数据
    taskIps = IPUtil().iplist("27.128.214.0", "27.128.214.255")
    connection.lpush(TaskConfig.TASK_INSTANCE_IP_PREFIX + str(taskInstanceId), *taskIps)

    logging.info("添加任务ip列表 : %s" % taskIps)


if __name__ == "__main__":
    startTask(1)
