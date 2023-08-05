# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Email:  hhczy1003@163.com
# @Date:   2017-08-01 20:37:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2019-02-18 14:23:19

from setuptools import setup

setup(
    name="easyspider",
    version="1.4.5",
    author="yiTian.zhang",
    author_email="hhczy1003@163.com",
    packages=["easyspider"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "scrapy",
        "scrapy-redis",
        "pymongo",
        "apscheduler",
        "selenium",
        "elogger",
        "DBService",
        "sqlalchemy",
        "BeautifulSoup4"
    ],
    entry_points={
        "console_scripts": ["easyspider = easyspider.core.cmdline:execute"]
    }
)
