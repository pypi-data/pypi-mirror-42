#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 18-10-26
# @Author    : zbh
# @File      : views
# @Software  : Rich Web Platform
# @Functions
import logging

import re
from flask import jsonify,  request, session

from rich_base_provider import response
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_user_relations.models import User_relations

from flask_security import current_user


def detail_info():
    """
    商业好友个人详情信息
    :return:
    """
    logging.info('detail_info')
    # 当前用户编码
    current_user_code = current_user.user_code
    try:
        params = request.get_json()
        friend_user_code = params.get('friend_user_code')
        # 通过当前用户user_code和商业好友的user_code查询好友个人详情信息
        detail_info = User_relations.get_detail_info(current_user_code=current_user_code, friend_user_code=friend_user_code)
        return jsonify({"code": response.SUCCESS, "detail_info": detail_info})

    except Exception as e:
        logging.debug(e)
        raise e


def edit_userinfo():
    """
    编辑商业好友信息
    :return:
    """
    logging.info('edit_userinfo')
    # 当前用户编码
    user_code = current_user.user_code
    try:
        params = request.get_json()
        username = params.get('username')
        org_name = params.get('org_name')
        nickname = params.get('nickname')
        relation_type = params.get('relation_type')
        pay_type = params.get('pay_type')
        is_share = int(params.get('is_share'))

        # 获取待编辑好友的机构信息
        org_info = Sys_org.get_org_info_by_org_name(org_name=org_name)
        # 待编辑好友的机构id
        org_id = org_info.org_id

        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, username)
        # 判断用户输入的联系人是用户名还是手机号
        if res:
            # 待编辑用户
            user = User.objects(account__mobile=username).first()
        else:
            # 待编辑用户
            user = User.objects(username=username).first()

        relation = User_relations.create_user_relation(user_code=user.user_code,org_id=org_id,nickname=nickname,relation_type=relation_type,pay_type=pay_type,is_share=is_share)

        # 更新好友数据
        User_relations.update_user_relations(user_code=user_code, friend_user_code=user.user_code, relation=relation)

        return jsonify({"msg": response.RESULT_SUCCESS, "code": response.SUCCESS})

    except Exception as e:
        logging.debug(e)
        return jsonify({"msg": response.RESULT_ERROR, "code": response.ERROR})


def org_of_user():
    """
    获取待添加好友所属的所有机构
    :return:

    """
    logging.info('org_of_user')

    try:
        params = request.get_json()
        username = params.get('username')  # 联系人信息可能为:用户名/手机号
        # 判断用户输入的联系人是用户名还是手机号
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, username)
        if res:
            # 待添加用户
            user = User.objects(account__mobile=username).first()
        else:
            # 待添加用户
            user = User.objects(username=username).first()
        if user:
            # 获取用户所属的所有机构并返回
            org_role = user.org_role
            org_code_list = []
            org_name_list = []
            for org_r in org_role:
                org_code = org_r['org_code']
                org_code_list.append(org_code)
            for org_code in org_code_list:
                org_obj = Sys_org.get_org_info(org_code)
                org_name_list.append(org_obj.org_name)

            return jsonify({"msg": response.RESULT_SUCCESS, "code": response.SUCCESS, "org_name_list": org_name_list})

        else:
            # 待添加好友不存在于本系统
            return jsonify({"msg": '您所添加的好友不是本平台用户，请分享注册链接给你的好友！', "code": response.ERROR})

    except Exception as e:
        logging.debug(e)
        return jsonify({"msg": response.RESULT_ERROR, "code": response.ERROR})


def add_relation():
    """
    添加用户关系
    :return:
    """
    logging.info("add_relation")
    # 当前用户编码
    user_code = current_user.user_code
    # 当前用户所属机构编码
    current_user_org_id = session.get('org_id')

    try:
        params = request.get_json()
        username = params.get('username')  # 联系人信息可能为:用户名/手机号
        org_name = params.get('org_name')
        nickname = params.get('nickname')
        relation_type = params.get('relation_type')
        pay_type = params.get('pay_type')
        is_share = params.get('is_share', 0)

        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, username)
        # 判断用户输入的联系人是用户名还是手机号
        if res:
            # 待添加用户
            user = User.objects(account__mobile=username).first()
        else:
            # 待添加用户
            user = User.objects(username=username).first()

        # 待添加用户的编码
        u_code = user.user_code
        # 获取待添加好友的机构信息
        org_info = Sys_org.get_org_info_by_org_name(org_name=org_name)
        # 待添加好友的机构id
        org_id = org_info.org_id

        # 判断用户关系表中是否已经有当前用户，有则直接添加关系，没有则添加用户及关系
        user_rel = User_relations.get_user_relation_by_user_code(user_code=user_code)
        if user_rel is not None:
            for u_rel in user_rel.user_relations:
                if u_rel['user_code'] == u_code:
                    # 已添加过该好友
                    return jsonify({"msg": response.RESULT_EXIST_ERROR, "code": response.ERROR})

            relation = user_rel.create_user_relation(user_code=u_code, org_id=org_id, nickname=nickname, relation_type=relation_type, pay_type=pay_type, is_share=is_share)
            user_rel.user_relations.append(relation)
            user_rel.save()
        else:
            user_relation = User_relations(
                user_code=user_code,
                org_id=current_user_org_id
            )
            relation = user_relation.create_user_relation(user_code=u_code, org_id=org_id, nickname=nickname, relation_type=relation_type, pay_type=pay_type, is_share=is_share)
            user_relation.user_relations.append(relation)
            user_relation.save()

        return jsonify({"msg": response.RESULT_SUCCESS, "code": response.SUCCESS})

    except Exception as e:
        logging.debug(e)
        return jsonify({"msg": response.RESULT_ERROR, "code": response.ERROR})


def get_relation_list():
    """
    查询用户所有商业好友
    :return:
    """
    logging.info("get_relation_list")
    try:
        params = request.get_json()
        search_data = params.get("search_data")
        page = params.get("page", 1)
        per_page = params.get("per_page", 8)

        # 获取当前登录用户的user_code
        u_code = current_user.user_code
        if not u_code:
            return jsonify({"msg": '当前用户编号不存在', "code": response.ERROR})
        else:
            # 根据页码信息获取用户的全部商业好友
            u_rel = User_relations.objects(user_code=u_code).first()
            if u_rel:
                # 用户所有商业好友列表

                user_list_page = User_relations.get_user_relation(u_code, search_data, page, per_page)
                user_list = user_list_page['user_list']
                count = user_list_page['count']
                return jsonify({"msg": response.RESULT_SUCCESS, "code": response.SUCCESS, "lists": user_list, "count": count})

            else:
                # 尚未添加商业好友
                return jsonify({"msg": '尚未添加商业好友', "code": response.ERROR})

    except Exception as e:
        logging.debug(e)
        return jsonify({"msg": response.RESULT_ERROR, "code": response.ERROR})

