#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

import urllib.request as urlreq
# 设置https代理
ph = urlreq.ProxyHandler({'https': 'https://web-proxy.tencent.com:8080'})
oper = urlreq.build_opener(ph)
# 将代理安装到全局环境，这样所有请求都会自动使用代理
urlreq.install_opener(oper)

setup(
    name='qcloud-python-test',
    version='0.0.1',
    description='this is test for python on pypi',
    url='https://github.com/tencentyun/qcloud-cos-sts-sdk',
    author='qcloudterminal',
    author_email='qcloudterminal@gmail.com',
    license='MIT',
    packages=find_packages(),
)
