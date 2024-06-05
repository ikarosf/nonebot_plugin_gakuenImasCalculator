#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "nonebot_plugin_gakuenImasCalculator",
    version = "0.0.4",
    keywords = ("nonebot","plugin", "gakuenImas", "Calculator"),
    description = "NoneBot2学院偶像大师算分插件",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT Licence",

    url = "https://github.com/ikarosf/nonebot_plugin_gakuenImasCalculator",
    author = "ikarosf",
    author_email = "ikarosff@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["nonebot2"]
)