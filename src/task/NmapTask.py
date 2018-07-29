#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 20:41
# @Author  : ganliang
# @File    : NmapTask.py
# @Desc    : nmap任务

import logging
import os
import xml.dom.minidom
from src.util.IPUtil import IPUtil

from src.config.TaskConfig import TaskConfig
from src.util.ElementUtil import getElement, getTagElement

logging.basicConfig(**TaskConfig.LOGGING_CONFIG)


class NmapTask:

    def __init__(self, taskInstanceId):
        self.taskInstanceId = taskInstanceId
        self.base_dir = TaskConfig.TASK_TEMP_DIR + taskInstanceId
        self.ipUtil = IPUtil()

    def execute(self, portStr, zmapPaths):
        port, protocol, serverName = str(portStr).split("_")
        nmapOutFiles, file_counter, nmapBaseDir = [], 0, self.base_dir + "/nmap/"
        if not os.path.exists(nmapBaseDir):
            os.makedirs(nmapBaseDir)
        for zmapPath in zmapPaths:
            try:
                nmapoutpath = nmapBaseDir + str(portStr)
                if file_counter == 0:
                    nmapoutpath = nmapoutpath + ".xml"
                else:
                    nmapoutpath = nmapoutpath + "_" + str(file_counter) + ".xml"

                commname = None
                if protocol.upper() == 'TCP':
                    commname = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sT".format(zmapPath, port, nmapoutpath)
                elif protocol.upper() == "UDP":
                    commname = "nmap -T5 -sV -Pn -iL {0} -p {1} -oX {2} -sU".format(zmapPath, port, nmapoutpath)
                else:
                    logging.info("unsupport protocol [ %s]" % protocol)
                    continue
                file_counter += 1
                logging.info("执行nmap：" + commname)
                value = os.system(commname)
                logging.info("nmap执行结果: %s " % value)
                # 删除空文件
                if os.path.exists(nmapoutpath):
                    if os.path.getsize(nmapoutpath) == 0:
                        os.remove(nmapoutpath)
                    else:
                        nmapOutFiles.append(nmapoutpath)
            except Exception as ex:
                logging.error(ex)
        return nmapOutFiles

    def parseXml(self, xml_file):
        """解析xml"""
        if not os.path.exists(xml_file):
            return []
        dom = xml.dom.minidom.parse(xml_file)
        rootElement = dom.documentElement
        hostElements = rootElement.getElementsByTagName('host')
        hosts = []
        for hostElement in hostElements:
            try:
                # 获取状态信息
                state = getElement(hostElement, "status", "state")
                # 获取地址信息
                address = getElement(hostElement, "address", "addr")

                # 获取ip对应的域名信息
                hostname = getTagElement(hostElement, "hostnames", "hostname", "name")

                # 获取端口号信息
                portsElements = hostElement.getElementsByTagName("ports")
                # 如果不存在ports节点则过滤该条数据
                if not portsElements:
                    logging.warn("解析xml-过滤数据:不存在ports节点,文件 {0}".format(xml_file))
                    continue

                portElements = portsElements[0].getElementsByTagName("port")
                if not portElements:
                    logging.warn("解析xml-过滤数据:不存在port节点,文件 {0}".format(xml_file))
                    continue

                portElement = portElements[0]
                port_protocol = portElement.getAttribute("protocol")
                portid = portElement.getAttribute("portid")

                # 获取端口的状态和服务
                port_state = getElement(portElement, "state", "state")
                port_service = getElement(portElement, "service", "name")
                port_product = getElement(portElement, "service", "product")
                port_version = getElement(portElement, "service", "version")
                port_ostype = getElement(portElement, "service", "ostype")
                portServiceCpe = getElement(portElement, "service", "servicefp")

                serviceElements = portElement.getElementsByTagName("service")
                if not serviceElements:
                    logging.warn("解析xml-过滤数据:不存在service节点,文件 {0}".format(xml_file))
                    continue

                portCpeElements = serviceElements[0].getElementsByTagName("cpe")
                for portCpeElement in portCpeElements:
                    portServiceCpe += portCpeElement.toxml()

                host_dict = {"state": state, "address": address, "hostname": hostname, "protocol": port_protocol,
                             "portid": portid, "port_state": port_state, "service": port_service,
                             "product": port_product, "version": port_version, "ostype": port_ostype,
                             "service_cpe": portServiceCpe}
                start_ip, end_ip, contry, local = self.ipUtil.ipLocation(address)
                host_dict.setdefault("contry", contry)
                host_dict.setdefault("local", local)
                hosts.append(host_dict)
                logging.info(host_dict)
            except Exception as ex:
                logging.error(ex)
        return hosts

    def parseNmapXmlResult(self, portStr, nmapOutFiles):
        """解析nmap的xml返回结果"""
        result_dir, out_files = self.base_dir + "/result/", []
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        for nmapOutFile in nmapOutFiles:
            hosts = self.parseXml(nmapOutFile)
            if not hosts:
                continue
            out_file = result_dir + portStr + ".csv"
            result_file = open(out_file, "w")
            for host in hosts:
                result_file.write(str(host) + "\n")
            result_file.close()
            out_files.append(out_file)
        return out_files


if __name__ == "__main__":
    nmapTask = NmapTask("1")
    nmapTask.parseXml("../../10001_tcp_atg.xml")
