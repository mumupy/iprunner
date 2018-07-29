#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : ZmapTask.py
# @Desc    : zmap任务

import logging
import os

from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class ZmapTask:

    def __init__(self, taskInstanceId):
        self.taskInstanceId = taskInstanceId
        self.base_dir = TaskConfig.TASK_TEMP_DIR + self.taskInstanceId

    def execute(self, portStr, ipFilePaths):
        """执行zmap任务"""

        port, protocol, serverName = str(portStr).split("_")
        outPaths, file_counter, zmapDir = [], 0, self.base_dir + "/zmap/"
        if not os.path.exists(zmapDir):
            os.makedirs(zmapDir)

        for ipFilePath in ipFilePaths:
            try:
                if file_counter == 0:
                    outpath = zmapDir + portStr + ".csv"
                else:
                    outpath = zmapDir + portStr + "_" + str(file_counter) + ".csv"

                file_counter += 1
                command = ""
                if protocol.upper() == "TCP":
                    command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 " % (
                        port, TaskConfig.TASK_BRIDGE, outpath, ipFilePath)
                elif protocol.upper() == "UDP":
                    command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 -M udp --probe-args=file:%s" % (
                        port, TaskConfig.TASK_BRIDGE, outpath, ipFilePath, "")
                else:
                    logging.info("unsupport protocol [ %s]" % protocol)
                    continue

                logging.info("执行zmap：" + command)
                value = os.system(command)
                logging.info("zmap执行结果 %s" % value)
                # 删除空文件
                if os.path.exists(outpath):
                    if os.path.getsize(outpath) == 0:
                        os.remove(outpath)
                    else:
                        outPaths.append(outpath)
            except Exception as ex:
                logging.error(ex)
        return outPaths

    def mergeZmapTask(self, portStr, zmapPaths, mergeCount):
        """将多个zmap结果文件合并成一个文件"""

        # 待拆分文件小于1 则不拆分
        if len(zmapPaths) <= 1:
            return zmapPaths

        ipList, current_index, file_counter, merge_files, baseMZmapDir = [], 0, 0, [], self.base_dir + "/mzmap/"
        if not os.path.exists(baseMZmapDir):
            os.makedirs(baseMZmapDir)
        for zmapPath in zmapPaths:
            if not os.path.exists(zmapPath):
                continue
            file = open(zmapPath, "r")
            ipList.extend(set(file.readlines()))
            file.close()

        if len(ipList) == 0:
            return []

        # 合并zmap文件列表
        newMergeFileName = baseMZmapDir + portStr + ".csv"
        merge_files.append(newMergeFileName)
        mergeZmapFile = open(newMergeFileName, "w")
        for ip in ipList:
            current_index += 1
            if current_index >= mergeCount:
                mergeZmapFile.close()
                file_counter += 1
                current_index = 0
                newMergeFileName = baseMZmapDir + portStr + str(file_counter) + ".csv"
                merge_files.append(newMergeFileName)
                mergeZmapFile = open(newMergeFileName, "w")
            if not ip.endswith("\n"):
                ip = ip + "\n"
            mergeZmapFile.write(ip)
        mergeZmapFile.close()
        # 去除最后一个空文件
        if current_index == 0:
            merge_files.remove(newMergeFileName)
        return merge_files
