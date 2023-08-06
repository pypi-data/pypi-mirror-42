#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/20 09：50
# @Author  : chenwanyue
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function: 权限管理路由接口

import json
import datetime
from flask import session, request, jsonify
from rich_base_provider.sysadmin.sys_permission.models import *
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider import response

from rich_base_provider.sysadmin.sys_role.models import Role

"""
权限管理
"""


def get_perm_all():
    """
    根据角色编号，获取属于此角色的权限
    :return:
    """
    logging.info("get_perm_all")
    response_dict = {}
    try:
        params = request.values.to_dict()
        per_page = int(params.get("per_page", "10"))
        page = int(params.get("page", "1")) / per_page + 1
        sort = params.get('sort') if params.get('sort') else 'create_time'
        sortOrder = params.get('sortOrder')
        if sortOrder == 'desc':
            sortOrder = '-'
        elif sortOrder == 'asc':
            sortOrder = ''

        # 获取查询字段
        search_data = params.get("search_data")
        if not search_data:
            search_data = ''
        # 根据页码以及角色编号获取本角色在此机构所有权限
        perm_list_page, data_count = Permissions.find_perm_list(session.get("role_code"), page, per_page, search_data, sort, sortOrder)
        # 存储返回的权限信息
        perm_response_list = format_permission_info(perm_list_page)
        # 封装返回页面数据信息
        return jsonify({'rows': perm_response_list, 'total': data_count})
    except Exception as e:
        logging.debug(e)
        return jsonify({'rows': [], 'total': 0})



def delete_perm():
    """
    根据权限编号对某权限进行删除 只有权限创建者以及父机构admin可以对此权限进行删除
    :return:
    """
    logging.info("delete_role")
    response_dict = {}
    try:
        params = request.get_json()
        permission_id = params.get("permission_id")
        flag = Permissions.delete_perm(permission_id, datetime.datetime.now())
        response_dict["data"] = []
        if flag == "-1":
            response_dict["code"] = response.ERROR
            response_dict["msg"] = "当前权限编号错误"
        else:
            # 级联删除
            cascade_delete_perm(params.get("permission_id"))
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
        # 更新菜单
        session['menu'] = get_user_menu(session.get("role_code"))

    except Exception as e:
        logging.debug(e)
        response_dict["data"] = []
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR

    finally:
        return jsonify(response_dict)


