#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:40
# @Author  : ganliang
# @File    : gynet.py
# @Desc    : 工业互联网流程自动化脚本 1、将容器提交、编译成自启动的镜像。2、docker-compose自动化编排。3、docker环境搭建
import logging
import os
import platform
import sys
import time

logging.basicConfig(
    format="%(asctime)s|%(process)d|%(thread)d|%(filename)s[%(funcName)s:%(lineno)d]|%(levelname)s|%(message)s",
    level=logging.INFO)

# 临时参数
CURRENT_TIME = str(int(time.time()))
DOCKER_COMMIT_TEMP_IMAGE = "gynet_ubuntu_temp:{0}".format(CURRENT_TIME)  # 容器提交为镜像的名称
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")  # 获取当前脚本执行的目录

# docker file
DOCKERFILE_NAME = "gynet_dockerfile_{0}".format(CURRENT_TIME)
DOCKERFILE_PATH = CURRENT_DIR + "/" + DOCKERFILE_NAME

# docker compose
DOCKER_COMPOSE_NAME = "gynet_dockercompose_{0}.yml".format(CURRENT_TIME)
DOCKER_COMPOSE_PATH = CURRENT_DIR + "/" + DOCKER_COMPOSE_NAME

# 程序中使用到的环境变量
ARG_DICT = {
    "NETMASK": "eth0",  # 网卡名称
    "REDIS_HOST": "172.31.134.216",  # redis服务器地址
    "REDIS_PORT": "6379",  # redis端口
    "ES_HOST": "172.31.134.216",  # es服务器
    "ES_PORT": "9200",  # es端口
    "ES_NAME": "gynetres",  # es索引名称
    "ES_TYPE": "gynet_type",  # es索引类型
    "POSTGRE_HOST": "172.31.134.230",  # postgre服务器地址
    "POSTGRE_USER": "ads",  # postgre用户名称
    "POSTGRE_PASSWD": "adspassword",  # postgre用户密码
    "POSTGRE_PORT": "5432",  # postgre端口
    "POSTGRE_DB": "ads",  # postgre数据库
    "TASK_FETCH_KEY_SLEEP": 1,  # 获取端口间隔
    "TASK_MAINTHREAD_SCAN_INTERVEL": 60,  # 任务扫描间隔
}


def dockerBuild(DOCKER_COMMIT_CONTAINER_ID, DOCKER_BUILD_IMAGE, ARG_DICT):
    """执行docker commit 将容器提交成镜像"""
    DOCKER_COMMIT = "docker commit -a '甘亮、殷小康' -m '工业互联网功能初步完成' {0} {1}".format(DOCKER_COMMIT_CONTAINER_ID,
                                                                                DOCKER_COMMIT_TEMP_IMAGE)
    logging.info(DOCKER_COMMIT)
    os.system(DOCKER_COMMIT)

    docker_file_lines = []
    # 执行dockerfile 构建镜像脚本文件
    logging.info("构建镜像文件:" + DOCKERFILE_PATH)

    docker_file_lines.append("FROM {0}".format(DOCKER_COMMIT_TEMP_IMAGE))
    docker_file_lines.append("MAINTAINER 'gynet docker images'")
    docker_file_lines.append("ENV PYTHONPATH /gynet:/usr/lib/python2.7")
    for arg_env in ARG_DICT:
        docker_file_lines.append("ENV {0} {1}".format(arg_env, arg_dict.get(arg_env)))
    docker_file_lines.append("CMD [\"python\",\"/gynet/project/src/main.py\"]")

    docker_file = open(DOCKERFILE_PATH, "w")
    for line in docker_file_lines:
        logging.info(line)
        docker_file.write(line + "\n")
    docker_file.close()

    DOCKER_BUILD = "docker build -t '{0}' -f {1} {2}".format(DOCKER_BUILD_IMAGE, DOCKERFILE_NAME, CURRENT_DIR)
    logging.info(DOCKER_BUILD)
    os.system(DOCKER_BUILD)

    # 删除临时镜像
    DOCKER_DELETE_IMAGE = "docker rmi {0}".format(DOCKER_COMMIT_TEMP_IMAGE)
    logging.info(DOCKER_DELETE_IMAGE)
    os.system(DOCKER_DELETE_IMAGE)


