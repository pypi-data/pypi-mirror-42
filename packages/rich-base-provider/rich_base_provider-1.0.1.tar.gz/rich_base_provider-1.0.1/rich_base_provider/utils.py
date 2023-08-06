#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/24 09：50
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : utils.py
# @Software: Rich Web Platform
# @Function: 通用
import datetime
import os
import platform
import time
import logging
from urllib.parse import quote

from flask import flash, current_app, send_file
import random
from dateutil.relativedelta import relativedelta
from flask_mail import Message

from rich_base_provider import settings
from rich_base_provider import mail

SECURITY_TOKEN_MAX_AGE = 86400  # 令牌过期时间  24小时
def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def verification_code(k):
    """
    验证码
    :param k: 验证码长度
    :return:
    """
    total = '012345789'
    return random.choices(total, k=k)


def check_file_extensions(filename, extensions):
    """
    判断文件后缀是否合法
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions


def getDictAllowdExtensions():
    """
    可允许的字典文件后缀
    :return:
    """
    return set(['xls', 'xlsx'])


def get_dict_keys():
    """
    文件中字典属性名
    :return:
    """
    return ['字典名', '字典id号', '字典类型', '描述', '序号', '创建者', '创建时间', '更新者', '更新时间', '备注', '状态']


def is_eligible_files(keys, length, data):
    """
    判断文件内容是否符合
    :return:
    """
    logging.info('is_eligible_files')
    if length != len(keys):
        return False
    for i in range(len(keys)):
        if data[i] != keys[i]:
            return False
    return True


def get_time_difference(auth_token_time):
    """
    获取时间差,判断auth_token是否有效
    :return:
    """
    current_time = int(round(time.time()))
    if current_time - int(auth_token_time) > settings.Config.SECURITY_TOKEN_MAX_AGE:
        return False
    else:
        return True


def email_reset_password(name, new_password, email):
    """
    发送密码重置邮件
    :param name:
    :return:
    """
    logging.info('email_reset_password')
    msg = Message('格灵信息密码重置', sender='service@rich-f.com', recipients=[email])
    msg.body = '邮件内容'
    msg.html = "<h1>密码重置成功！<h1> <div> {}您好：</div><div>我们收到了来自您的格灵信息用户密码重置的申请。" \
               "请使用下面的密码进行登录，并尽快设置新的密码。以下是您的密码：</div><h2> {} <h2><div>格灵教育</div>".format(name, new_password)
    with current_app.app_context():  # 获取上下文
        mail.send(msg)  # 发送邮件


def email_send_code(email):
    """
    发送邮箱验证码
    :param email:
    :return:
    """
    logging.info('email_send_code')
    try:
        code = "".join(verification_code(6))  # 生成6位随机数验证码
        msg = Message('格灵信息验证码', sender='service@rich-f.com', recipients=[email])
        msg.body = '邮件内容'
        msg.html = " <div> 您好：</div><div>我们收到了来自您的格灵教育用户密码重置的申请。" \
                   "以下是您的验证码：</div><h2> {} <h2><div>格灵教育</div>".format(code)
        with current_app.app_context():  # 获取上下文
            mail.send(msg)  # 发送邮件
        return code
    except Exception as e:
        logging.debug(e)
        raise e

def resource_size_unit_conversion(size):
    """
    将Byte单位转换为其他单位
    :param size: 只含纯数字的字符串
    :return: 
    """
    if int(size) < 1024:
        size = size + 'B'
    elif int(size) > 1024 and int(size) < 104858:
        size = '%.2f' % (int(size) / 1024) + 'KB'
    elif int(size) > 104858:
        size = '%.2f' % (int(size) / 1048576) + 'MB'
    return size

def get_30_day_list():
    """
    以当前时间为参考，获取前30天的数据列表
    :return: 
    """
    current_time = datetime.datetime.now()
    pre_30_day_time = current_time - datetime.timedelta(days=30)
    date_list = []
    begin_date = pre_30_day_time
    while begin_date <= current_time:
        date_list.append(begin_date.day)
        begin_date += datetime.timedelta(days=1)
    return date_list

def get_12_month_list():
    """
    以当前时间为参考，获取前12月的数据列表
    :return: 
    """
    current_time = datetime.datetime.now()
    pre_11_month = current_time - relativedelta(months=11)
    month_list = []
    begin_month = pre_11_month
    while begin_month <= current_time:
        month_list.append(begin_month.month)
        begin_month += relativedelta(months=1)
    return month_list

def download_file_name(file_name):
    """
    下载文件方法
    :param file_name:
    :return:
    """
    CURRENT_SYSTEM = platform.system()
    basedir = os.getcwd() + '/docs'
    if CURRENT_SYSTEM == 'Windows':
        directory_path = os.path.abspath(basedir) + '\\' + file_name
    else:
        directory_path = os.path.abspath(basedir) + '/' + file_name
    logging.info('docs_download directory_path:{}'.format(directory_path))
    rv = send_file(directory_path, as_attachment=True)
    file_name_quote = quote(file_name)
    if file_name_quote != file_name:  # 下载文件名包含中文的文件，要转换请求头
        rv.headers['Content-Disposition'] = "attachment; filename*=utf-8''%s" % file_name_quote
    if rv:
        return rv
    else:
        return False
