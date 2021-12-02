#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
...........
@desc:
@date:
@author:
@license:
@contact:

@para:
"""
import os


class RunTimeEnv(object):
    def __init__(self, env: str):
        self.name = env
        self.value = os.getenv(env)

    def __str__(self) -> str:
        return self.value


# 数据库
MYSQL = ''

# 日志输出
LOG_ON = True
LOG_FILE = ''
LOG_FORMAT = '%(asctime)s [ %(levelname)s ] %(message)s'

# 构建环境变量
ROOT_DIR = '/home/jenkins/repo/'
JOB_NAME = os.getenv('JOB_NAME')
WORKSPACE = os.getenv('WORKSPACE')
GIT_PROJECT_URL = os.getenv('GIT_PROJECT_URL')
GIT_BRANCH = os.getenv('GIT_BRANCH')
PENV = os.getenv('PENV')
BUILD_CMD = os.getenv('BUILD_COMMAND')
ARTIFACT_PATH = os.getenv('ARTIFACT_PATH')
DOCKER_FILES = os.getenv('DOCKER_FILES').split(';')
IMAGE_REPO = os.getenv('IMAGE_REPO')
REPO_NAMESPACE = os.getenv('REPO_NAMESPACE')

# Kubernetes
KUBE_CONFIG = ''
