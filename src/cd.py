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
import subprocess
import constants as C
from modules.display import Display
display = Display()


def replace_dns(file):
    ip = ''
    command = 'kubectl -n {} get svc | grep kube-dns | awk {}'.format(C.PENV, '{print$3}')
    process = subprocess.run(command, capture_output=True, shell=True)
    if process.returncode:
        ip = process.stdout
    else:
        display.error('没有获取CoreDNSip地址')


