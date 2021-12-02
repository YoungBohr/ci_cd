#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
...........
@desc:
@date:
@author:
@license: GNU GENERAL PUBLIC LICENSE V3.0
@contact:

@para:
"""

import shutil
import argparse
# import sqlalchemy
import constants as C
from modules.build import *
from modules.display import Display

display = Display()


def get_args():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-b', '--build-dir=', required=False, dest='config', help='The path to build')
    parser.add_argument('-c', '--config=', required=False, dest='config', help='Specify the config path')
    parser.add_argument('-i', '--instance=', default='default', dest='instance', help='Select an instance to run')
    parser.add_argument('-r', '--reset=', default=False, required=False, dest='config',
                        help='Force git repo to move the current HEAD to the commit specified ')
    args = parser.parse_args()

    return args


def is_null(val) -> bool:
    if val is None or val == '':
        return True
    else:
        return False


def main():
    # args = get_args()

    for i in (C.JOB_NAME, C.GIT_PROJECT_URL, C.GIT_BRANCH, C.BUILD_CMD, C.ARTIFACT_PATH):
        if is_null(i):
            display.error(f'变量为空')

    # 去掉JOB_NAME前缀
    project_name = '-'.join(C.JOB_NAME.split('_')[1:])
    assert isinstance(project_name, str)
    repo_local_path = C.ROOT_DIR + project_name

    # 同步代码仓库
    repo = Project(project_name, C.GIT_PROJECT_URL, repo_local_path)
    repo.sync(C.GIT_BRANCH)

    # 显示当前HEAD 哈希
    repo.get_head()

    # 输出代码改动
    # repo.diff()

    # 获取最近一次的代码提交信息
    # committer = repo.get_committer_info()

    # 代码构建
    shutil.copytree(repo_local_path, C.WORKSPACE, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
    artifact = repo.Artifact(project_name, C.ARTIFACT_PATH)
    artifact.build(C.WORKSPACE, C.BUILD_CMD)

    # checksum = artifact.checksum()

    # 容器化
    artifact.containerized(C.DOCKER_FILES, C.IMAGE_REPO, C.REPO_NAMESPACE)


if __name__ == '__main__':
    main()
