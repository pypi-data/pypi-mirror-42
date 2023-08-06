#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 13:50
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : setting.py
# @Software: Rich Web Platform
# @Function: 系统-配置
import os
import datetime

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.python.runtime import platform


class Config(object):
    """Base configuration."""
    
    SECRET_KEY = os.environ.get('richresource_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13  # 决定encryption的复杂程度，默认值为12
    ASSETS_DEBUG = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    # 允许追踪 login activities
    SECURITY_TRACKABLE = True
    # 密码加密存储
    SECURITY_HASHING_SCHEMES = ['pbkdf2_sha512']
    # 用于创建和验证tokens的不推荐的算法列表. 默认为 hex_md5
    SECURITY_DEPRECATED_HASHING_SCHEMES = []
    SECURITY_PASSWORD_SALT = 'RichChen'
    # 银行卡设置
    
    RICHPAY_URL = 'https://pay.rich-f.com'
    RICH_ACCESS_TOKEN = 'xiWeK0QIBkql4ghBMvYc9tx16PhV0F'
    RICH_CLIENT_ID = '2t9L5e1ZZzaIAoKqaY11g9pk54NbVbuvoBP3Qbna'
    RICH_KEY = 'Y5Uw1YiKnO15DuhV5GeAlRNOZyqUyWkdlD8JHphf11IHJ0EoE5k7AZDnkBBUPKn6K' \
               '2waM411l8kqx4Ma0Ugi8EeOhd4Uqj5MA70vY63VcFXEVYdrlAmKX3r1NgjEa2QQ'
    USER_BIND_CALL_BACK = 'http://127.0.0.1:5000/user_center/wallet/bankcard?bind_success'
    ORG_BIND_CALL_BACK = 'http://127.0.0.1:5000/org_center/wallet/bankcard?bind_success'
    MERCHANT_CODE = 'M0000000017'
    BIND_BANK_CARD = '/apis/pingan/v1/pay/unionpay_bind_card'
    GET_BANK_CARD_INFO = '/apis/pingan/v1/pay/query_bind_card'  # 获取银行卡信息
    
    # 允许注册 register，暂不需要邮件确认
    SECURITY_REGISTERABLE = False  # 生成用户注册点
    SECURITY_SEND_REGISTER_EMAIL = False  # 注册邮件不发送
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['username']  # 用户登陆的字段
    # SECURITY_LOGIN_URL = '/login/'  # 登录端口
    # SECURITY_LOGIN_USER_TEMPLATE = 'public/login.html'  # 登陆页面
    SECURITY_REGISTER_USER_TEMPLATE = 'public/register.html'  # 注册页面
    SECURITY_POST_LOGIN_VIEW = '/'  # 指定用户登录后默认跳转的页面
    # flask-security消息文本
    SECURITY_MSG_USER_DOES_NOT_EXIST = ['用户名错误', '']  # 登陆时用户名错误提醒
    SECURITY_MSG_INVALID_PASSWORD = ['密码错误', '']  # 登陆时密码错误提醒
    SECURITY_TOKEN_MAX_AGE = 86400  # 令牌过期时间  24小时
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BAIDU_MAP_URL = 'http://api.map.baidu.com/geocoder/v2'  # 百度地图URL
    BAIDU_OUTPUT = '&output=json&ak=iN6oMgMYyneB2PVqk40K5qCF9efLTFvj'  # 百度地图out_put






