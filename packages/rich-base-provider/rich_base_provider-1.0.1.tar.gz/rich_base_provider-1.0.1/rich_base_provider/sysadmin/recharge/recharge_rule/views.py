#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 15：50
# @Author  : chenwanyue
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function: 充值方案管理接口

import logging
from flask import session, request, jsonify
from rich_base_provider import response
from rich_base_provider.sysadmin.recharge.recharge_rule.models import RechargeRule
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_role.models import Role


"""
充值方案管理
"""
def get_recharge_rule_list():
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
            RechargeRule.get_recharge_rule_list_by_data(page, per_page, session.get("org_code"), search_data))
        response_data_list = format_recharge_rule_info(integral_rule_list)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = response_data_list
        if response_data_list:
            response_dict["count"] = RechargeRule.get_recharge_rule_total_count(session.get("org_code"), search_data)
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
                "org_name": org_info.org_name,
                "org_code": org_info.org_code
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


def get_rule_apply_object_list_select():
    """
    根据适用类型获取本机构此类型的适用对象
    :return:
    """
    logging.info("get_rule_apply_object_list_select")
    response_dict = {}
    try:
        response_data_list = []
        params = request.get_json()
        dict_id = params.get("dict_id")
        org_code = params.get("org_code")
        if dict_id == SysDict.get_dict_by_type_and_name("recharge_apply_type", "角色").dict_id:
            # 查询角色
            response_data_list = Role.get_role_list(org_code)
        elif dict_id == SysDict.get_dict_by_type_and_name("recharge_apply_type", "部门").dict_id:
            # 查询部门
            current_org_department_list = Sys_org.get_org_info(org_code).department
            for department in current_org_department_list:
                if department.status != "3":
                    response_data_list.append(department)
        elif dict_id == SysDict.get_dict_by_type_and_name("recharge_apply_type", "机构").dict_id:
            # 查询机构(查询当前充值方案所属机构子机构)
            response_data_list = Sys_org.find_son_sysorg(org_code)

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


def insert_recharge_rule():
    """
    根据create_dict添加充值方案
    :return:
    """
    logging.info("insert_recharge_rule")
    response_dict = {}
    try:
        params = request.get_json()
        org_id = params.get("org_id")
        rule_apply_type = params.get("rule_apply_type")
        rule_name = params.get("rule_name")
        recharge_condition = params.get("recharge_condition")
        giving_count = params.get("giving_count")
        # 验证方案名称是否冲突
        judge_rule_name_exist = RechargeRule.get_recharge_rule_list_by_kwargs(org_id=org_id,
                                                                              rule_apply_type=rule_apply_type,
                                                                              rule_name=rule_name)
        if len(judge_rule_name_exist) > 0:
            response_dict["code"] = response.PARAMETER_ERROR
            response_dict["msg"] = "本充值方案名称已存在"
            response_dict["data"] = []
            return jsonify(response_dict)
        else:
            # 验证满足金额、优惠金额是否冲突
            judge_recharge_exist = RechargeRule.get_recharge_rule_list_by_kwargs(org_id=org_id,
                                                                                 rule_apply_type=rule_apply_type,
                                                                                 recharge_condition=recharge_condition,
                                                                                 giving_count=giving_count)
            if len(judge_recharge_exist) > 0:
                response_dict["code"] = response.PARAMETER_ERROR
                response_dict["msg"] = "本充值方案已存在"
                response_dict["data"] = []
                return jsonify(response_dict)

        rule_start_time = params.get("rule_start_time")
        rule_end_time = params.get("rule_end_time")
        if rule_end_time < rule_start_time:
            response_dict["code"] = response.PARAMETER_ERROR
            response_dict["msg"] = "结束日期不可小于开始日期"
            response_dict["data"] = []
            return jsonify(response_dict)
        rule_apply_object = params.get("rule_apply_object")
        status = params.get("status")
        remarks = params.get("remarks")
        create_dict = {
            "org_id": org_id,
            "rule_apply_type": rule_apply_type,
            "rule_apply_object": rule_apply_object,
            "rule_name": rule_name,
            "recharge_condition": int(recharge_condition),
            "giving_count": int(giving_count),
            "rule_start_time": rule_start_time,
            "rule_end_time": rule_end_time,
            "status": status,
            "remarks": remarks
        }
        RechargeRule.insert_recharge_rule_by_create_dict(create_dict)
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


