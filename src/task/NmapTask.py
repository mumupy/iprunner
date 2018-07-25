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

    def execute(self, port, zmapPaths):
        port, protocol, protocolName = str(port).split("_")
        nmapOutFiles = []
        for zmapPath in zmapPaths:
            # zmapDir, zmapFileName = os.path.split(zmapPath)
            nmapoutpath = zmapPath + "_nmap"
            commName = ""
            if protocol.upper() == 'TCP':
                # commName = "nmap -T5 -sV -Pn -iL [zmap输出的开放特定端口的IP列表] -p 端口号 -oX [输出路径] -sU"
                commName = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sT".format(zmapPath, port, nmapoutpath)
            else:
                commName = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sU".format(zmapPath, port, nmapoutpath)
            logging.info("执行nmap：" + commName)
            value = os.system(commName)
            logging.info("nmap执行结果: %s " % value)
            nmapOutFiles.append(nmapoutpath)
        return nmapOutFiles
