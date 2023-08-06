#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 11:21
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : views.py

import logging,datetime
from flask import jsonify
from flask import session, request
from rich_base_provider import response
from rich_base_provider.sysadmin.integral.integral_charge.models import IntegralCharge
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from flask_security import current_user
from rich_base_provider.sysadmin.integral.integral_charge_record.models import IntegralChargeRecord
from rich_base_provider.sysadmin.sys_dict.models import SysDict


def get_update_integral_charge_html(present_id):
    """
    获取编辑积分兑换页面
    :param present_id:
    :return:
    by denghaolin
    """
    logging.info('get_update_integral_charge_html')
    try:
        edit_obj = IntegralCharge.get_integral_charge_by_id(present_id)
        res_dict = {
            'present_id': present_id,
            'org_id': edit_obj.org_id,
            'org_name': Sys_org.get_org_name_by_org_id(edit_obj.org_id).org_name,
            'present_name': edit_obj.present_name,
            'integral': edit_obj.integral,
            'stock': edit_obj.stock,
            'types_code': edit_obj.appropriate_types,
            'value_code': edit_obj.appropriate_value,
            'types_data': SysDict.get_dict_info_by_type_and_id(dict_type='integral_charge_type',
                                                               dict_id=edit_obj.appropriate_types).dict_name if edit_obj.appropriate_types else '',
            'value_data': IntegralCharge.get_appropriate_value(edit_obj) if edit_obj.appropriate_types else [],
            'start_time': datetime.datetime.strftime(edit_obj.start_time, '%Y-%m-%d'),
            'end_time': datetime.datetime.strftime(edit_obj.end_time, '%Y-%m-%d'),
            'is_charge': IntegralCharge.present_is_charge(present_id)  # 查询是否已被兑换过（兑换过只能编辑库存）
        }
        return res_dict
    except Exception as e:
        logging.debug(e)
        raise e


def delete_integral_charge():
    """
    删除积分兑换
    :return:
    by denghaolin
    """
    logging.info('delete_integral_charge')
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        if params.get("present_id"):
            IntegralCharge.deleted(params.get("present_id"))
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


def get_integral_charge_list():
    """
    获取积分兑换列表数据
    :return:
    by denghaolin
    """
    logging.info('get_integral_charge_list')
    response_dict = {}
    try:
        params = request.get_json()
        page = params.get("page")
        per_page = params.get("per_page")
        # 获取查询条件
        search_data = params.get("search_data")
        integral_charge_list, count = IntegralCharge.get_integral_charge_list_by_data(page=page, per_page=per_page,
                                                                                      search_data=search_data)
        response_data_list = []
        for integral_charge in integral_charge_list:
            info = {
                'present_id': integral_charge.get('present_id'),
                'present_name': integral_charge.get('present_name'),
                'integral': integral_charge.get('integral'),
                'stock': integral_charge.get('stock'),
                'owner_org': integral_charge['sys_org']['org_name'],
                'start_time': integral_charge.get('start_time').strftime('%F %H:%M:%S'),
                'end_time': integral_charge.get('end_time').strftime('%F %H:%M:%S')
            }
            response_data_list.append(info)
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
            response_dict["data"] = dict(data=response_data_list, count=count)
    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def format_integral_charge_info(integral_charge_list):
    """
    格式化积分兑换主页数据信息
    :param integral_charge_list:
    :return:
    by denghaolin
    """
    format_integral_charge_list = []
    for integral_charge_obj in integral_charge_list:
        start_time = str(integral_charge_obj.start_time).split(".")[0]
        end_time = str(integral_charge_obj.end_time).split(".")[0] if integral_charge_obj.end_time else ''
        format_unit_dict = {
            "present_id": integral_charge_obj.present_id,
            "present_name": integral_charge_obj.present_name,
            'integral': integral_charge_obj.integral,
            "stock": integral_charge_obj.stock,
            "owner_org": Sys_org.get_org_name_by_org_id(integral_charge_obj.org_id).org_name,
            "start_time": start_time,
            "end_time": end_time
        }
        format_integral_charge_list.append(format_unit_dict)
    return format_integral_charge_list


def add_integral_charge():
    """
    新增积分兑换
    :return:
    by denghaolin
    """
    logging.info('add_integral_charge')
    response_data = {}
    try:
        params = request.get_json()
        check_data = ['org_id', 'present_name', 'integral', 'stock', 'start_time', 'end_time', 'appropriate_types'
            , 'appropriate_value']  # 验证参数是否完整
        for data in check_data:
            if data not in params.keys():
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                return jsonify(response_data)
        if not response_data:
            # 判断礼物名称是否在本机构已存在
            exist_present_name = IntegralCharge.get_exist_present_name(org_id=params.get('org_id'),
                                                                       present_name=params.get('present_name'))
            if exist_present_name:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_EXIST_ERROR
                response_data['data'] = ""
            else:
                # 新增积分兑换
                IntegralCharge.add_integral_charge(params)
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