def find_recharge_rule_update_page(recharge_rule_id):
    """
    返回充值方案管理更新页面
    :return:
    """
    # 获取充值方案适用类型（角色、部门...）
    recharge_apply_type_list = SysDict.get_dict_list_by_type("recharge_apply_type")
    # 获取充值方案状态（启用 停用 删除）
    recharge_status_list = SysDict.get_dict_list_by_type("recharge_status")
    # 获取操作记录所属部门编号org_code
    operation_org_id = RechargeRule.get_recharge_rule_by_recharge_rule_id(recharge_rule_id).org_id
    operation_org_code = Sys_org.get_org_name_by_org_id(operation_org_id).org_code

    recharge_rule_obj = RechargeRule.get_recharge_rule_by_recharge_rule_id(recharge_rule_id)
    rule_apply_type = recharge_rule_obj.rule_apply_type
    # 获取充值方案适用对象列表
    rule_apply_object = recharge_rule_obj.rule_apply_object
    # 获取适用对象列表信息
    rule_apply_object_list = []
    if rule_apply_type == "0":
        # 查询角色
        rule_apply_object_list = Role.get_role_list(operation_org_code)
    elif rule_apply_type == "1":
        # 查询部门
        current_org_department_list = Sys_org.get_org_info(operation_org_code).department
        for department in current_org_department_list:
            if department.status != "3":
                rule_apply_object_list.append(department)
    elif rule_apply_type == "2":
        # 查询机构(查询当前充值方案所属机构子机构)
        rule_apply_object_list = Sys_org.find_son_sysorg(operation_org_code)

    return recharge_apply_type_list,recharge_rule_id,operation_org_code,rule_apply_object,rule_apply_object_list,rule_apply_type,recharge_status_list


def get_recharge_rule_info():
    """
    根据充值方案ID获取本记录具体信息
    :return:
    """
    logging.info("get_recharge_rule_info")
    response_dict = {}
    try:
        params = request.get_json()
        recharge_rule_id = params.get("recharge_rule_id")
        recharge_rule_obj = RechargeRule.get_recharge_rule_by_recharge_rule_id(recharge_rule_id)
        # 获取机构名称
        org_obj = Sys_org.get_org_name_by_org_id(recharge_rule_obj.org_id)
        org_name = ""
        if org_obj:
            org_name = org_obj.org_name
        response_data_dict = {
            "org_id": recharge_rule_obj.org_id,
            "org_name": org_name,
            "rule_name": recharge_rule_obj.rule_name,
            "recharge_condition": recharge_rule_obj.recharge_condition,
            "giving_count": recharge_rule_obj.giving_count,
            "rule_apply_type": recharge_rule_obj.rule_apply_type,
            "rule_apply_object": recharge_rule_obj.rule_apply_object,
            "rule_start_time": str(recharge_rule_obj.rule_start_time)[:-9],
            "rule_end_time": str(recharge_rule_obj.rule_end_time)[:-9],
            "status": recharge_rule_obj.status,
            "remarks": recharge_rule_obj.remarks,
        }
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


