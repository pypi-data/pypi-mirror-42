#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name = "mazic",
    version = "0.1.0",
    keywords = ("pip", "usual lib","mazic", "mazic"),
    description = "contain some common preprocess function",
    long_description = "A lib contain some common preprocess function",
    license = "MIT Licence",

    url = "https://github.com/mazicwong/mazic",
    author = "mazicwong",
    author_email = "mazic@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []  # 需要的第三方库
)
