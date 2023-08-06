#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 下午3:01
# @Author  : Lee才晓
# @File    : response.py
# @Function: 

"""
请求码
"""

SUCCESS = "0"  # 请求成功
ERROR = "-1"  # 异常失败
PARAMETER_ERROR = '-2'  # 参数错误
PERMISSION_ERROR = '-3'  # 暂无权限
UN_AUTH_ERROR = "-4"  # auth_token认证失败

"""
请求结果
"""

RESULT_SUCCESS = "请求成功"
RESULT_ERROR = "请求异常"
RESULT_PARAMETER_ERROR = "参数错误"
RESULT_PERMISSION_ERROR = "暂无权限"
RESULT_EXIST_ERROR = "对象已存在"
RESULT_UN_AUTH_ERROR = "认证失败, 请重新登录！"
