#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 23:00
# @Author  : ganliang
# @File    : IPUtil.py
# @Desc    : ip工具类
import os
import socket
import struct

current_project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class IPUtil:
    def ipToLong(self, ip):
        """将ip转成long数字"""
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

    def longToIp(self, longIp):
        """将数字转化为ip地址"""
        return socket.inet_ntoa(struct.pack('!L', longIp))

    def iplist(self, startIp, endIp):
        """根据起始ip地址和结束ip地址，获取ip段"""
        taskIps = []
        for ip in range(self.ipToLong(startIp), self.ipToLong(endIp) + 1):
            taskIps.append(self.longToIp(ip))
        return taskIps

    def ipLocation(self, ip):
        """ip定位 定位该ip所属的地区和运营商"""
        if not ip:
            return None

        iptable = open(current_project + "/IPTABLE.csv", "r")
        try:
            for line in iptable.readlines():
                line = line.replace("\"", "")
                start_ip, end_ip, contry, local = line.split(",")
                if self.ipToLong(start_ip) <= self.ipToLong(ip) <= self.ipToLong(end_ip):
                    return (start_ip, end_ip, contry, local)
        finally:
            iptable.close()
        return None


if __name__ == "__main__":
    iputil = IPUtil()
    # print(iputil.ipToLong("27.128.214.0"))
    # print(iputil.ipToLong("27.128.214.255"))
    # print(iputil.iplist("27.128.214.0", "27.128.214.255"))
    ip_location = iputil.ipLocation("27.128.214.0")
    print(ip_location[2])
