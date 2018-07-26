#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 19:39
# @Author  : ganliang
# @File    : RedisConfig.py
# @Desc    : redis配置信息

import redis

from src.config.TaskConfig import TaskConfig


class RedisConfig:

    def connection(self):
        """获取redis链接"""

        connection = None
        if TaskConfig.REDIS_AUTH:
            connection = redis.StrictRedis(host=TaskConfig.REDIS_SERVER, port=TaskConfig.REDIS_PORT,
                                           db=TaskConfig.REDIS_DB,
                                           password=TaskConfig.REDIS_AUTH)
        else:
            connection = redis.StrictRedis(host=TaskConfig.REDIS_SERVER, port=TaskConfig.REDIS_PORT,
                                           db=TaskConfig.REDIS_DB)
        return connection

    def close(self, connection):
        """将redis的链接返回到连接池中"""
        connection.connection_pool.disconnect()
