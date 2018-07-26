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

    def execute(self, portStr, ipFilePaths):
        """执行zmap任务"""
        try:
            port, protocol, protocolName = str(portStr).split("_")
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
                    command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 " % (port, "ens33", outpath, ipFilePath)
                elif protocol.upper() == "UDP":
                    command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 -M udp --probe-args=file:%s" % (
                        port, "ens33", outpath, ipFilePath, "")
                else:
                    continue

                logging.info("执行zmap：" + command)
                value = os.system(command)
                logging.info("zmap执行结果 %s" % value)
                outPaths.append(outpath)
        except Exception as ex:
            logging.error(ex)
            outPaths = []
        return outPaths

    def mergeZmapTask(self, zmapPaths, mergeCount=1000):
        # 将多个zmap结果文件合并成一个文件
        ipList, current_index, file_counter, merge_files = [], 0, 0, []
        for zmapPath in zmapPaths:
            zmap_dir, zmap_filename = os.path.split(zmapPath)
            if not os.path.exists(zmapPath):
                continue
            file = open(zmapPath, "r")
            ipList.extend(set(file.readlines()))
            file.close()

        if len(ipList) == 0:
            return []

        # 合并zmap文件列表
        newMergeFileName = zmap_dir + "mzmap"
        merge_files.append(newMergeFileName)
        mergeZmapFile = open(newMergeFileName, "w")
        for ip in ipList:
            current_index += 1
            if current_index >= mergeCount:
                mergeZmapFile.close()
                file_counter += 1
                current_index = 0
                newMergeFileName = zmap_dir + "mzmap_" + file_counter
                merge_files.append(newMergeFileName)
                mergeZmapFile = open(newMergeFileName, "w")
            mergeZmapFile.write(ip + "\n")
        mergeZmapFile.close()
        # 去除最后一个空文件
        if current_index == 0:
            merge_files.remove(newMergeFileName)
        return merge_files