def update_recharge_rule():
    """
    根据update_dict更新充值方案信息
    :return:
    """
    logging.info("update_recharge_rule")
    response_dict = {}
    try:
        params = request.get_json()
        org_id = params.get("org_id")
        rule_apply_type = params.get("rule_apply_type")
        rule_name = params.get("rule_name")
        recharge_condition = params.get("recharge_condition")
        giving_count = params.get("giving_count")
        recharge_rule_id = params.get("recharge_rule_id")
        # 验证方案名称是否冲突
        judge_rule_name_exist = RechargeRule.get_recharge_rule_list_by_kwargs(org_id=org_id,
                                                                              rule_apply_type=rule_apply_type,
                                                                              rule_name=rule_name)

        if len(judge_rule_name_exist) > 0:
            if judge_rule_name_exist[0].recharge_rule_id != recharge_rule_id:
                response_dict["code"] = response.PARAMETER_ERROR
                response_dict["msg"] = "本充值方案名称已存在"
                response_dict["data"] = []
                return jsonify(response_dict)

        else:
            # 验证满足金额、优惠金额是否冲突
            judge_recharge_exist = RechargeRule.get_recharge_rule_list_by_kwargs(org_id=org_id,
                                                                                 rule_apply_type=rule_apply_type,
                                                                                 recharge_condition=recharge_condition,
                                                                                 giving_count=giving_count)

            if len(judge_recharge_exist) > 0:
                if judge_recharge_exist[0].recharge_rule_id != recharge_rule_id:
                    response_dict["code"] = response.PARAMETER_ERROR
                    response_dict["msg"] = "本充值方案已存在"
                    response_dict["data"] = []
                    return jsonify(response_dict)
        rule_start_time = params.get("rule_start_time")
        rule_end_time = params.get("rule_end_time")
        if rule_end_time < rule_start_time:
            response_dict["code"] = response.PARAMETER_ERROR
            response_dict["msg"] = "结束日期不可小于开始日期"
            response_dict["data"] = []
            return jsonify(response_dict)

        rule_apply_object = params.get("rule_apply_object")

        status = params.get("status")
        remarks = params.get("remarks")
        update_dict = {
            "recharge_rule_id": recharge_rule_id,
            "rule_apply_type": rule_apply_type,
            "rule_apply_object": rule_apply_object,
            "rule_name": rule_name,
            "recharge_condition": int(recharge_condition),
            "giving_count": int(giving_count),
            "rule_start_time": rule_start_time,
            "rule_end_time": rule_end_time,
            "status": status,
            "remarks": remarks
        }
        RechargeRule.update_recharge_rule_by_update_dict(update_dict)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = []

    except Exception as e:
        logging.exception(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def delete_recharge_rule():
    """
    根据充值方案ID删除充值方案记录
    :return:
    """
    logging.info("delete_recharge_rule")
    response_dict = {}
    try:
        params = request.get_json()
        recharge_rule_id = params.get("recharge_rule_id")
        RechargeRule.delete_recharge_rule_by_recharge_rule_id(recharge_rule_id)
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


def format_recharge_rule_info(recharge_rule_list):
    """
    格式化充值规则主页面数据信息
    :param recharge_rule_list:
    :return:
    """
    format_recharge_rule_list = []
    for recharge_rule_obj in recharge_rule_list:
        format_recharge_rule_dict = {
            "recharge_rule_id": recharge_rule_obj["recharge_rule_id"],
            "org_name": recharge_rule_obj["sys_org"]["org_name"],
            "rule_name": recharge_rule_obj["rule_name"],
            "recharge_condition": recharge_rule_obj["recharge_condition"],
            "giving_count": recharge_rule_obj["giving_count"],
            "rule_apply_type": recharge_rule_obj["rule_apply_type_dict"]["dict_name"],
            "rule_start_time": str(recharge_rule_obj["rule_start_time"]).split(".")[0][:-9],
            "rule_end_time": str(recharge_rule_obj["rule_end_time"]).split(".")[0][:-9],
            "status": recharge_rule_obj["status_dict"]["dict_name"],
            "remarks": recharge_rule_obj["remarks"],
            "update_time": str(recharge_rule_obj["update_time"]).split(".")[0]
        }
        format_recharge_rule_list.append(format_recharge_rule_dict)
    return format_recharge_rule_list
