#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:55
# @Author  : ganliang
# @File    : TaskAssign.py
# @Desc    : 任务分配器
import logging
import os
import threading
import time

from TaskExecution import TaskExecution
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class TaskAssign(threading.Thread):
    """任务执行器 每一个任务是一个线程"""

    def __init__(self, taskManager, taskInfo, threadCount=3):
        super(TaskAssign, self).__init__()
        self.threadCount = threadCount  # 每一个任务分配多少线程来并行处理
        self.taskManager = taskManager
        self.taskInfo = taskInfo
        self.taskInstanceId = taskInfo["taskInstanceId"]
        self.taskConfig = TaskConfig()
        self.redisConfig = RedisConfig()
        logging.info("任务分配器-初始化任务分配器 %s" % self.taskInstanceId)

    def assignTaskPort(self, sleepTime=10):
        """分配任务的 端口号_端口协议_other"""
        connection = self.redisConfig.connection()
        ports = []

        while True:
            port = connection.lpop(self.taskConfig.TASK_INSTANCE_PORT_PREFIX + str(self.taskInstanceId))
            if not port:
                break
            ports.append(port)
            time.sleep(sleepTime)  # 休眠 sleepTime 秒 均衡任务分配
        self.taskInfo.setdefault("ports", []).extend(ports)  # 该任务分配的端口号
        logging.info("任务分配器-任务[ %s ] 分配端口号 %s" % (self.taskInstanceId, ports))
        return ports

    def getTaskIps(self, batchCount=1000):
        """获取任务分配的ip列表数据"""
        connection = self.redisConfig.connection()
        taskInstanceIps = []
        current_index = 0
        while True:
            taskIps = connection.lrange(self.taskConfig.TASK_INSTANCE_IP_PREFIX + str(self.taskInstanceId),
                                        current_index,
                                        current_index + batchCount)
            taskInstanceIps.extend(taskIps)
            if len(taskIps) < batchCount:
                break
            else:
                current_index += batchCount
        logging.info("任务分配器-任务[ %s ] ip列表 %s" % (self.taskInstanceId, taskInstanceIps))
        return taskInstanceIps

    def createIpFiles(self, ips, everyFileIpCount=1000):
        """每一个任务只需要创建一个ip文件即可，其他的端口号可以复用这个IP列表文件"""
        port_dir = self.taskConfig.TASK_TEMP_DIR + self.taskInstanceId + "/"
        if not os.path.exists(port_dir):
            os.makedirs(port_dir)

        current_index, file_counter, ipFilePaths, ipFilePath = 0, 0, [], port_dir + "ip"
        ipFilePaths.append(ipFilePath)
        file = open(ipFilePath, "w")
        for ip in ips:
            current_index += 1
            # 大ip文件分片
            if current_index >= everyFileIpCount:
                file.close()
                file_counter += 1
                current_index = 0
                newFileName = port_dir + "ip_" + str(file_counter)
                file = open(newFileName, "w")
                ipFilePaths.append(newFileName)
            file.write(ip + "\n")
        file.close()
        # 去除最后一个空文件
        if current_index == 0:
            ipFilePaths.remove(newFileName)
        logging.info("任务分配器-任务[ %s ] 生成ip数据文件 %s" % (self.taskInstanceId, ipFilePaths))
        return ipFilePaths

    def executeTask(self, ports, ipFilePaths, threadCount=10):
        """执行任务"""
        thread_dict = {}
        current_thread_index = 0

        # 分配任务 将端口号平均分配到 threadCount 个线程中
        for port in ports:
            thread_dict.setdefault(current_thread_index % threadCount, []).append(port)
            current_thread_index += 1

        # 执行任务
        taskThreads = []
        for dictKey in thread_dict.keys():
            allocatePorts = thread_dict.get(dictKey)
            taskExecution = TaskExecution(self.taskInfo, allocatePorts, ipFilePaths)
            taskExecution.start()
            taskThreads.append(taskExecution)
            logging.info("任务分配器-任务[ %s ] 执行子任务[ %d ] : 分配端口号：%s ip数据文件: %s" % (
                self.taskInstanceId, len(taskThreads), allocatePorts, ipFilePaths))

        # 等待所有的线程执行完毕 在继续
        for taskThread in taskThreads:
            taskThread.join()

    def run(self):
        result = True
        try:
            ## 获取任务分配的端口号 如果没有分配到端口号 则结束
            ports = self.assignTaskPort(1)
            if len(ports) == 0:
                logging.info("任务分配器,任务 [ %s ] ，未分配端口号结束。" % self.taskInstanceId)
            else:
                ips = self.getTaskIps()
                ipFilePaths = self.createIpFiles(ips, 1000)
                self.executeTask(ports, ipFilePaths, self.threadCount)
        except StandardError as error:
            result = False
            logging.error(error)
            raise error
        finally:
            self.taskManager.completeTaskAssign(self, result)


if __name__ == "__main__":
    pass
