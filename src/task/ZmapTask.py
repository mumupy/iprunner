#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : ZmapTask.py
# @Desc    : zmap任务

import logging
import os

from src.config.TaskConfig import TaskConfig
from src.util.FileUtil import writeFile

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class ZmapTask:

    def execute(self, portStr, ipFilePaths):
        """执行zmap任务"""
        try:
            port, protocol, serverName = str(portStr).split("_")
            outPaths, file_counter = [], 0
            for ipFilePath in ipFilePaths:
                ipFileDir, ipFileName = os.path.split(ipFilePath)
                zmapDir = ipFileDir + "/zmap/"

                if not os.path.exists(zmapDir):
                    os.makedirs(zmapDir)
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
                # writeFile(outpath, list(open(ipFilePath, "r").readlines()))
                logging.info("zmap执行结果 %s" % value)
                outPaths.append(outpath)
        except Exception as ex:
            logging.error(ex)
            outPaths = []
        return outPaths

    def mergeZmapTask(self, portStr, zmapPaths, mergeCount):
        """将多个zmap结果文件合并成一个文件"""

        if len(zmapPaths) <= 1:
            return zmapPaths

        baseZmapDir, ipList, current_index, file_counter, merge_files = None, [], 0, 0, []
        for zmapPath in zmapPaths:
            zmap_dir, zmap_filename = os.path.split(zmapPath)
            baseZmapDir = zmap_dir + "/"
            if not os.path.exists(zmapPath):
                continue
            file = open(zmapPath, "r")
            ipList.extend(set(file.readlines()))
            file.close()

        if len(ipList) == 0:
            return []

        # 合并zmap文件列表
        newMergeFileName = baseZmapDir + portStr + "_m.csv"
        merge_files.append(newMergeFileName)
        mergeZmapFile = open(newMergeFileName, "w")
        for ip in ipList:
            current_index += 1
            if current_index >= mergeCount:
                mergeZmapFile.close()
                file_counter += 1
                current_index = 0
                newMergeFileName = baseZmapDir + portStr + "_m_" + str(file_counter) + ".csv"
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
