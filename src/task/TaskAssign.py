#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:55
# @Author  : ganliang
# @File    : TaskAssign.py
# @Desc    : 任务分配器
import os
import threading
import time

from TaskExecution import TaskExecution
from src.config.RedisConfig import RedisConfig
from src.config.TaskConfig import TaskConfig


class TaskAssign(threading.Thread):
    """任务执行器 每一个任务是一个线程"""

    def __init__(self, taskInstanceId):
        super(TaskAssign, self).__init__()
        self.taskInstanceId = taskInstanceId
        self.TaskConfig = TaskConfig()
        self.RedisConfig = RedisConfig()

    def assignTaskPort(self, sleepTime=10):
        """分配任务的端口号"""
        connection = self.RedisConfig.connection()
        ports = []

        while True:
            port = connection.lpop(self.TaskConfig.TASK_INSTANCE_PORT_PREFIX + str(self.taskInstanceId))
            if not port:
                break
            ports.append(port)
            time.sleep(sleepTime)  # 休眠 sleepTime 秒 均衡任务分配
        return ports

    def getTaskIps(self, batchCount=1000):
        """获取任务分配的ip列表数据"""
        connection = self.RedisConfig.connection()
        taskInstanceIps = []
        current_index = 0
        while True:
            taskIps = connection.lrange(self.TaskConfig.TASK_INSTANCE_IP_PREFIX + str(self.taskInstanceId),
                                        current_index,
                                        current_index + batchCount)
            taskInstanceIps.extend(taskIps)
            if len(taskIps) < batchCount:
                break
            else:
                current_index += batchCount
        return taskInstanceIps

    def run(self):
        ## 获取任务分配的端口号 如果没有分配到端口号 则结束
        ports = self.assignTaskPort()
        if len(ports) == 0:
            return
        ips = self.getTaskIps()
        port_paths = self.createPortFiles(ports, ips)
        self.executeTask(port_paths, 3)

    def createPortFiles(self, ports, ips):
        port_paths = []
        # 遍历端口号 每一个端口号生成一个文件
        port_dir = self.TaskConfig.TASK_TEMP_DIR + self.taskInstanceId + "/"
        os.makedirs(port_dir)
        for port in ports:
            file = open(port_dir + port)
            port_paths.append(os.path.abspath(file))
            for ip in ips:
                file.write(ip + "\n")
            file.close()
        return port_paths

    def executeTask(self, port_paths, threadCount=10):
        """执行任务"""

        thread_dict = {}
        current_thread_index = 0

        for port_path in port_paths:
            thread_dict.setdefault(current_thread_index % threadCount, []).append(port_path)
            current_thread_index += 1

        taskThreads = []
        for dictKey in thread_dict.keys():
            portPaths = thread_dict.get(dictKey)
            taskExecution = TaskExecution(self.taskInstanceId, portPaths)
            taskExecution.start()
            taskThreads.append(taskExecution)

        # 等待所有的线程执行完毕 在继续
        for taskThread in taskThreads:
            taskThread.join()


if __name__ == "__main__":
    pass