def dockerCompose(DOCKER_IMAGE, CONTAINER_COUNT, ARG_DICT):
    """编写docker-compose编排文件"""

    docker_compose_lines = []

    docker_compose_lines.append("version: '2'")
    docker_compose_lines.append("services:")
    docker_compose_lines.append("     gynet:")
    docker_compose_lines.append("         image: '{0}'".format(DOCKER_IMAGE))
    docker_compose_lines.append("         environment:")
    docker_compose_lines.append("              - PYTHONPATH=/gynet:/usr/lib/python2.7")
    for arg_env in ARG_DICT:
        docker_compose_lines.append("              - {0}={1}".format(arg_env, ARG_DICT.get(arg_env)))
    docker_compose_lines.append("         volumes:")
    docker_compose_lines.append("              - /opt/docker/dockercompose/gynet:/opt/gynet'")

    docker_compose = open(DOCKER_COMPOSE_PATH, "w")
    for line in docker_compose_lines:
        logging.info(line)
        docker_compose.write(line + "\n")
    docker_compose.close()

    DOCKER_COMPOSE_EXECUTION = "docker-compose -f {0} up -d --scale gynet={1}".format(DOCKER_COMPOSE_PATH,
                                                                                      CONTAINER_COUNT)
    logging.info(DOCKER_COMPOSE_EXECUTION)
    os.system(DOCKER_COMPOSE_EXECUTION)


def dockerInstall():
    """安装docker 和docker-compose环境"""

    python_execution = os.system("which python")
    docker_execution = os.system("which docker")
    dockercompose_execution = os.system("which docker-compose")
    if python_execution and docker_execution and dockercompose_execution:
        logging.info("python、docker、docker-compose环境已经安装完成!")
    else:
        my_platform = str(platform.platform()).upper()
        if "UBUNTU" in my_platform:
            os.system("apt-get -y install python")
            os.system("apt-get -y install python-pip")
            os.system("pip install docker-compose")
        elif "CENTOS" in my_platform:
            os.system("yum -y install python")
            os.system("yum -y install epel-release")
            os.system("yum -y install python-pip")
            os.system("pip install docker-compose")
        else:
            logging.warn("unsupport system!")


if __name__ == "__main__":
    # dockerInstall()

    args = sys.argv[1:]
    print("控制台接受参数...  %s" % args)
    if (len(args) == 0):
        logging.warn("usage: python gynet.py dockerfile|dockercompose|all")
        sys.exit(-1)
    docker_arg = str(args[0]).upper()
    if docker_arg == "DOCKERFILE":  # 执行编译容器任务 f2dc0256e7bb、gynet_ubuntu:1.0.0
        docker_commit_container_id, docker_build_image, arg_dict = None, None, {}
        if len(args) == 3:
            docker_commit_container_id = args[1]
            docker_build_image = args[2]
            arg_dict = ARG_DICT
        elif len(args) == 4:
            docker_commit_container_id = args[1]
            docker_build_image = args[2]
            arg_dict = args[3]
        else:
            logging.warn("usage: python gynet.py dockerfile container_id docker_image arg_dict")
            sys.exit(-1)
        dockerBuild(docker_commit_container_id, docker_build_image, arg_dict)
    elif docker_arg == "DOCKERCOMPOSE":  # 执行编排任务
        docker_image, container_count, arg_dict = None, None, {}
        if len(args) == 2:
            docker_image = args[1]
            container_count = 1
            arg_dict = ARG_DICT
        elif len(args) == 3:
            docker_image = args[1]
            container_count = args[2]
            arg_dict = ARG_DICT
        elif len(args) == 4:
            docker_image = args[1]
            container_count = args[2]
            arg_dict = args[3]
        else:
            logging.warn("usage: python gynet.py dockercompose docker_image container_count arg_dict")
            sys.exit(-1)
        dockerCompose(docker_image, container_count, arg_dict)
    elif docker_arg == "ALL":  # 执行所有的任务
        docker_commit_container_id, docker_build_image, container_count, arg_dict = None, None, None, {}
        if len(args) == 3:
            docker_commit_container_id = args[1]
            docker_build_image = args[2]
            container_count = 1
            arg_dict = ARG_DICT
        elif len(args) == 4:
            docker_commit_container_id = args[1]
            docker_build_image = args[2]
            container_count = args[3]
            arg_dict = ARG_DICT
        elif len(args) == 5:
            docker_commit_container_id = args[1]
            docker_build_image = args[2]
            container_count = args[3]
            arg_dict = args[4]
        else:
            logging.warn("usage: python gynet.py all container_id docker_image container_count arg_dict")
            sys.exit(-1)
        dockerBuild(docker_commit_container_id, docker_build_image, arg_dict)
        dockerCompose(docker_build_image, container_count, arg_dict)
    else:
        logging.warn("usage: python gynet.py dockerfile|dockercompose ...")
        sys.exit(-1)
