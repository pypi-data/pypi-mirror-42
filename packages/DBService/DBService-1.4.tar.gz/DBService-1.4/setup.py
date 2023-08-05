# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2019-02-18 14:54:32

from setuptools import setup

setup(
    name="DBService",
    version="1.4",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["DBService"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "scrapy",
        "scrapy-redis",
        "pymongo",
        "apscheduler",
        "selenium",
    ],
)
