#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 09：50
# @Author  : chenwanyue
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function: 积分规则管理接口

import logging
from flask import session, request, jsonify
from rich_base_provider import response
from rich_base_provider.sysadmin.integral.integral_rule.models import IntegralRule
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_org.models import Sys_org


"""
积分规则管理
"""

def get_integral_rule_list():
    """
    根据页码、搜索条件查询指定数目记录
    :return:
    """
    logging.info("get_integral_rule_list")
    response_dict = {}
    try:
        params = request.get_json()
        page = params.get("page")
        per_page = params.get("per_page")
        # 获取查询条件
        search_data = params.get("search_data")
        integral_rule_list = list(
            IntegralRule.get_integral_rule_list_by_data(page, per_page, session.get("org_code"), search_data))
        response_data_list = format_integral_rule_info(integral_rule_list)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = response_data_list
        if response_data_list:
            response_dict["count"] = IntegralRule.get_integral_rule_total_count(session.get("org_code"), search_data)
        else:
            response_dict["count"] = 0
    except Exception as e:
        logging.exception(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def get_sys_org_list_select():
    """
    分页获取机构信息列表信息加载到select
    :return:
    """
    logging.info("get_sys_org_list_select")
    response_dict = {}
    try:
        params = request.args
        page = params.get("page")
        org_name = params.get("name", "")
        org_info_list = Sys_org.find_sysorg(session.get("org_code"), org_name, page, 10)
        response_data_list = []
        for org_info in org_info_list["orgs"]:
            response_data_list.append({
                "org_id": org_info.org_id,
                "org_name": org_info.org_name
            })
        total_count = Sys_org.find_son_sysorg_count(session.get("org_code"))
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = response_data_list
        response_dict["total_count"] = total_count
    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict['msg'] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def get_child_rule_type_list_select():
    """
    根据integral_rule_type获取其child_rule_type列表
    :return:
    """
    logging.info("get_child_rule_type_list_select")
    response_dict = {}
    try:
        response_data_list = SysDict.get_dict_list_by_type("child_rule_type")
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = response_data_list
    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict['msg'] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def insert_integral_rule():
    """
    根据create_dict添加积分规则
    :return:
    """
    logging.info("insert_integral_rule")
    response_dict = {}
    try:
        params = request.get_json()
        org_id = params.get("org_id")
        integral_rule_type = params.get("integral_rule_type")
        child_rule_type = params.get("child_rule_type")
        integral_condition = params.get("integral_condition")
        receive_integral_count = params.get("receive_integral_count")
        # 验证积分规则是否冲突
        judge_integral_rule_exist = IntegralRule.get_integral_rule_list_by_kwargs(org_id=org_id,
                                                                                  integral_rule_type=integral_rule_type,
                                                                                  child_rule_type=child_rule_type,
                                                                                  integral_condition=integral_condition,
                                                                                  receive_integral_count=receive_integral_count)
        if len(judge_integral_rule_exist) > 0:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "本积分规则已存在"
            response_dict["data"] = []
            return jsonify(response_dict)

        status = params.get("status")
        remarks = params.get("remarks")
        create_dict = {
            "org_id": org_id,
            "integral_rule_type": integral_rule_type,
            "child_rule_type": child_rule_type,
            "integral_condition": int(integral_condition),
            "receive_integral_count": int(receive_integral_count),
            "status": status,
            "remarks": remarks
        }
        IntegralRule.insert_integral_rule_by_create_dict(create_dict)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = []

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def get_integral_rule_info():
    """
    根据积分规则获取本记录详细信息
    :return:
    """
    logging.info("get_integral_rule_info")
    response_dict = {}
    try:
        params = request.get_json()
        integral_rule_id = params.get("integral_rule_id")
        integral_rule_obj = IntegralRule.get_integral_rule_by_integral_rule_id(integral_rule_id)
        # 获取机构名称
        org_obj = Sys_org.get_org_name_by_org_id(integral_rule_obj.org_id)
        org_name = ""
        if org_obj:
            org_name = org_obj.org_name

        response_data_dict = {
            "org_id": integral_rule_obj.org_id,
            "integral_rule_id": integral_rule_obj.integral_rule_id,
            "org_name": org_name,
            "integral_rule_type": integral_rule_obj.integral_rule_type,
            "child_rule_type": integral_rule_obj.child_rule_type,
            "integral_condition": integral_rule_obj.integral_condition,
            "receive_integral_count": integral_rule_obj.receive_integral_count,
            "status": integral_rule_obj.status,
            "remarks": integral_rule_obj.remarks
        }
        # 若存在功能类型 返回功能类型列表
        if integral_rule_obj.child_rule_type != "":
            child_rule_type_list = SysDict.get_dict_list_by_type("child_rule_type")
            response_data_dict["child_rule_type_list"] = child_rule_type_list

        response_data_list = [response_data_dict]
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


def update_integral_rule():
    """
    根据update_dict更新积分规则信息
    :return:
    """
    logging.info("update_integral_rule")
    response_dict = {}
    try:
        params = request.get_json()
        org_id = params.get("org_id")
        integral_rule_id = params.get("integral_rule_id")
        integral_rule_type = params.get("integral_rule_type")
        child_rule_type = params.get("child_rule_type")
        integral_condition = params.get("integral_condition")
        receive_integral_count = params.get("receive_integral_count")
        # 验证积分规则是否冲突
        judge_integral_rule_exist = IntegralRule.get_integral_rule_list_by_kwargs(org_id=org_id,
                                                                                  integral_rule_type=integral_rule_type,
                                                                                  child_rule_type=child_rule_type,
                                                                                  integral_condition=integral_condition,
                                                                                  receive_integral_count=receive_integral_count)
        if len(judge_integral_rule_exist) > 0:
            if integral_rule_id != judge_integral_rule_exist[0].integral_rule_id:
                response_dict["code"] = response.ERROR
                response_dict["msg"] = "本积分规则已存在"
                response_dict["data"] = []
                return jsonify(response_dict)
        status = params.get("status")
        remarks = params.get("remarks")
        update_dict = {
            "integral_rule_id": integral_rule_id,
            "integral_rule_type": integral_rule_type,
            "child_rule_type": child_rule_type,
            "integral_condition": int(integral_condition),
            "receive_integral_count": int(receive_integral_count),
            "status": status,
            "remarks": remarks
        }
        IntegralRule.update_integral_rule_by_update_dict(update_dict)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = []

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def delete_integral_rule():
    """
    根据积分规则ID删除积分规则记录
    :return:
    """
    logging.info("delete_integral_rule")
    response_dict = {}
    try:
        params = request.get_json()
        integral_rule_id = params.get("integral_rule_id")
        IntegralRule.delete_integral_rule_by_integral_rule_id(integral_rule_id)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = []
    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def update_user_point_count(user_code, recharge_money_count):
    """
    根据用户编号、充值金额更新更新该用户总积分数目
    :param user_code:
    :param recharge_money_count:
    :return: 返回此用户此次充值操作可得积分数目（积分数目、积分流水已添加）
    """
    # 添加用户积分 获取可用积分规则
    org_integral_rule_list = IntegralRule.get_org_integral_rule_list_by_data(session.get("org_id"),
                                                                             float(recharge_money_count))
    if len(org_integral_rule_list) > 0:
        giving_integral_count = org_integral_rule_list[0].receive_integral_count
        # 修改用户积分数量、添加积分流水
        if giving_integral_count > 0:
            User.change_user_point("get", user_code, giving_integral_count, org_integral_rule_list[0].integral_rule_id)
        return giving_integral_count
    else:
        return 0


def update_org_point_count(org_id, recharge_money_count):
    """
        根据机构ID、充值金额更新更新该机构总积分数目
        :param org_id:
        :param recharge_money_count:
        :return: 返回此机构此次充值操作可得积分数目（积分数目、积分流水已添加）
    """
    # 添加机构积分 获取可用积分规则
    org_integral_rule_list = IntegralRule.get_org_integral_rule_list_by_data(org_id,
                                                                             float(recharge_money_count))
    if len(org_integral_rule_list) > 0:
        giving_integral_count = org_integral_rule_list[0].receive_integral_count
        # 修改机构积分数量、添加积分流水
        if giving_integral_count > 0:
            Sys_org.change_org_point("get", giving_integral_count, org_integral_rule_list[0].integral_rule_id)
        return giving_integral_count
    else:
        return 0


def format_integral_rule_info(integral_rule_list):
    """
    格式化积分规则主页面数据信息
    :param integral_rule_list:
    :return:
    """
    format_integral_rule_list = []
    for integral_rule_obj in integral_rule_list:
        update_time = str(integral_rule_obj["update_time"]).split(".")[0]
        child_rule_type = ""
        if integral_rule_obj["child_rule_type"] == "":
            child_rule_type = "无功能类型"
        else:
            child_rule_type = SysDict.get_dict_info_by_type_and_id("child_rule_type",
                                                                   integral_rule_obj["child_rule_type"]).dict_name
        format_integral_rule_dict = {
            "integral_rule_id": integral_rule_obj["integral_rule_id"],
            "org_name": integral_rule_obj["sys_org"]["org_name"],
            "integral_rule_type": integral_rule_obj["integral_rule_type_dict"]["dict_name"],
            "child_rule_type": child_rule_type,
            "integral_condition": integral_rule_obj["integral_condition"],
            "receive_integral_count": integral_rule_obj["receive_integral_count"],
            "status": integral_rule_obj["status_dict"]["dict_name"],
            "remarks": integral_rule_obj["remarks"],
            "update_time": update_time
        }
        format_integral_rule_list.append(format_integral_rule_dict)
    return format_integral_rule_list
