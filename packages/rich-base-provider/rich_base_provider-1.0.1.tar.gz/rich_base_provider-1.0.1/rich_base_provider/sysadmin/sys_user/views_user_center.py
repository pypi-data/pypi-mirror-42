#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 15:54
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : views_user_center.py
# @Software: Rich Web Platform
# @Function:

from flask import request, session, jsonify
from rich_base_provider import response
from rich_base_provider.sysadmin.coupon.models import Coupon
from rich_base_provider.sysadmin.recharge.recharge_rule.models import RechargeRule
from rich_base_provider.sysadmin.integral.integral_rule import views as IntegralRuleViews
from rich_base_provider.sysadmin.recharge.balance_recharge_record.models import BalanceRechargeRecord
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from flask_security import current_user
from rich_base_provider.sysadmin.pingan.pingan_until import *
import logging, re
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.integral.integral_rule.models import IntegralRule


def get_unused_coupons():
    """
    获取未使用优惠券
    :return:
    """
    logging.info("get_unused_coupons")
    resp_data = {}
    try:
        params = request.get_json()
        page = params.get('page')
        per_page = params.get('per_page')
        coupon_code_list = []
        for coupon in current_user.wallet.coupons:
            if not coupon.use_time:
                coupon_code_list.append(coupon.coupon_code)
        coupons = Coupon.get_unused_coupon_info(coupon_code_list, page, per_page)
        data = []
        if coupons:
            data = get_coupons(coupon_code_list, coupons)

        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = data

    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)



def get_used_coupons():
    """
    获取已使用优惠券
    :return:
    """
    logging.info('get_used_coupons')
    resp_data = {}
    try:
        params = request.get_json()
        page = params.get('page')
        per_page = params.get('per_page')
        user_code = current_user.user_code
        coupons = Coupon.get_used_coupons(user_code, page, per_page)
        data = []
        if coupons:
            data = get_used_coupons_method(coupons)
        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = data

    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)


def get_expired_coupons():
    """
    获取已失效优惠券
    :return:
    """
    logging.info('get_expired_coupons')
    resp_data = {}
    try:
        params = request.get_json()
        page = params.get('page')
        per_page = params.get('per_page')
        coupon_code_list = []
        for coupon in current_user.wallet.coupons:
            if not coupon.use_time:
                coupon_code_list.append(coupon.coupon_code)
        coupons = Coupon.get_expired_coupon_info(coupon_code_list, page, per_page)
        data = []
        if coupons:
            data = get_coupons(coupon_code_list, coupons)
        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = data

    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)


def update_bankcard():
    """用户银行卡绑定后回调,请求银联数据，记录用户银行卡信息"""
    logging.info('update_bankcard')
    resp_data = {}
    try:
        req = RichPayRequest()
        response_data = req.get_user_bankcard_info(current_user.user_code)
        if response_data.get('code') == '0':
            bank_card_list = response_data['data']['bind_acc_list']
            query_result = current_user.update_bank_card_info(bank_card_list)
            if query_result:
                resp_data['code'] = response.SUCCESS
                resp_data['msg'] = response.RESULT_SUCCESS
                resp_data['data'] = []
            else:
                resp_data["code"] = response.ERROR
                resp_data["msg"] = response.RESULT_ERROR
                resp_data["data"] = []
        else:
            resp_data["code"] = response.ERROR
            resp_data["msg"] = response.RESULT_ERROR
            resp_data["data"] = []
    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)



def get_bankcards_info():
    """
    用户银行卡信息获取
    :return:
    """
    logging.info(get_bankcards_info)
    resp_data = {}
    try:
        data = current_user.get_bank_cards_info()
        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = data
    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)


def get_recharge_rule():
    """
    根据用户部门信息、角色信息、获取充值规则
    :return:
    """
    logging.info('get_recharge_rule')
    resp_data = {}
    try:
        # 获取当前操作用户银行卡信息列表、所处部门信息...
        current_user_dict = User.get_user_by_org_and_data(session.get("org_code"), session.get("username"))[0]
        # 部门信息
        for org_role in current_user_dict["org_role"]:
            # 获取该用户在此机构下所有部门信息以及角色信息
            if org_role["org_code"] == session.get("org_code"):
                role_code_list = org_role["role_code"]
                department_id_list = org_role["department_id"]
        rule_apply_object = department_id_list + role_code_list
        rule_apply_type = [SysDict.get_dict_by_type_and_name("recharge_apply_type", "角色").dict_id,
                           SysDict.get_dict_by_type_and_name("recharge_apply_type", "部门").dict_id]
        recharge_rule_list = RechargeRule.get_recharge_rule_all_by_data(rule_apply_object,
                                                                        session.get("org_id"), rule_apply_type)

        response_data_list = format_recharge_rule(recharge_rule_list)
        resp_data["code"] = response.SUCCESS
        resp_data["msg"] = response.RESULT_SUCCESS
        resp_data["data"] = response_data_list
    except Exception as e:
        logging.exception(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)



