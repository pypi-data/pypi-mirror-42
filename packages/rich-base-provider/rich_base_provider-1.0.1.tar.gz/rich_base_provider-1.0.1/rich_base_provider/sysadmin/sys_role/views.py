#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 09：50
# @Author  : shuyi
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function: 角色管理路由接口


import logging
from flask import session, request
from rich_base_provider import response
from rich_base_provider.sysadmin.sys_role.models import Role
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_permission.models import Permissions
from flask import jsonify
from flask_security import current_user



"""
角色管理
"""

def get_role_all():
    """
    根据机构编号、页码获取当前机构、旗下子机构所有角色信息
    :author: chenwanyue
    :return:
    """
    logging.info("get_role_all")
    response_dict = {}
    try:
        params = request.values.to_dict()
        search_data = params.get("search_data")
        if not search_data:
            search_data = ''
        per_page = int(params.get("per_page", "10"))
        page = int(params.get("page", "1")) / per_page + 1
        sort = params.get('sort') if params.get('sort') else 'create_time'
        sortOrder = params.get('sortOrder')
        if sortOrder == 'desc':
            sortOrder = -1
        elif sortOrder == 'asc':
            sortOrder = 1
        # 获取当前登录的org_code
        org_code = session.get("org_code", None)
        if not org_code:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "当前机构编号不存在"
            response_dict["data"] = []
        else:
            # 根据页码=获取全部机构的全部角色信息
            role_list_page = Role.get_role_by_org(org_code, search_data, page, per_page, sort, sortOrder)
            role_response_list = []
            for role_obj in role_list_page["user_list"]:
                # 将角色信息根据机构编号进行归类
                role = {}
                role["name"] = role_obj["name"]
                role["role_code"] = role_obj["role_code"]
                role["description"] = role_obj["description"]
                role["role_status"] = Role.status_dict[role_obj["role_status"]]
                role["org_code"] = role_obj["org_code"]
                role["org_for"] = role_obj["sys_org"]["org_name"]
                role_response_list.append(role)

            role_response_list = role_response_list
            return jsonify({'total': role_list_page["count"], 'rows': role_response_list})
    except Exception as e:
        logging.debug(e)
        return jsonify({'total': 0, 'rows': []})


def insert_role():
    """
    根据机构编号、用户名、角色基本信息添加角色
    :return:
    """
    logging.info("insert_role")
    response_dict = {}
    try:
        # 获取机构编号(登录的机构编号)
        login_org_code = session.get("org_code", None)
        if not login_org_code:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "当前机构编号不存在"
            response_dict["data"] = []
        else:
            # 获取角色基本信息
            params = request.get_json()
            role_name = params.get("role_name")
            org_code = params.get("org_code")  # 获取该角色创建所属机构编号
            role_obj = Role.judge_role_name(org_code, role_name)
            if role_obj:
                response_dict["code"] = response.ERROR
                response_dict["msg"] = "该角色名称已存在"
                response_dict["data"] = []
            else:
                role_desc = params.get("role_desc", "")
                # 创建角色编号
                new_role_code = Role.create_role_code(org_code)
                role_status = params.get("role_status")

                create_dict = {
                    "org_code": org_code,
                    "role_name": role_name,
                    "role_desc": role_desc,
                    "role_code": new_role_code,
                    'role_status': role_status
                }
                # 添加角色
                Role.insert_role(create_dict)
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


def delete_role():
    """
    根据机构编号、角色编号删除角色
    :return:
    """
    logging.info("delete_role")
    response_dict = {}
    try:
        # 获取机构编号(登录的机构编号)
        login_org_code = session.get("org_code")
        login_role_code = session.get("role_code")

        role_code = request.get_json().get("role_code")
        if role_code in login_role_code:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "自己角色不可以删除"
            response_dict["data"] = []

        elif role_code[len(login_org_code):] == "-0001":
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "本机构管理员不可删除"
            response_dict["data"] = []

        else:
            user_list = User.get_info_by_org_role_code(role_code)
            if user_list:
                response_dict["code"] = response.ERROR
                response_dict["msg"] = '当前角色正在使用中，无法删除！'
                response_dict["data"] = []
            else:
                Role.delete_role(role_code)
                # 将此角色从原先的权限引用中删除
                Permissions.delete_permission_roles(role_code)

                logging.info(user_list)

                for user in user_list:
                    logging.info(user)
                    user.delete_role_and_org(role_code)  # 将绑定该角色的用户该角色解除

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


