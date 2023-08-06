#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 15:15
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function:

import logging,datetime
from flask import session, jsonify, request
from flask_security import current_user
from rich_base_provider import response
from rich_base_provider.sysadmin.sys_role.models import Role
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.coupon.models import Coupon
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_dict.models import SysDict
role_type = "2"
user_type = "3"


def get_coupons():
    """
    获取当前机构及子机构的优惠券
    :return:
    """
    logging.info('get_coupons')
    res_json = {}
    try:
        params = request.get_json()
        org_code = session.get('org_code')
        page = params.get('page')
        per_page = params.get('per_page')
        search_data = params.get('search_data', '')
        coupons = Coupon.query_coupons_by_org_code(org_code, search_data, page, per_page)
        data = []

        for coupon in coupons:
            info = {'sys_name': coupon['sys_org']['org_name'],
                    'coupon_code': coupon.get('coupon_code'),
                    'title': coupon.get('title'),
                    'type': coupon['type_dict']['dict_name'],
                    'start_time': coupon.get('start_time').strftime('%F %H:%M:%S'),
                    'end_time': coupon.get('end_time').strftime('%F %H:%M:%S'),
                    'status': coupon['status_dict']['dict_name']}
            data.append(info)
        if data and int(page) == 1:
            count = Coupon.get_coupon_count(org_code, search_data)
            res_json['count'] = count
        elif not data:
            res_json['count'] = 0
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def add_coupon():
    """
    添加优惠券
    :return:
    """
    logging.info('add_coupon')
    res_json = {}
    try:
        params = request.get_json()
        create_by = current_user.user_code
        update_by = create_by
        start_time = datetime.datetime.strptime(params.get('start_time'), '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(params.get('end_time'), '%Y-%m-%d %H:%M:%S')

        if end_time > start_time:
            yesterday = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
            if start_time > yesterday:
                Coupon.create(create_by=create_by, update_by=update_by, **params)
                res_json['code'] = response.SUCCESS
                res_json['msg'] = response.RESULT_SUCCESS
                res_json['data'] = []
            else:
                res_json["code"] = response.ERROR
                res_json["msg"] = '优惠券开始时间至少从今天开始'
                res_json["data"] = []
        else:
            res_json["code"] = response.ERROR
            res_json["msg"] = '优惠券结束时间必须大于开始时间'
            res_json["data"] = []

    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def update_coupon():
    """
    更新优惠券
    :return:
    """
    logging.info('update_coupon')
    res_json = {}
    try:
        params = request.get_json()
        coupon_code = params.get('coupon_code')
        coupon = Coupon.get_coupon_obj_by_coupon_code(coupon_code)
        update_by = current_user.user_code
        logging.info(coupon)
        coupon.edit_coupon(update_by=update_by, **params)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = []
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_coupon_info():
    """
    获取优惠券信息
    :return:
    """
    logging.info('get_coupon_info')
    res_json = {}
    try:
        params = request.get_json()
        coupon_code = params.get('coupon_code')
        coupon = Coupon.get_coupon_info_update(coupon_code)
        select_info = Coupon.get_status_product_user_type()

        target_list = []
        if coupon["user_type"] == role_type:
            obj_list = Role.get_role_list_by_code(coupon["target_user"])
            for each in obj_list:
                target_list.append(dict(id=each.role_code, name=each.name))

        if coupon["user_type"] == user_type:
            obj_list = User.get_user_by_code_list(coupon["target_user"])
            for each in obj_list:
                target_list.append(dict(id=each.user_code, name=each.username))
        send_num = coupon.get('send_num')
        coupon_info = dict(org_id=coupon["org_id"],
                           org_name=coupon["sys_org"]["org_name"],
                           title=coupon["title"],
                           content=coupon["content"],
                           type=coupon["type"],
                           condition=coupon["condition"],
                           value=coupon["value"],
                           start_time=coupon["start_time"].strftime('%Y-%m-%d'),
                           end_time=coupon["end_time"].strftime('%Y-%m-%d'),
                           product_type=coupon["product_type"],
                           target_product=coupon["target_product"],
                           user_type=coupon["user_type"],
                           target_user=coupon["target_user"],
                           target_list=target_list,
                           status=coupon["status"],
                           is_edit=True,
                           coupon_num=coupon["coupon_num"],
                           send_num=send_num
                           )

        if send_num > 0:
            coupon_info['is_edit'] = False
        data = dict(select_info=select_info,
                    coupon_info=coupon_info)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_select():
    """
    渲染编辑页面相关选择框---商品对象，用户对象，状态
    :return:
    """
    logging.info('get_select')
    res_json = {}
    try:
        data = Coupon.get_status_product_user_type()

        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_user_by_org_id(org_id):
    """
    通过机构获取用户
    :return:
    """
    logging.info('get_user_by_role_code')
    res_json = {}
    try:
        params = request.args
        page = params.get('page')
        keyword = params.get("name", "")
        data = User.get_select_users_by_org_id(org_id, keyword, page)
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


def get_role_by_org_id(org_id):
    """
    通过机构获取角色
    :return:
    """
    logging.info('get_user_by_role_code')
    res_json = {}
    try:
        params = request.args
        if org_id == 'null':
            org_id = params.get('org_id')
        page = params.get('page')
        keyword = params.get("name", "")
        data = Role.get_role_dict_by_org_id(org_id, keyword, page)
        count = data["count"]
        result = data["role_list"]

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


def get_classify_by_org_id(org_id):
    """
    通过机构获取角色
    :return:
    """
    logging.info('get_classify_by_org_id')
    res_json = {}
    try:
        params = request.args
        if org_id != 'null':
            page = params.get('page')
            keyword = params.get("name", "")
            base_result = []
            if int(page) ==1:
                base_data = SysDict.get_dict_list_by_type('product_classify')
                for info in base_data:
                    base_result.append(dict(classify_id=info.dict_id, name=info.dict_name))
            data = list(ProductClassify.get_product_classify_list_by_data(current_org_id=org_id, page=page, search_data=keyword))
            result = []
            for info in data:
                result.append(dict(classify_id=info.get('classify_id'), name=info.get('classify_name')))
            if len(result) ==20:
                res_json['more'] = True
            result = base_result+result
            res_json['code'] = response.SUCCESS
            res_json['msg'] = response.RESULT_SUCCESS
            res_json['data'] = result

    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_users_by_org_id():
    """
    通过机构获取用户
    :return:
    """
    logging.info('get_users_by_org_id')
    res_json = {}
    try:
        params = request.get_json()
        org_id = params.get('org_id')
        search_data = params.get('search_data', '')
        page = params.get('page')
        per_page = params.get('per_page')
        users = User.get_users_by_org_id(org_id, search_data, page, per_page)
        data = []
        for user in users:
            info = dict(user_code=user.get('user_code'),
                        username=user.get('username'),
                        mobile=user['account']['mobile'],
                        org_name=user['sys_org']['org_name'])
            data.append(info)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_son_orgs_by_org_id():
    """
    通过机构id获取子机构信息
    :return:
    """
    logging.info("get_son_orgs_by_org_id")
    res_json = {}
    try:
        params = request.get_json()
        org_id = params.get('org_id')
        search_data = params.get('search_data', '')
        page = params.get('page')
        per_page = params.get('per_page')
        org_code = Sys_org.get_org_info_by_org_id(org_id).org_code
        orgs = Sys_org.get_sys_son_orgs(org_code, search_data, page, per_page)
        data = []
        for org in orgs:
            info = dict(org_code=org['org_code'],
                        org_name=org['org_name'],
                        mobile=org["mobile"],
                        org_id=org["org_id"])
            data.append(info)
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def check_edit():
    """
    验证当前优惠券是否可以修改（验证条件：优惠券已发放）
    :return:
    """
    logging.info('check_edit')
    res_json = {}
    try:
        data = {'is_edit': True}
        params = request.get_json()
        coupon_code = params.get('coupon_code')
        send_num = Coupon.coupon_send_num(coupon_code)
        if send_num > 0:
            data = {'is_edit': False}

        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = data
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def delete_coupon():
    """
    删除优惠券
    :return:
    """
    logging.info('delete_coupon')
    res_json = {}
    try:
        params = request.get_json()
        coupon_code = params.get('coupon_code')
        send_num = Coupon.coupon_send_num(coupon_code)
        if send_num == 0:
            bool_data = Coupon.delete_by_coupon_code(coupon_code)
            if bool_data:
                res_json['code'] = response.SUCCESS
                res_json['msg'] = response.RESULT_SUCCESS
                res_json['data'] = []
            else:
                res_json['code'] = response.ERROR
                res_json['msg'] = '优惠删除失败'
                res_json['data'] = []
        else:
            res_json['code'] = response.ERROR
            res_json['msg'] = '优惠已生效，不能修改'
            res_json['data'] = []

    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def send_coupon_users():
    """
    发放优惠券
    :return:
    """
    logging.info('send_coupon_users')
    res_json = {}
    try:
        parmas = request.get_json()
        org_id = session.get('org_id')
        coupon_code = parmas.get('coupon_code')
        users_code = parmas.get('users_code')
        bool_data = Coupon.send_coupon_to_users(org_id, coupon_code, users_code)
        if bool_data:
            res_json['code'] = response.SUCCESS
            res_json['msg'] = response.RESULT_SUCCESS
            res_json['data'] = []
        else:
            res_json["code"] = response.ERROR
            res_json["msg"] = '发放失败'
            res_json["data"] = []
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def send_coupon_orgs():
    """
    发放优惠券
    :return:
    """
    logging.info('send_coupon_orgs')
    res_json = {}
    try:
        parmas = request.get_json()
        org_id = session.get('org_id')
        coupon_code = parmas.get('coupon_code')
        orgs_code = parmas.get('orgs_code')
        bool_data = Coupon.send_coupon_to_orgs(org_id, coupon_code, orgs_code)
        if bool_data:
            res_json['code'] = response.SUCCESS
            res_json['msg'] = response.RESULT_SUCCESS
            res_json['data'] = []
        else:
            res_json["code"] = response.ERROR
            res_json["msg"] = '发放失败'
            res_json["data"] = []
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def get_statistics_coupon_info():
    """
    获取优惠券统计时优惠券信息
    :return:
    """
    logging.info("get_statistics_coupon_info")
    res_json = {}
    try:
        params = request.get_json()
        coupon_code = params.get('coupon_code')
        coupon = Coupon.get_coupon_info(coupon_code)
        coupon_type = coupon["type_dict"]["dict_name"]
        product_type = coupon["product_type"]["dict_name"]
        start_time = coupon["start_time"].strftime('%Y/%m/%d')  # 优惠券使用开始时间
        end_time = coupon["end_time"].strftime('%Y/%m/%d')  # 优惠券使用结束时间
        condition = coupon["condition"]  # 优惠券使用条件
        value = coupon["value"]  # 优惠力度

        coupon_info = dict(
            coupon_type=coupon_type,
            product_type=product_type,
            condition=condition,
            value=value,
            start_time=start_time,
            end_time=end_time,
        )
        res_json['code'] = response.SUCCESS
        res_json['msg'] = response.RESULT_SUCCESS
        res_json['data'] = coupon_info
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def user_use_coupon():
    """
    用户使用优惠券
    :return:
    """
    logging.info('use_coupon')
    res_json = {}
    try:
        params = request.get_json()
        record_id = params.get('record_id')
        order_id = params.get('order_id')
        user_code = current_user.user_code
        bool_data = User.use_coupon(user_code, record_id, order_id)
        if bool_data:
            res_json['code'] = response.SUCCESS
            res_json['msg'] = response.RESULT_SUCCESS
            res_json['data'] = []
        else:
            res_json["code"] = response.ERROR
            res_json["msg"] = '使用失败'
            res_json["data"] = []
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)


def org_use_coupon():
    """
    机构使用优惠券
    :return:
    """
    logging.info('use_coupon')
    res_json = {}
    try:
        params = request.get_json()
        record_id = params.get('record_id')
        order_id = params.get('order_id')
        org_code = session.get('org_code')
        bool_data = Sys_org.use_coupon(org_code, record_id, order_id)
        if bool_data:
            res_json['code'] = response.SUCCESS
            res_json['msg'] = response.RESULT_SUCCESS
            res_json['data'] = []
        else:
            res_json["code"] = response.ERROR
            res_json["msg"] = '使用失败'
            res_json["data"] = []
    except Exception as e:
        logging.debug(e)
        res_json["code"] = response.ERROR
        res_json["msg"] = response.RESULT_ERROR
        res_json["data"] = []
    finally:
        return jsonify(res_json)