def user_balance_recharge():
    """
    用户余额充值
    :return:
    """
    logging.info('user_balance_recharge')
    resp_data = {}
    try:
        params = request.get_json()
        # 充值金额
        recharge_money_count = params.get("recharge_money_count")
        # 付款账户
        payment_account = params.get("payment_account")
        # 充值方案
        recharge_rule_id = params.get("recharge_rule_id")
        # 支付密码
        datapw = params.get("datapw")
        # 验证支付密码
        current_user_obj = User.get_by(user_code=session.get("user_code"))
        check_flag = current_user_obj.check_pay_password(datapw)
        if check_flag:
            # 支付密码输入正确
            # 实付金额
            real_pay_count = ""
            if not recharge_rule_id:
                # 用户没有选择充值方案 或者 没有充值方案
                User.change_user_balance("recharge", recharge_money_count)
                real_pay_count = float(recharge_money_count)
            else:
                # 获取充值方案详情 （计算实付金额）
                recharge_rule = RechargeRule.get_recharge_rule_by_recharge_rule_id(recharge_rule_id)
                real_pay_count = float(recharge_money_count) - float(recharge_rule.giving_count)
                User.change_user_balance("recharge", recharge_money_count)

            # 获取本次操作可得积分 执行积分更新操作
            giving_integral_count = IntegralRuleViews.update_user_point_count(session.get("user_code"),
                                                                              recharge_money_count)
            recharge_record_create_dict = {
                "recharge_object_type": SysDict.get_dict_by_type_and_name("recharge_object_type", "用户充值").dict_id,
                "recharge_object_code": current_user.user_code,
                "recharge_money_count": recharge_money_count,
                "recharge_rule_id": recharge_rule_id,
                "real_pay_count": real_pay_count,
                "payment_method": payment_account,
                "giving_integral_count": giving_integral_count
            }
            if payment_account == SysDict.get_dict_by_type_and_name("recharge_payment_method", "微信").dict_id:
                # 微信支付
                recharge_record_create_dict["payment_account"] = "微信账户"
            elif payment_account == SysDict.get_dict_by_type_and_name("recharge_payment_method",
                                                                      "支付宝").dict_id:
                # 支付宝支付
                recharge_record_create_dict["payment_account"] = "支付宝账户"
            else:
                # 银行卡
                recharge_record_create_dict["payment_account"] = payment_account
            # 添加余额充值记录
            BalanceRechargeRecord.insert_balance_recharge_record_by_create_dict(recharge_record_create_dict)
            resp_data["code"] = response.SUCCESS
            resp_data["msg"] = response.RESULT_SUCCESS
            resp_data["data"] = []
        else:
            # 支付密码输入错误
            resp_data["code"] = response.PARAMETER_ERROR
            resp_data["msg"] = "密码输入错误"
            resp_data["data"] = []
    except Exception as e:
        logging.exception(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)


def recharge_record():
    """
    钱包中充值记录
    :return:
    """
    logging.info(recharge_record)
    resp_data = {}
    try:
        params = request.get_json()
        code = current_user.user_code
        data_obj = BalanceRechargeRecord.get_record_by_recharge_object_code(code=code, **params)
        data = []
        for info in data_obj:
            data_dict = dict(money_count=info.get('recharge_money_count'),
                             recharge_time=info.get('recharge_time').strftime('%F %H:%M:%S'),
                             recharge_status=info.get('sys_dict').get('dict_name'),
                             record_id=info.get('record_id'))
            data.append(data_dict)
        resp_data['code'] = response.SUCCESS
        resp_data['msg'] = response.RESULT_SUCCESS
        resp_data['data'] = data
    except Exception as e:
        logging.debug(e)
        resp_data["code"] = response.ERROR
        resp_data["msg"] = response.RESULT_ERROR
        resp_data["data"] = []
    finally:
        return jsonify(resp_data)



def update_pay_password():
    """
    修改支付密码
    :return:
    """
    logging.info("update_pay_password")
    try:
        old_password = request.get_json().get("old_pwd")
        new_password = request.get_json().get("new_pwd")
        repeat_password = request.get_json().get("re_pwd")
        if new_password != repeat_password:
            return jsonify({"msg": "两次密码输入不一致"})

        have_pay_password = current_user.pay_password
        if have_pay_password:  # 判断是否为新增密码
            password_true = current_user.check_pay_password(old_password)
            if not password_true:
                return jsonify({"msg": "原密码错误"})

        current_user.pay_password = new_password
        return jsonify({"code": response.SUCCESS})

    except Exception as e:
        logging.info(e)
        return jsonify({"code": response.ERROR,
                        'msg': response.RESULT_ERROR})


# method

