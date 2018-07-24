#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 23:00
# @Author  : ganliang
# @File    : IPUtil.py
# @Desc    : ip工具类
import socket, struct


class IPUtil:
    def ipToLong(self, ip):
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

    def longToIp(self, longIp):
        return socket.inet_ntoa(struct.pack('!L', longIp))

    def iplist(self, startIp, endIp):
        taskIps = []
        for ip in range(self.ipToLong(startIp), self.ipToLong(endIp) + 1):
            taskIps.append(self.longToIp(ip))
        return taskIps


if __name__ == "__main__":
    iputil = IPUtil()
    print(iputil.ipToLong("27.128.214.0"))
    print(iputil.ipToLong("27.128.214.255"))
    print(iputil.iplist("27.128.214.0", "27.128.214.255"))