def get_role_info():
    """
    根据角色编号获取本角色具体信息
    :return:
    """
    logging.info("get_role_info")
    response_dict = {}
    try:
        # 获取机构编号(当前登录机构)
        login_org_code = session.get("org_code", None)
        if not login_org_code:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "当前机构编号不存在"
            response_dict["data"] = []
        else:
            params = request.get_json()
            role_code = params.get("role_code")
            role_obj = Role.get_role_info(role_code)

            org_name = Sys_org.get_org_info(role_obj.org_code).org_name

            if role_obj:
                response_dict["code"] = response.SUCCESS
                response_dict["msg"] = response.RESULT_SUCCESS
                response_dict["data"] = {"role_code": role_obj.role_code,
                                         "org_code": role_obj.org_code,
                                         "org_name": org_name,
                                         "role_name": role_obj.name,
                                         "role_desc": role_obj.description,
                                         "role_status": role_obj.role_status,
                                         }
            else:
                response_dict["code"] = response.ERROR
                response_dict["msg"] = response.RESULT_ERROR
                response_dict["data"] = []

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def update_role():
    """
    根据机构编号、用户名、角色基本信息编辑角色
    :return:
    """
    logging.info("update_role")
    response_dict = {}
    try:
        # 获取要更改角色信息
        params = request.get_json()
        old_org_code = params.get("old_org_code")
        org_code = params.get("org_code")
        role_code = params.get("role_code")
        role_name = params.get("role_name")
        role_desc = params.get("role_desc")
        role_status = params.get("role_status")

        new_info = {
            "old_org_code": old_org_code,
            "org_code": org_code,
            "role_code": role_code,
            "new_role_code": role_code,
            "role_name": role_name,
            "role_desc": role_desc,
            "role_status": role_status
        }
        # 编辑角色
        if old_org_code == org_code:
            Role.update_role_info(new_info)
        else:
            new_role_code = Role.create_role_code(org_code)  # 当前角色所属机构被更改时
            new_info["new_role_code"] = new_role_code
            Role.update_role_info(new_info)
            new_old_org = org_code
            old_role_code = role_code
            user_org_role_list = User.get_info_by_org_role_code(role_code)
            for org_role in user_org_role_list:
                org_role.update_role_and_org(old_role_code, new_role_code, new_old_org)  # 同步更新当前角色用户角色信息

            Permissions.update_permission_roles_info(old_role_code, new_role_code)  # 同步更新权限角色权限信息

        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = []

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = "查找不到该角色"
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def get_permissions():
    """
    通过角色id获取权限信息
    :return:
    """
    logging.info("get_permissions_by_role_code")
    response_dict = {}
    try:
        params = request.get_json()
        role_code = params.get("role_code")
        permissions_obj_list = Permissions.get_permissions_by_role(role_code)  # 该角色已有权限对象
        permissions_all_obj_list = Permissions.get_permissions_all()  # 所有菜单，限制权限对象
        permissions_list = []
        permissions_all_list = []
        for perm in permissions_obj_list:
            _dict = {}
            _dict["id"] = perm.permission_id
            _dict["text"] = perm.permission_name
            _dict["parent_id"] =perm.parent_id
            permissions_list.append(_dict)

        for each in permissions_all_obj_list:
            _dict = {}
            _dict["id"] = each.permission_id
            _dict["text"] = each.permission_name
            if each.parent_id=='-1':
                _dict["parent_id"] = '0'
            else:
                _dict["parent_id"] = each.parent_id

            permissions_all_list.append(_dict)

        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        response_dict["data"] = {'permissions_list': permissions_list,
                                 'permissions_all_list': permissions_all_list}

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def update_permissions():
    """
    根据角色id 更改角色权限
    :return:
    """
    logging.info("update_permissions")
    response_dict = {}
    try:
        # 获取要更改角色信息
        params = request.get_json()
        role_code = params.get("role_code")
        role_name = params.get("role_name")
        role_desc = params.get("role_desc")
        role_status = params.get("role_status")
        new_info = {
            "role_code": role_code,
            "role_name": role_name,
            "role_desc": role_desc,
            "role_status": role_status
        }
        Role.update_role_info_by_role_code(new_info)
        new_permissions_list = request.get_json().get("permissions_list")
        user = current_user.user_code
        permissions_obj_list = Permissions.get_permissions_by_role(role_code)  # 改角色未修改前权限
        old_permissions_list = []
        for parm in permissions_obj_list:
            old_permissions_list.append(parm.permission_id)

        update_permissions_list = list(set(new_permissions_list) ^ set(old_permissions_list))  # 需要修改的权限列表

        add_list = []  # 要给角色添加权限的列表
        delete_list = []  # 要给角色删除的权限列表

        for each in update_permissions_list:
            if each in old_permissions_list:
                delete_list.append(each)
            else:
                add_list.append(each)

        if delete_list:
            Permissions.delete_role_by_permission_id(delete_list, role_code, user)

        if add_list:
            Permissions.add_role_by_permission_id(add_list, role_code, user)

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
