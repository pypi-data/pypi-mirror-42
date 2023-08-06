#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:26:38 2019

@author: liuxiaoyan
"""
from distutils.core import setup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
setup(
          name='xyliuuu',
          version='1.1.0',
          py_modules=['xyliuuu'],
          author='YancyLiu',
          author_email='452939447@qq.com',
          url='http://www.headfirstlabs.com',
          description='A simple test',
          )
      