def edit_integral_charge():
    """
    编辑积分兑换
    :return:
    by denghaolin
    """
    logging.info('edit_integral_charge')
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['present_id', 'org_id', 'present_name', 'integral', 'stock', 'start_time', 'end_time',
                      'appropriate_types', 'appropriate_value']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
        if not response_data:
            # 判断礼物名称除自己本身以外是否在本机构已存在
            exit_present_name_in_edit = IntegralCharge.get_exit_present_name_in_edit(params)
            if exit_present_name_in_edit:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_EXIST_ERROR
                response_data['data'] = ""
            else:
                # 更新产品规格
                IntegralCharge.edit_integral_charge(params)
                response_data['code'] = response.SUCCESS
                response_data['msg'] = response.RESULT_SUCCESS
                response_data['data'] = ""
    except Exception as e:
        # 捕获异常
        response_data['code'] = response.RESULT_ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
        logging.debug(e)
    finally:
        # 响应结果
        return jsonify(response_data)


def get_user_data():
    """
    获取用户信息
    :return:
    """
    logging.info('get_user_data')
    res_json = {}
    try:
        from rich_base_provider.sysadmin.sys_user.models import User
        user_code = current_user.user_code
        user_obj = User.objects(user_code=user_code).first()
        user_name = user_obj.username
        user_point = user_obj.wallet.point
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = {'user_name': user_name, 'user_code': user_code, 'user_point': user_point}
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_user_list():
    """
    获取有积分兑换的机构下的所有用户(用作积分兑换礼物选取用户下拉框)
    :return:
    """
    logging.info('get_user_list')
    res_json = {}
    try:
        params = request.args
        page = params.get('page')
        count = None
        result = None
        from rich_base_provider.sysadmin.sys_user.models import User
        org_code_list = IntegralCharge.get_org_code_in_model()  # 获取机构code列表
        data = User.get_select_users_by_org_code_list(org_code_list=org_code_list)
        count = data["count"]
        result = data["user_list"]
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = result
        more = int(page) * 10 < int(count)
        res_json["more"] = more
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_presents():
    """
    # 获取可兑换的礼品列表
    :return:
    """
    logging.info('get_presents')
    res_json = {}
    try:
        params = request.get_json()
        from rich_base_provider.sysadmin.sys_user.models import User
        search_data = params.get('search_data', '')
        page = params.get('page')
        per_page = params.get('per_page')
        # 查询当前登陆用户 所属机构，部门，角色  是否有可兑换的礼品
        # 所属机构列表
        orgs = current_user.org_codes
        # 所属部门
        departments = current_user.org_role[0].department_id
        # 角色
        roles = current_user.org_role[0].role_code
        # 获取当前登录用户所有身份能获取的礼品id列表
        present_id_list = IntegralCharge.get_user_can_charge_present_id_list(orgs=orgs, roles=roles,
                                                                             departments=departments)
        presents, count = IntegralCharge.get_present_list_by_present_id_list(present_id_list, search_data, page,
                                                                             per_page)
        data = []
        for present in presents:
            info = dict(present_name=present.present_name,
                        present_id=present.present_id,
                        integral=present.integral,
                        stock=present.stock,
                        owner_org=Sys_org.get_org_name_by_org_id(present.org_id).org_name,
                        start_time=str(present.start_time).split(".")[0],
                        end_time=str(present.end_time).split(".")[0]
                        )
            data.append(info)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = dict(data=data, count=count)
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def charge_present_to_user():
    """
    兑换礼品
    :return:
    """
    logging.info('charge_present_to_user')
    response_data = {}
    try:
        params = request.get_json()
        check_data = ['present_list', 'user_code']  # 验证参数是否完整
        for data in check_data:
            if data not in params.keys():
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                return jsonify(response_data)
        if not response_data:
            # 查询该用户积分
            user_code = params.get('user_code')
            present_id_list = params.get('present_list')
            from rich_base_provider.sysadmin.sys_user.models import User
            user_integral = User.objects(user_code=user_code).first().wallet.point
            # 获取礼品列表
            present_obj_list = IntegralCharge.get_integral_charge_by_id_list(present_id_list)
            present_need_integral = 0  # 礼品所需积分
            for present_obj in present_obj_list:
                if int(present_obj.stock) < 1:
                    response_data['code'] = response.PARAMETER_ERROR
                    response_data['msg'] = '库存不足'
                    return
                present_need_integral += int(present_obj.integral)
            # 对比礼品所需积分和用户积分
            if int(user_integral) < int(present_need_integral):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = '积分不足'
                return
            else:
                # TODO 用户积分记录
                # 扣除用户积分
                User.objects(user_code=user_code).update_one(
                    set__wallet__point=int(user_integral) - int(present_need_integral),
                    set__update_by=current_user.user_code,
                    set__update_time=datetime.datetime.now())
                req_data = {}
                for present_obj in present_obj_list:
                    req_data['user_code'] = user_code
                    req_data['present_id'] = present_obj.present_id
                    req_data['present_name'] = present_obj.present_name
                    req_data['count'] = 1
                    req_data['deduct_integral'] = present_obj.integral
                    # 积分兑换记录增加兑换记录
                    IntegralChargeRecord.add_record(req_data)
                    # 积分兑换删减礼品库存
                    IntegralCharge.update_stock(req_data)
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


