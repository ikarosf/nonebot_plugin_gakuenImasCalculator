#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "nonebot_plugin_gakuenImasCalculator",
    version = "0.1.2",
    keywords = ("nonebot","plugin", "gakuenImas", "Calculator","gakuenIdolMaster"),
    description = "NoneBot2学院偶像大师算分插件",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT Licence",

    url = "https://github.com/ikarosf/nonebot_plugin_gakuenImasCalculator",
    author = "ikarosf",
    author_email = "ikarosff@gmail.com",

    packages = find_packages(),
    install_package_data=True,
    include_package_data = True,
    platforms = "any",
    install_requires = ["nonebot2>=2.2.0,<3.0.0" , "opencv-contrib-python>=4.10.0.0" , "opencv-python>=4.10.0.0","easyocr>=1.7.1"]
)