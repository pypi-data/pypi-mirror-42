#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 11:12
# @Author  : wangzhouyang
# @Site    : www.rich-f.com
# @File    : setup
# @Software: richpay
# @Function:

from setuptools import setup,find_packages

setup(name='rich_base_provider',
      version='1.0.1',
      description='A Python Package Test',
      author='yinchengping',
      author_email='339171112@qq.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='ga nn',
      # project_urls={
      #       'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
      #       'Funding': 'https://donate.pypi.org',
      #       'Source': 'https://github.com/pypa/sampleproject/',
      #       'Tracker': 'https://github.com/pypa/sampleproject/issues',
      # },
      # packages=['rich_base_provider', 'sysadmin', 'coupon', 'integral', 'integral_change', 'integral_change_record', 'integral_rule', 'pingan',
      #           'recharge', 'sys_bin', 'sys_dict', 'sys_org', 'sys_permission', 'sys_role', 'sys_user', 'sys_user_relation', 'task'],
      # packages=['sysadmin'],
      packages = find_packages(),
      # packages=find_packages('rich_base_provider'),
      install_requires=[],
      python_requires='>=3'
     )
