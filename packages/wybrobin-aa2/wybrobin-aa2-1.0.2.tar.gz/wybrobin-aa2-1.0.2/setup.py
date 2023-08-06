#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "wybrobin-aa2",      #这里是pip项目发布的名称
    version = "1.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "aa"),
    description = "aa test",
    long_description = "aa test long",
    license = "MIT Licence",

    url = "https://github.com/wybrobin/packtest",     #项目相关文件地址，一般是github
    author = "wyb",
    author_email = "wyb_robin@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)