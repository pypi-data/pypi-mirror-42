#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/30 13:47
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function:

import logging, os, platform
from flask import send_file, jsonify, request
from rich_base_provider import response

CURRENT_SYSTEM = platform.system()
basedir = os.getcwd() + '/logs'


def get_bin_logs():
    """
    获取日志文件信息
    :return:
    """
    logging.info('get_bin_logs')
    try:
        params = request.values.to_dict()
        search_data = params.get('search_data') or ''
        per_page = params.get('per_page')

        start_index = int(params.get("page"))
        end_index = start_index + int(per_page)
        file_info_list = []  # 返回信息
        count = None
        if os.path.exists(basedir):
            file_names = [file_name for file_name in os.listdir(basedir) if search_data in file_name]  # 查询日志
            count = len(file_names)
            file_names = file_names[start_index: end_index]  # 分页
            if file_names:
                for file_name in file_names:
                    file_info = {}
                    # file_name
                    file_info['log_file_name'] = file_name
                    start_index = file_name.index('-')
                    end_index = file_name.index('.')
                    # file_data
                    file_info['log_file_time'] = file_name[start_index + 1:end_index]
                    # file_root
                    if CURRENT_SYSTEM == 'Windows':
                        file_info['log_file_path'] = os.path.abspath(basedir) + '\\' + file_name
                    else:
                        file_info['log_file_path'] = os.path.abspath(basedir) + '/' + file_name
                    file_info_list.append(file_info)
        return jsonify({'rows': file_info_list,'total': count})
    except Exception as e:
        logging.debug(e)
        return jsonify({'rows':[], 'total': 0})


def log_file_download(log_file_name):
    """
    下载日志文件信息
    :return:
    """
    logging.info('log_file_download')
    try:
        if CURRENT_SYSTEM == 'Windows':
            directory_path = os.path.abspath(basedir) + '\\' + log_file_name
        else:
            directory_path = os.path.abspath(basedir) + '/' + log_file_name
        logging.info('log_file_download directory_path:{}'.format(directory_path))
        return send_file(directory_path, as_attachment=True)
    except Exception as e:
        logging.debug(e)
        return jsonify({'code': response.ERROR,
                        'msg': '请求失败'})


def log_file_delete():
    """
    删除日志文件
    :return:
    """
    logging.info('log_file_delete')
    try:
        param = request.get_json()
        name = param.get('log_file_name')
        if CURRENT_SYSTEM == 'Windows':
            directory_path = os.path.abspath(basedir) + '\\' + name
        else:
            directory_path = os.path.abspath(basedir) + '/' + name

        logging.info('log_file_delete directory_path:{}'.format(directory_path))
        os.remove(directory_path)
        return jsonify({'code': response.SUCCESS, 'desc': '删除成功!'})
    except Exception as e:
        logging.debug(e)
        return jsonify({'code': response.ERROR, 'msg': '删除失败'})
