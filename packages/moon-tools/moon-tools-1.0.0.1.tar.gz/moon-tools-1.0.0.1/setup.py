#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name = "moon-tools",      #这里是pip项目发布的名称
    version = "1.0.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "moon-tools"),
    description = "Moon's Dev tools",
    long_description = "Moon's Dev tools",
    license = "MIT Licence",

    url = "https://github.com/moonChenHaohui/python_tools",     #项目相关文件地址，一般是github
    author = "moon4Chen",
    author_email = "moon4chen@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)