#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : ZmapTask.py
# @Desc    : zmap任务

import os
import logging
from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class ZmapTask:

    def execute(self, port, ipFilePath):
        """执行zmap任务"""
        port, protocol, protocolName = str(port).split("_")
        outpath = ipFilePath + "_zmap"

        command = ""
        if protocol.upper() == "TCP":
            command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 " % (port, "ens33", outpath, ipFilePath)
        elif protocol.upper() == "UDP":
            command = "zmap -p %s -i %s -o %s -w %s -c 10 -B 20M -T 4 -M udp --probe-args=file:%s" % (
                port, "ens33", outpath, ipFilePath, "")
        logging.info("执行zmap：" + command)
        # value = os.system(command)
        logging.info("zmap执行结果:")
        return outpath
