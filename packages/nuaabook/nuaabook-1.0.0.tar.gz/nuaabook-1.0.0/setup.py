#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : RyanSu
# @Filename : setup.py
# @Mailto   : i@suruifu.com
# @Website  : https://www.suruifu.com/
from setuptools import setup

setup(
    name='nuaabook',
    version='1.0.0',
    author='Ryan Su',
    author_email='i@suruifu.com',
    url='https://www.suruifu.com/',
    description="南航图书馆电子书下载",
    packages=['nuaabook'],
    install_requires=['requests', 'reportlab']
)
