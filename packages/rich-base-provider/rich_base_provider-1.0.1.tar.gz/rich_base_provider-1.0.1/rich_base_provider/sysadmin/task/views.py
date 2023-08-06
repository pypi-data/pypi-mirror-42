#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 17:25
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : views.py

from flask import session, jsonify, request
from flask_security import current_user
from rich_base_provider import response
from rich_base_provider.sysadmin.task.models import Task
import logging, datetime
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_dict.models import SysDict


def add_task():
    """
    新增待办
    :return:
    """
    logging.info("add_task")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['title', 'worker', 'limit_time', 'is_critical']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break
        if not response_data:
            # 新增代办
            task_dict = Task.create_task(params)
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = task_dict
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
    finally:
        # 响应结果
        return jsonify(response_data)


def update_task():
    """
    更新代办
    :return:
    """
    logging.info("update_task")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['task_id', 'title', 'worker', 'limit_time', 'is_critical']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break
        if not response_data:
            # 更新代办
            Task.update_task(params)
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = ""
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
    finally:
        # 响应结果
        return jsonify(response_data)


def deal_task():
    """
    代办已处理
    :return:
    """
    logging.info("deal_task")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['task_id']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break
        if not response_data:
            # 代办已处理
            Task.deal_task(params)
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = ""
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
    finally:
        # 响应结果
        return jsonify(response_data)


def get_task_list():
    """
    获取待办列表
    :return:
    """
    logging.info("get_task_list")
    response_data = {}
    result_list = []
    try:
        # 接收参数
        params = request.get_json()
        worker_code = session.get('user_code')
        if worker_code:
            # 获取待办列表
            task_list, task_count = Task.get_task_info(worker_code,
                                                       params.get("search_data"),
                                                       params.get("page"),
                                                       params.get("per_page"))
            for task_obj in task_list:
                result_list.append({"task_id": task_obj.get('task_id'),
                                    "task_code": task_obj.get('task_code'),
                                    "title": task_obj.get('title'),
                                    "remark": task_obj.get('remark'),
                                    "source": task_obj.get('source_user')[0].get('username'),
                                    'worker': task_obj.get('worker_user')[0].get('username'),
                                    'limit_time': task_obj.get('limit_time').strftime('%F %H:%M:%S'),
                                    "create_time": task_obj.get('create_time').strftime('%F %H:%M:%S'),
                                    "status": SysDict.get_dict_info_by_type_and_id('task_status',
                                                                                   task_obj.get('status')).dict_name})
            response_data["code"] = response.SUCCESS
            response_data['data'] = {'data': result_list, 'count': task_count}
            response_data['msg'] = response.RESULT_SUCCESS
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        # 响应结果
        return jsonify(response_data)


def get_task_detail(task_id):
    """
    获取我创建的待办详情
    :param task_id:
    :return:
    """
    try:
        task_obj = Task.get_task_detail_by_id(task_id)
        task_dict = dict(
            task_id=task_obj.task_id,
            title=task_obj.title,
            remark=task_obj.remark,
            source=User.get_user_info_by_user_code(task_obj.source).username,
            worker=[{'worker_code': task_obj.worker,
                     'worker_name': User.get_user_info_by_user_code(task_obj.worker).username}],
            task_type=task_obj.task_type,
            task_type_name=SysDict.get_dict_info_by_type_and_id('task_type', task_obj.task_type).dict_name,
            order_list=task_obj.order_list,
            is_critical=task_obj.is_critical,
            limit_time=datetime.datetime.strftime(task_obj.limit_time, '%Y-%m-%d'),
            status=SysDict.get_dict_info_by_type_and_id('task_status', task_obj.status).dict_name,
            status_code=task_obj.status)

        return task_dict
    except Exception as e:
        logging.debug(e)
        raise e


def get_sponsor_task_list():
    """
    获取创建的待办列表
    :return:
    """
    logging.info("get_sponsor_task_list")
    response_data = {}
    result_list = []
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        source_code = session.get('user_code')
        if source_code:
            # 获取创建的待办列表
            sponsor_task_list, sponsor_task_count = Task.get_task_by_source(source_code,
                                                                            params.get("search_data"),
                                                                            params.get("page"),
                                                                            params.get("per_page"))
            for sponsor_task_obj in sponsor_task_list:
                result_list.append({"task_id": sponsor_task_obj.get('task_id'),
                                    "title": sponsor_task_obj.get('title'),
                                    "content": sponsor_task_obj.get('content'),
                                    "remark": sponsor_task_obj.get('remark'),
                                    "source": sponsor_task_obj.get('source_user')[0].get('username'),
                                    'worker': sponsor_task_obj.get('worker_user')[0].get('username'),
                                    'limit_time': sponsor_task_obj.get('limit_time').strftime('%F %H:%M:%S'),
                                    "create_time": sponsor_task_obj.get('create_time').strftime('%F %H:%M:%S'),
                                    "status": SysDict.get_dict_info_by_type_and_id('task_status',
                                                                                   sponsor_task_obj.get(
                                                                                       'status')).dict_name})
            response_data["code"] = response.SUCCESS
            response_data['data'] = {'data': result_list, 'count': sponsor_task_count}
            response_data['msg'] = response.RESULT_SUCCESS
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        # 响应结果
        return jsonify(response_data)


