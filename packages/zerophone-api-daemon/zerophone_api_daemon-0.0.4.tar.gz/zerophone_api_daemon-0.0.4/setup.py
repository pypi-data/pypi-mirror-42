#!/usr/bin/env python
# -*- coding: utf-8 -*-
version = "0.0.4"

try:
    import fastentrypoints
except ImportError:
    from setuptools.command import easy_install
    import pkg_resources
    easy_install.main(['fastentrypoints'])
    pkg_resources.require('fastentrypoints')
    import fastentrypoints

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



if sys.version_info[0] == 2:
    jsonrpclib = "jsonrpclib"
elif sys.version_info[0] == 3:
    jsonrpclib = "jsonrpclib-pelix"


setup(
    name='zerophone_api_daemon',
    py_modules=['zerophone_api_daemon'],
    version=version,
    description='ZeroPhone API daemon',
    author='CRImier',
    author_email='crimier@yandex.ru',
    install_requires=[
        jsonrpclib,
        "PyRIC",
        "zerophone_hw"
    ],
    url = 'https://github.com/ZeroPhone/Zerophone-API-Daemon',
    download_url = 'https://github.com/ZeroPhone/Zerophone-API-Daemon/archive/{}.tar.gz'.format(version),
    entry_points={"console_scripts": ["zerophone_api_daemon = daemon:main"]}
)
import sys


