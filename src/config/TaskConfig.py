#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:32
# @Author  : ganliang
# @File    : TaskConfig.py
# @Desc    : 任务配置信息
import logging

class TaskConfig:
    LOGGING_CONFIG = {
        # "filename": "config.log",
        # "filemode": "w",
        "format": "%(asctime)s|%(process)d|%(thread)d|%(filename)s[%(funcName)s:%(lineno)d]|%(levelname)s|%(message)s",
        "level": logging.INFO
    }

    """任务实例队列"""
    TASK_INSTANCE_QUEUE = "task_instance_queue"
    TASK_INSTANCE_IP_PREFIX = "task_instance_ip_"
    TASK_INSTANCE_PORT_PREFIX = "task_instance_port_"
    TASK_INSTANCE_COUNTER_PREFIX = "task_instance_counter_"
    TASK_TEMP_DIR = "/data/taskinstance/"
    TASK_BRIDGE="ens33"

    # redis配置信息
    REDIS_SERVER = "192.168.0.23"
    # REDIS_SERVER = "172.31.134.216"
    REDIS_PORT = 6379
    # REDIS_AUTH = 123456
    REDIS_AUTH = None
    REDIS_DB = 1
