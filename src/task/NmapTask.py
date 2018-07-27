#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : NmapTask.py
# @Desc    : nmap任务

import logging
import os

from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class NmapTask:

    def execute(self, portStr, zmapPaths):
        port, protocol, serverName = str(portStr).split("_")
        nmapOutFiles, file_counter = [], 0
        for zmapPath in zmapPaths:
            nmapBaseDir = os.path.split(os.path.split(zmapPath)[0])[0] + "/nmap/"
            if not os.path.exists(nmapBaseDir):
                os.makedirs(nmapBaseDir)
            nmapoutpath = nmapBaseDir + str(portStr)
            if file_counter == 0:
                nmapoutpath = nmapoutpath + ".xml"
            else:
                nmapoutpath = nmapoutpath + "_" + str(file_counter) + ".xml"

            commname = None
            if protocol.upper() == 'TCP':
                commname = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sT".format(zmapPath, port, nmapoutpath)
            else:
                commname = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sU".format(zmapPath, port, nmapoutpath)
            logging.info("执行nmap：" + commname)
            value = os.system(commname)
            logging.info("nmap执行结果: %s " % value)
            nmapOutFiles.append(nmapoutpath)
            file_counter += 1
        return nmapOutFiles

    def parseNmapXmlResult(self, portStr, nmapOutFiles):
        """解析nmap的xml返回结果"""
        pass
