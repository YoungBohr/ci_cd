#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='CI/CD',
    version='0.0.1',
    author='',
    author_email='',
    description='CI/CD tools',

    license='GNU GENERAL PUBLIC LICENSE V3.0',
    url='https://gitlab.haojiequ.com/zhanghuanrui/dtk-ci-cd.git',
    package_dir={"": "src"},
    packages=find_packages('src')
)
