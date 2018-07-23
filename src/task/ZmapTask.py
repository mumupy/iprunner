#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : ZmapTask.py
# @Desc    : zmap任务

import os


class ZmapTask:

    def execute(self, port_path):
        """执行zmap任务"""

        port = int(os.path.split(port_path)[1])
        outpath = port_path + "_zmap"
        # zmap -p 80 -N 100 -i ens33 -o zmap.out 随机扫描
        os.system("zmap -p %d -B 1M -i %s -o %s -w %s" % (port, "ens33", outpath, port_path))
        file = open(outpath)
        return list(file.readlines())
