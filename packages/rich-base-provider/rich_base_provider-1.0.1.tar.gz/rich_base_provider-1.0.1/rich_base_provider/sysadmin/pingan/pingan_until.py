#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 15:44
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : pingan_until.py
# @Software: Rich Web Platform
# @Function: 平安银行管理 工具类

import hashlib
import json
import requests
import random
from datetime import datetime
from rich_base_provider.settings import Config

sys_params = dict(client_id=Config.RICH_CLIENT_ID,
                  access_token=Config.RICH_ACCESS_TOKEN)
sys_key = Config.RICH_KEY

default_merchant_code = Config.MERCHANT_CODE


class RichPayRequest(object):
    """
    richpay 系统平台 请求类封装
    """

    def __init__(self, base_url=None):
        """
        初始化请求类
        :param base_url: 请求域名
        """
        # 默认系统设置 richpay域名
        default_base_url = Config.RICHPAY_URL
        self.base_url = base_url or default_base_url

    def get_bind_bankcard_url(self, user_code, call_back, merchant_code=default_merchant_code):
        """
        用户绑定银行卡
        :param user_code:客户号  user_code
        :return:
        """
        request_data = dict(customer_id=user_code,
                            merchant_code=merchant_code,
                            order_id=create_order_id(),
                            date_time=create_date_time(),
                            return_url=call_back)
        request_data.update(sys_params)
        sign, url_rep = sign_request_data(request_data, sys_key)
        url_rep = url_rep + '&sign={}'.format(sign)
        api_url = Config.BIND_BANK_CARD
        return self.base_url + '{}?{}'.format(api_url, url_rep)

    def get_user_bankcard_info(self, code, merchant_code=default_merchant_code):
        """
        用户查询银行卡信息
        :param code: 用户唯一标识符
        :param merchant_code:
        :return:
        """
        request_data = dict(customer_id=code,
                            merchant_code=merchant_code
                            )
        request_data.update(sys_params)
        sign, url_rep = sign_request_data(request_data, sys_key)
        request_data['sign'] = sign
        api_url = Config.GET_BANK_CARD_INFO
        encoding = 'utf-8'
        headers = {'Content-Type': 'application/json'}
        json_request_data = json.dumps(request_data)
        r = requests.post(self.base_url + api_url, headers=headers, data=json_request_data, timeout=(3, 7))
        r.encoding = encoding
        r.raise_for_status()  # 如果响应状态码不是200，就主动抛出异常
        response = r.json()
        return response


def sign_request_data(request_data, mech_key):
    """
    请求参数签名
    :param request_data: 请求参数
    :param mech_key: 密钥
    :return: GET请求参数
    """
    temp = []

    for key in sorted(request_data):
        if not request_data[key]:
            continue
        temp.append('{}={}'.format(key, request_data[key]))
    temp.append('key=' + mech_key)
    temp_str = '&'.join(temp)
    m = hashlib.md5()
    m.update(temp_str.encode())
    sign = m.hexdigest().upper()
    return sign, temp_str


def create_order_id():
    """
    创建 订单号
    :return:
    """
    # 生成随机数:当前精确到秒的时间再加6位的数字随机序列,用于生成交易订单号
    rd_num = create_date_time()
    ird = random.randint(0, 999999)
    srd = '%06d' % ird  # 字符串格式化,补0位
    order_id = rd_num + srd
    return order_id


def create_date_time():
    """
    请求时 时间
    :return: YYYYMMDDHHMMSS 格式时间
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')