def get_child_perm():
    """
    根据父权限编号查询子权限信息
    :return:
    """
    logging.info("get_child_perm")
    response_dict = {}
    try:
        # 获取操作权限基本信息
        params = request.get_json()
        # 获取parent_id 默认为-1
        parent_id = params.get("parent_id", "-1")
        # 获取当前用户角色编号
        perm_child_list = Permissions.get_child_perm(session.get("role_code"), parent_id)
        if len(perm_child_list) == 0:
            response_dict["code"] = response.PARAMETER_ERROR
            response_dict["msg"] = "权限编号错误"
            response_dict["data"] = []
        else:
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
            response_dict["data"] = perm_child_list

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def insert_perm():
    """
    根据机构编号、权限基本信息新增操作权限
    :return:
    """
    logging.info("insert_perm")
    response_dict = {}
    try:
        # 获取机构编号
        login_org_code = session.get("org_code")
        # 获取操作权限基本信息
        params = request.get_json()
        permission_name = params.get("permission_name")
        url = params.get("url")
        permission_type = params.get("permission_type")
        parent_id = params.get("parent_id")
        desc = params.get("desc")
        status = params.get("status")
        icon = params.get("icon")
        sort = params.get("sort")
        # 计算新增权限perm_id
        permission_id = create_perm_id(str(parent_id))
        # 验证数据是否重复
        permission_obj = Permissions.get_perm_sub_info(url, permission_name)
        # 根据当前权限名称-权限路径获取权限对象
        response_dict["data"] = []

        if permission_obj:
            if permission_obj.permission_name == permission_name:
                # 权限名称相同 判断此权限是否为更新权限自身
                if permission_obj.permission_id != permission_id:
                    response_dict["code"] = response.PARAMETER_ERROR
                    response_dict["msg"] = "当前权限名称已存在"
                    return jsonify(response_dict)
            if permission_obj.url == url:
                # 权限URL相同 判断此权限是否为更新权限自身
                if permission_obj.permission_id != permission_id:
                    response_dict["code"] = response.PARAMETER_ERROR
                    response_dict["msg"] = "当前请求URL已存在"
                    return jsonify(response_dict)

        create_dict = {
            "permission_id": permission_id,
            "permission_name": permission_name,
            "url": url,
            "permission_type": permission_type,
            "parent_id": parent_id,
            "desc": desc,
            "status": status,
            "icon": icon,
            "sort": sort,
            "roles": [],
            "login_org_code": login_org_code
        }
        # 添加权限
        Permissions.insert_perm(create_dict)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        # 更新菜单
        session['menu'] = get_user_menu(session.get("role_code"))

    except Exception as e:
        logging.exception(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []
    finally:
        return jsonify(response_dict)


def get_perm_info():
    """
    根据权限编号获取本权限具体信息
    :return:
    """
    logging.info("get_perm_info")
    response_dict = {}
    try:
        # 获取操作权限基本信息
        params = request.get_json()
        permission_id = params.get("permission_id")
        center_parent_name = params.get("center_parent_name")
        if center_parent_name:
            center_parent_name_list = center_parent_name.split("-")
            parent_obj_list = Permissions.get_perm_sub_info_by_name(session.get("role_code"),
                                                                    center_parent_name_list)
            response_dict["parent_obj_list"] = parent_obj_list
        perm_info = Permissions.get_perm_info(permission_id)
        if perm_info:
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
            response_dict["data"] = {"perm_info": perm_info}
        else:
            response_dict["code"] = response.ERROR
            response_dict["msg"] = response.RESULT_ERROR
            response_dict["data"] = {}

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def update_perm():
    """
    根据机构编号、权限基本信息更新操作权限
    :return:
    """
    logging.info("update_perm")
    response_dict = {}
    try:
        # 获取当前登录机构编号
        login_org_code = session.get("org_code")
        # 获取操作权限基本信息
        params = request.get_json()
        permission_id = params.get("permission_id")
        permission_name = params.get("permission_name")
        url = params.get("url")
        permission_type = params.get("permission_type")
        desc = params.get("desc")
        status = params.get("status")
        icon = params.get("icon")
        sort = params.get("sort")
        parent_id = params.get("parent_id")

        # 验证数据是否重复
        permission_obj = Permissions.get_perm_sub_info(url, permission_name)
        # 根据当前权限名称-权限路径获取权限对象
        response_dict["data"] = []

        if permission_obj:
            if permission_obj.permission_name == permission_name:
                # 权限名称相同 判断此权限是否为更新权限自身
                if permission_obj.permission_id != permission_id:
                    response_dict["code"] = response.PARAMETER_ERROR
                    response_dict["msg"] = "当前权限名称已存在"
                    return jsonify(response_dict)
            if permission_obj.url == url:
                # 权限URL相同 判断此权限是否为更新权限自身
                if permission_obj.permission_id != permission_id:
                    response_dict["code"] = response.PARAMETER_ERROR
                    response_dict["msg"] = "当前请求URL已存在"
                    return jsonify(response_dict)

        update_dict = {
            "permission_id": permission_id,
            "permission_name": permission_name,
            "url": url,
            "permission_type": permission_type,
            "desc": desc,
            "status": status,
            "icon": icon,
            "sort": sort,
            "parent_id": parent_id,
            "login_org_code": login_org_code
        }
        # 更新权限基本信息
        Permissions.update_perm(update_dict)
        response_dict["code"] = response.SUCCESS
        response_dict["msg"] = response.RESULT_SUCCESS
        # 更新菜单
        session['menu'] = get_user_menu(session.get("role_code"))

    except Exception as e:
        logging.debug(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)


def find_permission_update_page(permission_id):
    """
    返回更新权限页面
    :return:
    """
    # 查询本机构所有一级菜单权限
    perm_grade_one_list = Permissions.get_child_perm(session.get("role_code"), "-1")
    # 根据权限编号查询本权限具体信息
    perm_obj = Permissions.get_perm_info(permission_id)
    parent_id = perm_obj.parent_id
    permission_name = perm_obj.permission_name
    parent_permission_list = [perm_obj, ]
    while parent_id != "-1":
        parent_obj = Permissions.get_perm_info(parent_id)
        if parent_obj:
            parent_permission_list.append(parent_obj)
            parent_id = parent_obj.parent_id
        else:
            break
    parent_permission_list.reverse()
    # 返回中间层级权限名称a
    center_parent_name = ""
    # 根据当前登录角色编号以及权限名称获取权限ID
    if len(parent_permission_list) <= 2:
        grade_one_name = parent_permission_list[0].permission_name
    else:
        grade_one_name = parent_permission_list[0].permission_name
        for index, parent_obj in enumerate(parent_permission_list):
            if index == 0 or index == (len(parent_permission_list) - 1):
                continue
            else:
                center_parent_name = center_parent_name + parent_obj.permission_name + "-"

    return permission_id, permission_name,grade_one_name,perm_grade_one_list,center_parent_name,


def create_perm_id(parent_id):
    """
    创建权限ID
    规则: parent_id + 自增字段
    对于一级菜单：parent_id = -1 规则中parent_id为空
    :return:
    """
    # 用于存储新生成的权限ID
    create_new_id = ""
    # 获取当前同级权限最新的perm_id
    new_perm_id = Permissions.get_perm_id_new(parent_id)
    # 从字典表中获取初始权限ID字段（根据dict_type + dict_id 唯一获取）
    dict_obj = SysDict.get_dict_info_by_type_and_id("permission_code", "1")
    dict_data = dict_obj.description
    if new_perm_id == "0":
        # 当前没有同级权限，本次添加为首次增加
        # 判断是否为一级权限
        if parent_id == "-1":
            create_new_id = dict_data
        else:
            create_new_id = parent_id + dict_data
    else:
        # 已拥有同级权限
        # 截取自增字段 计算出当前权限perm_id
        count_perm_id = str(int(new_perm_id[-3:]) + 1)
        # 一级权限
        if parent_id == "-1":
            create_new_id = count_perm_id.zfill(3)
        else:
            create_new_id = parent_id + count_perm_id.zfill(3)
    # 判断此权限ID是否存在 若存在 则在原来的基础上+1 再次确认
    while True:
        exist_flag = Permissions.get_perm_info(create_new_id)
        if exist_flag:
            count_create_new_id = str(int(create_new_id[-3:]) + 1)
            create_new_id = create_new_id[:-3] + count_create_new_id.zfill(3)
        else:
            break
    return create_new_id


def perm_classify_tree(permission_list, parent_id):
    """
    递归对权限进行分类 返回树形结构数据
    :param permission_list:
    :param parent_id
    :return:
    """
    perm_tree_list = []
    perm_tree_node_list = []
    for perm_obj in permission_list:
        if perm_obj["parent_id"] == parent_id:
            perm_tree_node = {
                "permission_id": perm_obj["permission_id"],
                "permission_name": perm_obj["permission_name"],
                "url": perm_obj["url"],
                "icon": perm_obj["icon"],
                "permission_type": perm_obj["permission_type"],
                "parent_id": perm_obj["parent_id"],
                "desc": perm_obj["desc"]
            }
            child_list = perm_classify_tree(permission_list, perm_obj["permission_id"])
            perm_tree_node["child_perms"] = child_list
            perm_tree_node_list.append(perm_tree_node)
    for tree_node in perm_tree_node_list:
        perm_tree_list.append(tree_node)

    return perm_tree_list


def get_user_menu(role_code):
    """
    获取用户菜单权限列表
    :param role_code:
    :return:
    """
    try:
        if role_code:
            user_permission_list = Permissions.get_menu_permissions_by_role_code(role_code)
            json_str_list = jsonify({"data": user_permission_list}).data.decode()
            perm_list_dict = json.loads(json_str_list)["data"]
            menu_list = perm_classify_tree(perm_list_dict, '-1')
        else:
            menu_list = None
        return menu_list
    except Exception as e:
        logging.debug(e)
        raise e


def format_permission_info(perm_list_page):
    """
        通过递归对权限信息进行格式化
        :param perm_list_page
        :return:
    """
    format_permission_list = []
    for perm_obj in perm_list_page:
        # 格式化时间为 年-月-日 时:分:秒 去除毫秒数
        format_time = str(perm_obj.update_time).split(".")[0]

        format_permission_dict = {
            "permission_id": perm_obj.permission_id,
            "permission_name": perm_obj.permission_name,
            "url": perm_obj.url,
            "icon": perm_obj.icon,
            "permission_type": Permissions.permission_type_dict[perm_obj.permission_type],
            "sort": perm_obj.sort,
            "parent_id": perm_obj.parent_id,
            "desc": perm_obj.desc,
            "status": Permissions.status_dict[perm_obj.status],
            "update_time": format_time
        }
        format_permission_list.append(format_permission_dict)
    return format_permission_list


def cascade_delete_perm(parent_id):
    """
    级联删除 通过parent_id 删除子权限
    :param parent_id:
    :return:
    """
    # 获取此权限旗下所有子权限的ID信息
    child_perm_list = Permissions.get_child_perm_id(parent_id)
    if len(child_perm_list) != 0:
        for child_perm in child_perm_list:
            cascade_delete_perm(child_perm.permission_id)
            Permissions.delete_perm(child_perm.permission_id, datetime.datetime.now())
    else:
        return


def get_permission_role_list():
    """
    根据权限ID获取角色列表数据
    :return:
    """
    params = request.get_json()
    page = params.get("page")
    per_page = params.get("per_page")
    search_data = params.get("search_data")
    permission_id = params.get("permission_id")
    response_dict = {}
    try:
        permission_role_codes = Permissions.get_perm_info(permission_id).roles
        if permission_role_codes:
            data_list = list(
                Role.get_role_list_by_role_code_org_code(session.get("org_code"), permission_role_codes, page,
                                                         per_page, search_data))
            if data_list:
                response_dict["total_count"] = Role.get_role_list_by_role_code_org_code_total_count(
                    session.get("org_code"), permission_role_codes, search_data)
            else:
                response_dict["total_count"] = 0
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
            response_dict["data"] = data_list
        else:
            response_dict["code"] = response.SUCCESS
            response_dict["msg"] = response.RESULT_SUCCESS
            response_dict["data"] = []
            response_dict["total_count"] = 0
    except Exception as e:
        logging.error(e)
        response_dict["code"] = response.ERROR
        response_dict["msg"] = response.RESULT_ERROR
        response_dict["data"] = []

    finally:
        return jsonify(response_dict)



def get_permission_by_url(url):
    """
    根据URL获取相关角色
    :param url:
    :author ChenWanYue
    :return:
    """
    try:
        return Permissions.get_permission_by_url(url)
    except Exception as e:
        logging.debug(e)
        return ''


def get_child_permission_by_code(role_code, parent_id, url):
    """
    根据菜单编码获取子菜单
    :author ChenWanYue
    :return:
    """
    try:
        return Permissions.get_child_permission_by_code(role_code, parent_id, url)
    except Exception as e:
        logging.debug(e)
        return None


def get_parent_permission_by_id(permission_id):
    """
    根据ID获取父权限
    :param permission_id:
    :author ChenWanYue
    :return:
    """
    try:
        return Permissions.get_perm_info(permission_id)
    except Exception as e:
        logging.debug(e)
        return None


def get_first_menu(role_code):
    """
    获取第一菜单
    :param rle_code:
    :author ChenWanYue
    :return:
    """
    try:
        if role_code:
            return Permissions.get_first_menu_permissions_by_role_code(role_code)
        else:
            return None

    except Exception as e:
        logging.debug(e)
        return None

def get_left_menu(role_code):
    """
    获取左侧菜单
    :param rle_code:
    :author ChenWanYue
    :return:
    """
    try:
        if role_code:
            return get_two_menu(role_code)
        else:
            return None
    except Exception as e:
        logging.debug(e)
        return None


def get_two_menu(role_code):
    """
    获取前二级菜单
    :param role_code:
    :return:
    """
    logging.info('get_two_menu--role_code:%s'%role_code)
    per_list = Permissions.get_first_menu_permissions_by_role_code(role_code)
    menu_list = []
    if len(per_list) > 0 :
        for item in per_list:
            if len(item.permission_id) == 3:
                menu_list.append({
                    'permission_id':item.permission_id,
                    'permission_name':item.permission_name,
                    'url':item.url,
                    'icon':item.icon,
                    'sort':item.sort,
                    'parent_id':item.parent_id,
                    'permission_type':item.permission_type,
                    'desc':item.desc,
                    'child_list':get_child_menu(item.permission_id,per_list),
                })
        logging.info('menu_list：%s'%menu_list)
        return menu_list
    return None


def get_child_menu(permission_id,per_list):
    """

    :param permission_id:
    :param per_list:
    :return:
    """
    logging.info('get_child_menu')
    child_list = []
    if len(per_list) > 0:
        for item in per_list:
            if item.parent_id == permission_id:
                child_list.append({
                    'permission_id':item.permission_id,
                    'permission_name':item.permission_name,
                    'url':item.url,
                    'icon':item.icon,
                    'sort':item.sort,
                    'parent_id':item.parent_id,
                    'permission_type':item.permission_type,
                    'desc':item.desc,
                    'child_list':get_child_menu(item.permission_id,per_list),
                })
    return  child_list