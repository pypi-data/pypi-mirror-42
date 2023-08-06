#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 17:24
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : views.py


import logging
from flask import  session, request, jsonify
from rich_base_provider import response
from rich_base_provider.sysadmin.integral.integral_charge_record.models import IntegralChargeRecord
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from flask_security import current_user


def get_record_list():
    """
    根据礼品获取积分兑换记录
    :return:
    """
    logging.info('get_record_list')
    response_dict = {}
    try:
        params = request.get_json()
        page = params.get("page")
        per_page = params.get("per_page")
        present_id = params.get('present_id')
        record_list = IntegralChargeRecord.get_record_list_by_data(present_id, page, per_page)
        response_data_list = format_record_info(record_list)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = response_data_list
    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def format_record_info(record_list):
    """
    格式化积分兑换记录主页数据信息
    :param integral_charge_list:
    :return:
    by denghaolin
    """
    from rich_base_provider.sysadmin.sys_user.models import User
    format_integral_charge_list = []
    for record_obj in record_list:
        format_unit_dict = {
            "present_name": record_obj.present_name,
            "present_id": record_obj.present_id,
            'deduct_integral': record_obj.deduct_integral,
            "count": record_obj.count,
            "user_name": User.objects(user_code=record_obj.user_code).first().username if record_obj.user_code else '',
            "org_name": Sys_org.objects(org_id=record_obj.org_id).first().org_name if record_obj.org_id else '',
            "create_time": str(record_obj.create_time).split(".")[0]
        }
        format_integral_charge_list.append(format_unit_dict)
    return format_integral_charge_list


def get_charge_record(org=None):
    """
    根据用户/机构获取积分兑换记录
    :return:
    """
    logging.info("get_charge_record")
    resp_data = {}
    try:
        params = request.get_json()
        page = params.get('page')
        per_page = params.get('per_page')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        if not org:
            record_obj_list, count = IntegralChargeRecord.get_record_by_user_code_or_org_id(
                user_code=current_user.user_code,
                page=page, per_page=per_page, start_time=start_time, end_time=end_time)
        else:
            record_obj_list, count = IntegralChargeRecord.get_record_by_user_code_or_org_id(
                org_id=session.get('org_id'),
                page=page, per_page=per_page, start_time=start_time, end_time=end_time)
        data = format_record_info(record_obj_list)
        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = dict(data=data, count=count)

    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)