def get_used_coupons_method(data):
    """
    整理用户已使用的优惠券数据
    :return:
    """
    resp_data = []
    sys_dict = Coupon.get_coupon_type_and_product_type()
    type_dict = {}  # 优惠券类型
    product_dict = {}  # 优惠券范围
    for info in sys_dict:
        if info.dict_type == 'coupon_type':
            type_dict[info.dict_id] = info.dict_name
        if info.dict_type == 'coupon_product_type':
            product_dict[info.dict_id] = info.dict_name

    coupons_obj_dict = {}  # data下所有优惠券信息
    for coupon_obj in data[0].get('coupons'):
        coupons_obj_dict[coupon_obj.get('coupon_code')] = coupon_obj

    for user_coupon in data:
        coupon_code = user_coupon['wallet']['coupons']['coupon_code']
        coupon_obj = coupons_obj_dict[coupon_code]
        if coupon_obj:
            type = type_dict[coupon_obj.get('type')]
            product_type = product_dict[coupon_obj.get('product_type')]
            resp_dict = make_response_coupons_data(coupon_obj, type, product_type)
            resp_data.append(resp_dict)
    return resp_data


def get_coupons(coupon_code_list, coupons):
    """
    整理用户未使用或已过期的优惠券数据
    :param data:
    :return:
    """
    coupon_dict = {}
    for coupon in coupons:
        coupon_dict[coupon.get('coupon_code')] = coupon

    resp_data = []
    for info in coupon_code_list:
        coupon_obj = coupon_dict.get(info)
        if coupon_obj:
            type = coupon_obj.get('type_dict').get('dict_name')
            product_type = coupon_obj.get('product_type').get('dict_name')
            resp_dict = make_response_coupons_data(coupon_obj, type, product_type)
            resp_data.append(resp_dict)
    return resp_data


def make_response_coupons_data(coupon_obj, type, product_type):
    """
    整理优惠券数据
    :param coupon_obj:
    :return:
    """
    r = re.compile('.0$')
    desc = ''
    condition = coupon_obj.get('condition')
    value = coupon_obj.get('value')
    if type == '满减':
        desc = '满{}减{}'.format(r.sub(r'', str(condition)), r.sub(r'', str(value)))
    elif type == '折扣':
        value = float(coupon_obj.get('value')) * 10
        desc = '满{}打{}折'.format(r.sub(r'', str(condition)), r.sub(r'', str(value)))
    start_time = coupon_obj.get('start_time').strftime('%Y/%m/%d')
    end_time = coupon_obj.get('end_time').strftime('%Y/%m/%d')
    resp_dict = {'start_time': start_time,
                 'end_time': end_time,
                 'type': type,
                 'product_type': product_type,
                 'desc': desc,
                 'coupon_code': coupon_obj.get('coupon_code')}
    return resp_dict


def format_recharge_rule(recharge_rule_list):
    """
    格式化返回页面的充值方案信息
    :param recharge_rule_list:
    :return:
    """
    format_recharge_rule_list = []
    for recharge_rule in recharge_rule_list:
        format_recharge_rule_dict = {
            "recharge_rule_id": recharge_rule.recharge_rule_id,
            "org_id": recharge_rule.org_id,
            "rule_name": recharge_rule.rule_name,
            "recharge_condition": recharge_rule.recharge_condition,
            "giving_count": recharge_rule.giving_count,
            "rule_start_time": str(recharge_rule.rule_start_time).split(".")[0][:-9],
            "rule_end_time": str(recharge_rule.rule_end_time).split(".")[0][:-9],
            "remarks": recharge_rule.remarks
        }
        format_recharge_rule_list.append(format_recharge_rule_dict)
    return format_recharge_rule_list


"""积分获取记录开始"""



def get_point_record(org=None):
    """
    根据用户/机构获取积分获取记录
    :return:
    """
    logging.info("get_point_record")
    resp_data = {}
    try:
        params = request.get_json()
        page = params.get('page')
        per_page = params.get('per_page')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        if not org:
            record_obj_list, count = User.get_record_by_user_code(
                user_code=current_user.user_code, start_time=start_time, end_time=end_time,
                page=page, per_page=per_page)
        else:
            record_obj_list, count = Sys_org.get_record_by_org_id(
                org_id=session.get('org_id'), start_time=start_time, end_time=end_time,
                page=page, per_page=per_page)
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


def format_record_info(record_list):
    """
    格式化积分获取记录数据
    :param record_list:
    :return:
    """
    format_record_list = []
    for record_obj in record_list:
        way_type = IntegralRule.get_integral_rule_by_integral_rule_id(
            record_obj.get('wallet').get('point_record').get('way')).integral_rule_type
        format_record_dict = {
            "user_name": record_obj.get('username') if record_obj.get('username') else '',
            "org_name": record_obj.get('org_name') if record_obj.get('org_name') else '',
            "amount": record_obj.get('wallet').get('point_record').get('amount'),
            "org_code": record_obj.get('wallet').get('point_record').get('org_code'),
            "way": SysDict.get_dict_info_by_type_and_id('integral_rule_type', way_type).dict_name,
            'point_sum': record_obj.get('wallet').get('point_record').get('point_sum'),
            "create_time": str(record_obj.get('wallet').get('point_record').get('create_time')).split(".")[
                0] if record_obj.get('wallet').get('point_record').get('create_time') else
            str(record_obj.get('wallet').get('point_record').get('time')).split(".")[0]
        }
        format_record_list.append(format_record_dict)
    return format_record_list


"""积分获取记录结束"""
