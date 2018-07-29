#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/28 7:56
# @Author  : ganliang
# @File    : ProtocolUtil.py
# @Desc    : 从protocol文件中加载端口、协议、服务名称三元组
import logging, os

from src.config.TaskConfig import TaskConfig

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


def loadProtocol(prototcol_path, sep=None):
    """从protocol文件中加载端口、协议、服务名称三元组"""
    portArray = []
    file = open(prototcol_path, "r")
    for line in list(file.readlines()):
        line = line.replace("\n", "")
        fields = line.split(",")
        id, protocol, serverName, port = fields[0].replace("\"", ""), fields[1].replace("\"", ""), fields[2].replace(
            "\"", ""), fields[-1].replace("\"", "")
        if serverName.find(" ") > -1:
            serverName = serverName[:serverName.find(" ")]
        if serverName.find("_") > -1:
            serverName = serverName.replace("_", "-")
        if sep == None:
            portArray.append((port, protocol, serverName))
        else:
            portArray.append(port + sep + protocol + sep + serverName)

    return set(portArray)


def transorm(prototcol_path):
    file = open(prototcol_path, "r")
    lines = set(file.readlines())
    file.close()
    new_file = open(prototcol_path, "w")
    for line in lines:
        line = line.replace("\n", "")
        new_file.write(line + "\n")
        logging.info(line)
    new_file.close()


if __name__ == "__main__":
    protocols = loadProtocol("../../protocol.csv", "_")
    logging.info(protocols)
    logging.info(protocols.__len__())
    # transorm("../../protocol.csv")