def get_type():
    """
    获取积分兑换使用类型
    :return: code：name键值对
    """
    logging.info('get_type')
    response_data = {}
    try:
        type_list = SysDict.get_dict_list_by_type(dict_type='integral_charge_type')
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


def get_org_data():
    """
    获取当前机构信息
    :return:
    """
    logging.info('get_org_data')
    res_json = {}
    try:
        org_id = session.get('org_id')
        org_obj = Sys_org.objects(org_id=org_id).first()
        org_name = org_obj.org_name
        org_point = org_obj.wallet.point
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = {'org_name': org_name, 'org_id': org_id, 'org_point': org_point}
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_org_present():
    """
    获取当前机构可兑换的礼品
    :return:
    """
    logging.info('get_org_presents')
    res_json = {}
    try:
        params = request.get_json()
        from rich_base_provider.sysadmin.sys_user.models import User
        search_data = params.get('search_data', '')
        page = params.get('page')
        per_page = params.get('per_page')
        org_id = session.get('org_id')
        # 获取当前机构能获取的礼品id列表
        present_id_list = IntegralCharge.get_org_can_charge_present_id_list(org_id)
        presents, count = IntegralCharge.get_present_list_by_present_id_list(present_id_list, search_data, page,
                                                                             per_page)
        data = []
        for present in presents:
            info = dict(present_name=present.present_name,
                        present_id=present.present_id,
                        integral=present.integral,
                        stock=present.stock,
                        owner_org=Sys_org.get_org_name_by_org_id(present.org_id).org_name,
                        start_time=str(present.start_time).split(".")[0],
                        end_time=str(present.end_time).split(".")[0]
                        )
            data.append(info)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = dict(data=data, count=count)
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def charge_present_to_org():
    """
    机构兑换礼品
    :return:
    """
    logging.info('charge_present_to_org')
    response_data = {}
    try:
        params = request.get_json()
        check_data = ['present_list', 'org_id']  # 验证参数是否完整
        for data in check_data:
            if data not in params.keys():
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                return jsonify(response_data)
        if not response_data:
            # 查询该机构积分
            org_id = params.get('org_id')
            present_id_list = params.get('present_list')
            org_integral = Sys_org.objects(org_id=org_id).first().wallet.point
            # 获取礼品列表
            present_obj_list = IntegralCharge.get_integral_charge_by_id_list(present_id_list)
            present_need_integral = 0  # 礼品所需积分
            for present_obj in present_obj_list:
                if int(present_obj.stock) < 1:
                    response_data['code'] = response.PARAMETER_ERROR
                    response_data['msg'] = '库存不足'
                    return
                present_need_integral += int(present_obj.integral)
            # 对比礼品所需积分和机构积分
            if int(org_integral) < int(present_need_integral):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = '积分不足'
                return
            else:
                # TODO 机构积分记录
                # 扣除用户积分
                Sys_org.objects(org_id=org_id).update_one(
                    set__wallet__point=int(org_integral) - int(present_need_integral),
                    set__update_by=current_user.user_code,
                    set__update_time=datetime.datetime.now())
                req_data = {}
                for present_obj in present_obj_list:
                    req_data['org_id'] = org_id
                    req_data['present_id'] = present_obj.present_id
                    req_data['present_name'] = present_obj.present_name
                    req_data['count'] = 1
                    req_data['deduct_integral'] = present_obj.integral
                    # 积分兑换记录增加兑换记录
                    IntegralChargeRecord.add_record(req_data)
                    # 积分兑换删减礼品库存
                    IntegralCharge.update_stock(req_data)
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


