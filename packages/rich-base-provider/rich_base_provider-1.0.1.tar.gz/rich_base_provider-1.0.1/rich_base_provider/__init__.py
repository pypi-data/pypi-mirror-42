#!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2018/9/20 09：50
# # @Author  : wangwei
# # @Site    : www.rich-f.com
# # @File    : __init__.py
# # @Software: Rich Web Platform
# # @Function: sysadmin模块
"""Main application package."""
from . import sysadmin
from flask import current_app


db = current_app.extensions['db']
mail = current_app.extensions['mail']