def get_has_done_task_list():
    """
    获取我已完成的待办列表
    :return:
    """
    logging.info("get_has_done_task_list")
    response_data = {}
    result_list = []
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        worker = current_user.user_code
        if worker:
            # 获取创建的待办列表
            has_done_task_list, has_done_count = Task.get_task_info(worker,
                                                                    params.get("search_data"),
                                                                    params.get("page"),
                                                                    params.get("per_page"),
                                                                    '已完成')
            for has_done_task_obj in has_done_task_list:
                result_list.append({"task_id": has_done_task_obj.get('task_id'),
                                    "title": has_done_task_obj.get('title'),
                                    "content": has_done_task_obj.get('content'),
                                    "remark": has_done_task_obj.get('remark'),
                                    "source": has_done_task_obj.get('source_user')[0].get('username'),
                                    'worker': has_done_task_obj.get('worker_user')[0].get('username'),
                                    'limit_time': has_done_task_obj.get('limit_time').strftime('%F %H:%M:%S'),
                                    "create_time": has_done_task_obj.get('create_time').strftime('%F %H:%M:%S'),
                                    "update_time": has_done_task_obj.get('update_time').strftime('%F %H:%M:%S'),
                                    "status": SysDict.get_dict_info_by_type_and_id('task_status',
                                                                                   has_done_task_obj.get(
                                                                                       'status')).dict_name})
            response_data["code"] = response.SUCCESS
            response_data['data'] = {'data': result_list, 'count': has_done_count}
            response_data['msg'] = response.RESULT_SUCCESS
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        # 响应结果
        return jsonify(response_data)


def update_sponsor_task():
    """
    取消我创建的待办
    :return:
    """
    logging.info("update_sponsor_task")
    response_data = {}
    try:
        params = request.get_json()
        task_id = params.get('task_id')
        status = params.get('status')
        if task_id:
            if status == 'finish':
                Task.update_sponsor_task(task_id, status='已完成')
                response_data['code'] = response.SUCCESS
                response_data['msg'] = response.RESULT_SUCCESS
                response_data['data'] = ""
            elif status == 'cancel':
                Task.update_sponsor_task(task_id)
                response_data['code'] = response.SUCCESS
                response_data['msg'] = response.RESULT_SUCCESS
                response_data['data'] = ""

        else:
            response_data['code'] = response.PARAMETER_ERROR
            response_data['data'] = ""
            response_data['msg'] = response.RESULT_PARAMETER_ERROR

    except Exception as e:
        # 捕获异常
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
        logging.debug(e)
    finally:
        # 响应结果
        return jsonify(response_data)


def get_type():
    """
    获取待办类型
    :return: code：name键值对
    """
    logging.info('get_type')
    response_data = {}
    try:
        type_list = SysDict.get_dict_list_by_type(dict_type='task_type')
        type_info = []
        for type_obj in type_list:
            type_info.append({
                'type_id': type_obj.dict_id,
                'type_name': type_obj.dict_name})
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = type_info
    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        return jsonify(response_data)


def create_level_task():
    """
    创建层级待办(立刻处理指派其他人操作)
    :return:
    """
    logging.info("create_level_task")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['old_task_id', 'new_remark', 'new_worker', 'new_limit_time', 'new_is_critical']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break
        if not response_data:
            # 新增层级代办
            task_dict = Task.create_level_task(params)
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = task_dict
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
    finally:
        # 响应结果
        return jsonify(response_data)


def get_deal_html(task_code):
    """
    获取立刻处理页面
    :param task_code:
    :return:
    """
    logging.info('get_deal_html')
    try:
        task_obj = Task.get_task_detail_by_code(task_code)
        task_dict = dict(
            task_id=task_obj.task_id,
            title=task_obj.title,
            remark=task_obj.remark,
            source=User.get_user_info_by_user_code(task_obj.source).username,
            task_type=task_obj.task_type,
            task_type_name=SysDict.get_dict_info_by_type_and_id('task_type', task_obj.task_type).dict_name,
            order_list=task_obj.order_list,
            is_critical=task_obj.is_critical,
            limit_time=datetime.datetime.strftime(task_obj.limit_time, '%Y-%m-%d'),
            status=SysDict.get_dict_info_by_type_and_id('task_status', task_obj.status).dict_name,
            status_code=task_obj.status)

        return task_dict
    except Exception as e:
        logging.debug(e)
        raise e
