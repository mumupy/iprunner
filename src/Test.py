#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 22:34
# @Author  : ganliang
# @File    : Test.py
# @Desc    : 测试程序

import logging
import Config as config
config.initInstallComponent()
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig
from src.util.IPUtil import IPUtil
from src.util.ProtocolUtil import loadProtocol


def startTask(taskInstanceId, taskPorts=None, taskIps=None):
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
    if taskPorts == None:
        taskPorts = ["80_tcp_iot", "2181_udp_iot", "9000_tcp_iot", "9200_tcp_iot", "9300_udp_iot"]
    connection.lpush(TaskConfig.TASK_INSTANCE_PORT_PREFIX + str(taskInstanceId), *taskPorts)  # 端口号列表 任务启动之前弹出端口号
    connection.set(TaskConfig.TASK_INSTANCE_COUNTER_PREFIX + str(taskInstanceId), len(taskPorts))  # 端口号数量
    logging.info("添加任务端口 : %s" % taskPorts)

    ## 添加ip列表数据
    if taskIps == None:
        taskIps = IPUtil().iplist("27.128.214.0", "27.128.214.255")
    connection.lpush(TaskConfig.TASK_INSTANCE_IP_PREFIX + str(taskInstanceId), *taskIps)

    logging.info("添加任务ip列表 : %s" % taskIps)


def removeTask(taskInstanceId):
    """删除任务 将该任务的所有数据都删除掉"""
    connection = RedisConfig().connection()
    connection.delete(TaskConfig.TASK_INSTANCE_QUEUE,
                      TaskConfig.TASK_INSTANCE_IP_PREFIX + str(taskInstanceId),
                      TaskConfig.TASK_INSTANCE_PORT_PREFIX + str(taskInstanceId),
                      TaskConfig.TASK_INSTANCE_COUNTER_PREFIX + str(taskInstanceId))
    logging.info("清理任务[ {0} ]".format(taskInstanceId))


def main(taskInstanceId):
    ports = loadProtocol("../protocol.csv", "_")
    ips = []
    file = open("../results.csv", "r")
    for line in file.readlines():
        ips.append(line.replace("\n", ""))
    logging.info("添加测试数据 任务:{0} ports:{1} ips:{2}".format(taskInstanceId, ports, ips))
    startTask(taskInstanceId, ports, ips)


if __name__ == "__main__":
     # removeTask(113)
     main(114)
    # logging.info("lovecws")

