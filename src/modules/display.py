# -*- coding: utf-8 -*-
"""
日志输出
"""

import sys
import logging
import src.constants as C
# from .decorator import switcher

logging.basicConfig(level=logging.INFO,  format=C.LOG_FORMAT)
logger = logging.getLogger(__name__)


class Display(object):

    def __init__(self):
        self._infos = {}
        self._warns = {}
        self._errors = {}
        self.format = ''

    # @switcher
    def info(self, messages):
        logger.info(messages)

    # @switcher
    def warn(self, messages):
        logger.warning(messages)

    # @switcher
    def error(self, messages, ignore_errors=None):
        logger.error(messages)
        if not ignore_errors:
            sys.exit(1)

    # @switcher
    def step(self, messages):
        self.format = '-'*9 + '<' + messages + '>' + '-'*9
        print(self.format)

    # @switcher
    def json(self, messages):
        pass
