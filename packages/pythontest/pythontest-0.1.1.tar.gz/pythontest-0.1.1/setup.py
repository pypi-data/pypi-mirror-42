#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
	name = "pythontest",
	version = "0.1.1",
	author="Peng Shiyu",
    license = 'MIT License',  
    author_email="pengshiyuyx@gmail.com",
	url = 'https://github.com/snowroll/python-sdk.git',
	long_description = open('README.md').read(),
	packages = find_packages(),
)
