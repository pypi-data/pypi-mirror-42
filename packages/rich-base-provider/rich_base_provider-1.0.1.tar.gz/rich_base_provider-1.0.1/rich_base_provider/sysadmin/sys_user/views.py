#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 8:56
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : views.py
# @Software: Rich Web Platform
# @Function: sys_user 路由

import logging, base64, os, platform
import datetime as dt
from flask import request, session, jsonify
from rich_base_provider.sysadmin.sys_user.models import User
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_permission.models import Permissions
from rich_base_provider import response
from rich_base_provider.utils import verification_code, email_reset_password
from flask_security import current_user


def api_add_user():
    """
    机构新增用户接口
    :return:
    """
    logging.info('api_add_user')
    response_data = {}
    try:
        params = request.get_json()
        username = params.get('username')
        name = params.get('name')
        email = params.get('email')
        mobile = params.get('mobile')
        avatar = params.get('avatar')
        is_stop = params.get('is_stop')
        bassnise_type = params.get('bassnise_type')
        company_info = params.get('company_info')
        check_msg = check_user(username, email, mobile)
        if not check_msg:
                user = User.create(
                    username=username,
                    name=name,
                    password=params.get('password'),
                    email=email,
                    mobile=mobile,
                    gender=params.get('gender'),
                    org_code=params.get('org_code'),
                    role_code=params.get('role_code'),
                    create_by=current_user.user_code,
                    update_by=current_user.user_code,
                    is_stop=is_stop,
                    bassnise_type=bassnise_type,
                    company_info=company_info
                )

                if avatar:
                    avatar_url = save_avatar(avatar, user.user_code)
                    user.info.avatar = avatar_url
                    user.save()
                response_data['code'] = response.SUCCESS
                response_data['msg'] = response.RESULT_SUCCESS
                response_data['data'] = []
        else:
            response_data['code'] = response.PARAMETER_ERROR
            response_data['msg'] = check_msg
            response_data['data'] = check_msg

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def get_orgs():
    """
    通过当前机构code获取其和其子机构的 code：name键值对
    :return: code：name键值对
    """
    logging.info('get_orgs')
    response_data = {}
    try:

        params = request.args
        org_id = params.get('org_id')
        if org_id:
            org_code = Sys_org.objects(org_id=org_id).first().org_code
        else:
            org_code = session.get('org_code')
        page = params.get('page', 1)
        org_name = params.get('name', "")
        org_list = Sys_org.find_sysorg(org_code=org_code, org_name=org_name, page=page)
        org_info = []
        for org in org_list["orgs"]:
            org_info.append({
                'org_code': org.org_code,
                'org_id': org.org_id,
                'org_name': org.org_name})

        count = org_list["count"]

        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = org_info
        more = int(page) * 10 < int(count)
        response_data["more"] = more

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def get_org_role():
    """
    通过 role_code 获取用户org_role 信息
    by shuyi
    :return:
    """
    logging.info("get_org_role")
    response_data = {}
    try:
        role_code = request.get_json().get("role_code")
        org_role_obj = User.get_info_by_org_role_code(role_code)
        org_role_list = list()
        for each in org_role_obj:
            org_role_list.append(each.org_role)
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = org_role_list

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def get_user_info():
    """
    获取用户详情
    :return:
    """
    logging.info('get_user_info')
    response_data = {}
    try:
        params = request.get_json()
        user_code = params.get('user_code')
        session_org_code = session.get('org_code')
        user_data = User.get_user_by_org_and_data(session_org_code, user_code)
        user = get_users_method(user_data)
        if user:
            user = user[0]
            role_code = user.get('role_code')
            permissions = Permissions.get_permissions_by_role_code(role_code)
            per_name = []
            for per in permissions:
                per_name.append(per.permission_name)
            user['permission_names'] = per_name
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = user

        else:
            response_data["code"] = response.PARAMETER_ERROR
            response_data['data'] = []
            response_data['msg'] = response.RESULT_PARAMETER_ERROR

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)



def update_user():
    """
    机构编辑用户信息接口
    :return:
    """
    logging.info('update_user')
    response_data = {}
    error_msg = {}
    try:
        params = request.get_json()
        user_code = params.get('user_code')
        username = params.get('username')
        name = params.get('name')
        email = params.get('email')
        mobile = params.get('mobile')
        gender = params.get('gender')
        org_code = params.get('org_code')
        role_codes = params.get('role_code')
        avatar = params.get('avatar')
        desc = params.get('desc')
        is_stop = params.get('is_stop')
        bassnise_type = params.get('bassnise_type')
        company_info = params.get('company_info', '')
        session_org_code = session.get('org_code')
        user = User.get_by(user_code=user_code)
        # 验证信息
        rocket_update_data = {}
        if user:
            if username == user.username and username != '':  # 提交的用户名是当前用户旧用户名
                username = ''
            else:
                rocket_update_data['username'] = username
            if email == user.account.email and email != '':  # 邮箱
                email = ''
            else:
                rocket_update_data['email'] = email
            if mobile == user.account.mobile and mobile != '':  # 手机号
                mobile = ''
            if name != user.info.name and name != '':
                rocket_update_data['name'] = name

            error_msg = check_user(username, email, mobile)  # 验证账户信息是否重复
        if not error_msg:

            # 更新用户信息
            if username:
                user.username = username
                session['username'] = username
            if email:
                user.account.email = email
                session['email'] = email
            if mobile:
                user.account.mobile = mobile
            if name:
                user.info.name = name
            if gender:
                user.info.gender = gender
            if org_code and role_codes:
                user.update_org_role(session_org_code, org_code, role_codes)
            if bassnise_type:
                user.bassnise_type = bassnise_type
            if company_info:
                user.company_info = company_info
            if avatar:
                avatar_url = save_avatar(avatar, user.user_code)
                user.info.avatar = avatar_url
                session['avatar'] = avatar_url
            if isinstance(is_stop, bool):
                org_role = user.get_org_role_by_org_code(org_code)
                org_role.is_stop = is_stop
            if is_stop:  # 停用用户修改状态
                user.status = 1
            elif is_stop == False:
                user.status = 0
            user.desc = desc
            user.update_by = current_user.user_code
            user.update_time = dt.datetime.now()
            user.save()
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = []
        else:
            response_data['code'] = response.PARAMETER_ERROR
            response_data['msg'] = error_msg
            response_data['data'] = error_msg
    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def delete_user():
    """
    机构删除用户关联
    :return:
    """
    logging.info('delete_user')
    response_data = {}
    try:
        params = request.get_json()
        user_code = params.get('user_code')
        org_code = params.get('org_code')  # 前端必须传值，子机构从session获取不了
        if user_code != current_user.user_code:
            user = User.get_by(user_code=user_code)
            if user:
                # user.delete_org(org_code)
                res_delete = user.delete_user_by_code(user_code)
                if res_delete:
                    response_data['code'] = response.SUCCESS
                    response_data['msg'] = response.RESULT_SUCCESS
                    response_data['data'] = []
            else:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_ERROR
                response_data['data'] = []
        else:
            response_data['code'] = response.ERROR
            response_data['msg'] = '无法删除自己'
            response_data['data'] = []

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)



def search_users():
    """
    搜索用户
    :return:
    """
    logging.info('search_users')
    response_data = {}
    count = 0
    try:
        params = request.values.to_dict()
        search_data = params.get('search_data')
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
        org_code = session.get('org_code')
        users_data = User.get_users_by_org(data=search_data, org_code=org_code, page=page,
                                           per_page=per_page, sort=sort, sortOrder=sortOrder)  # 分页获取同一机构（子机构）的用户
        users = get_users_method(users_data)
        if users :
            count = User.get_org_users_count(org_code=org_code, data=search_data)  # 获取当前搜索用户数量
            response_data['count'] = count
        elif not users:
            response_data['count'] = 0
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = users
        return jsonify({'rows': users, 'total': count})
    except Exception as e:
        logging.debug(e)
        return jsonify({'rows':[],'total':0})


def user_reset_password():
    """
    用户管理--重置密码
    通过code查询到用户，获取用户姓名，用户邮箱，通过随机生成六位数密码，发送给用户邮箱
    :return:
    """
    logging.info('user_reset_password')
    response_data = {}
    try:
        params = request.get_json()
        user_code = params.get('user_code')
        new_password = verification_code(6)  # 生成6位 数字字母 密码
        new_password = ''.join(new_password)
        user = User.get_by(user_code=user_code)
        if user:
            name = user.username
            email = user.account.email
            email_reset_password(name=name, email=email, new_password=new_password)  # 发送重置密码邮件
            user.password = new_password
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = []

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def vaild_user():
    """
    验证用户
    :return:
    """
    logging.info('ver_user')
    response_data = {}
    try:
        params = request.get_json()
        field = params.get('field')
        data = params.get('data')
        user = None
        if field == 'username':
            user = User.get_by(username=data)
        if field == 'email':
            user = User.get_by(email=data)
        if field == 'mobile':
            user = User.get_by(mobile=data)
        if user:
            response_data['code'] = response.PARAMETER_ERROR  # -2
            response_data['msg'] = response.RESULT_EXIST_ERROR  # 信息已存在
            response_data['data'] = []
        else:
            response_data['code'] = response.SUCCESS
            response_data['msg'] = response.RESULT_SUCCESS
            response_data['data'] = []

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def get_user_permission():
    """获取用户在该机构下的权限"""
    logging.info('ver_user')
    response_data = {}
    try:
        params = request.get_json()
        role_code = params.get('role_code')  # 用户角色list
        permissions = Permissions.get_permission_by_role_code(role_code)
        per_name = []
        for per in permissions:
            per_name.append(per.permission_name)
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = per_name

    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR

    finally:
        return jsonify(response_data)


def get_users_method(users_data):
    """
    整理用户信息
    :param users_data:
    :return:
    """
    users = []
    for user in users_data:
        # 机构处理
        sys_org = user.get('sys_org')
        org_name = sys_org[0].get('org_name')
        org_code = sys_org[0].get('org_code')
        is_stop = user.get('org_role')[0].get('is_stop')

        # 角色处理
        role_names = []
        role_codes = []
        sys_role = user.get('sys_role')
        if sys_role:
            for role in sys_role:
                role_names.append(role.get('name', ''))
                role_codes.append(role.get('role_code', ''))
        # 时间处理
        if user.get('update_time'):
            update_time = user.get('update_time').strftime('%F %H:%M:%S')
        else:
            update_time = ''

        # 时间处理
        if user.get('last_login_at'):
            last_login_at = user.get('last_login_at').strftime('%F %H:%M:%S')
        else:
            last_login_at = ''

        users.append({
            'user_code': user.get('user_code'),
            'org_code': org_code,
            'name': user.get('info').get('name'),
            'username': user.get('username'),
            'desc': user.get('desc'),
            'mobile': user.get('account').get('mobile'),
            'email': user.get('account').get('email'),
            'org_name': org_name,
            'role_name': role_names,
            'role_code': role_codes,
            'update_time': update_time,
            'last_login_time': last_login_at,
            'is_stop': is_stop,
            'avatar': user.get('info').get('avatar'),
            'gender': user.get('info').get('gender'),
            'role_list': user.get('sys_role'),
            'bassnise_type': user.get('bassnise_type'),
            'company_info': user.get('company_info')
        })
    return users


def check_user(username, email, mobile):
    """
    判断用户是否存在
    :params username:
    :params email:
    :params mobile:
    :return:
    """
    logging.info('check_user')
    error_msg = {}
    users = User.fuzzy_get_by(username, email, mobile)
    if users:
        for user in users:
            if user.username == username:
                error_msg['username'] = '用户名已存在'
            if user.account.email == email:
                error_msg['email'] = '邮箱已存在'
            if user.account.mobile == mobile:
                error_msg['mobile'] = '手机号已存在'
    return error_msg


def save_avatar(img, user_code):
    """
    保存头像到本地
    :param img:
    :return:
    """
    logging.info('save_image')
    try:
        if img is not None:
            img = img.split(',')[1]
            imgdata = base64.b64decode(img)
            path = os.getcwd()
            CURRENT_SYSTEM = platform.system()
            if CURRENT_SYSTEM == 'Windows':
                image_path = path + '\\rich_base_provider\\static\\images\\avatar\\'
            else:
                image_path = path + '/rich_base_provider/static/images/avatar/'

            file_name = str(user_code) + dt.datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
            file = open(image_path + file_name, 'wb+')
            logging.info(file)
            file.write(imgdata)
            file.close()
        return file_name
    except Exception as e:
        logging.debug(e)
        raise e


def update_password():
    """
    修改密码
    :return:
    """
    logging.info("update_password")
    try:
        username = session.get("username")
        old_password = request.get_json().get("old_pwd")
        new_password = request.get_json().get("new_pwd")
        repeat_password = request.get_json().get("re_pwd")

        user = User.get_by(username=username)
        user_password = user.check_password(old_password)

        if not all([old_password, new_password, repeat_password]):
            return jsonify({"msg": "数据不完整"})

        if not user_password:
            return jsonify({"msg": "原密码错误"})

        if new_password != repeat_password:
            return jsonify({"msg": "两次密码输入不一致"})

        # RocketChat 更新用户密码
        try:
            user.password = new_password
            return jsonify({"code": response.SUCCESS})
        except:
            return jsonify({"msg": "修改密码失败"})

    except Exception as e:
        logging.info(e)
        return jsonify({"code": response.ERROR,
                        'msg': response.RESULT_ERROR})


""" 部门用户模块 """


def find_department_user_page(org_code, department_id, department_code):
    """
    返回部门员工主页面
    :return:
    """
    response_dict = get_current_user_list_select(org_code, department_id)
    current_org_user_list = response_dict["response_data_list"]
    department_user_code_list = response_dict["department_user_code_list"]
    return org_code, department_id, department_code,current_org_user_list,department_user_code_list



def get_department_user_list():
    """
    根据页码、搜索条件查询指定数目记录
    :return:
    """
    logging.info("get_integral_rule_list")
    count = 0
    try:
        params = request.values.to_dict()
        page = params.get("page")
        if page is '0':
            page = 1
        per_page = params.get("per_page")
        search_data = params.get("search_data") or ''
        department_id = params.get("department_id")
        department_user_list = User.get_user_list_by_data(page, per_page, search_data, [department_id])
        response_data_list = format_department_user_info(department_user_list)
        if response_data_list:
            count = User.get_department_user_total_count([department_id], search_data)
        return jsonify({'rows': response_data_list, 'total': count})
    except Exception as e:
        logging.debug(e)
        return jsonify({'rows':[],'total':0})


def update_current_department_user():
    """
    修改当前部门员工列表
    :return:
    """
    logging.info("remove_current_department")
    response_dict = {}
    try:
        params = request.get_json()
        old_user_code_list = params.get("old_user_code_list").split(",")
        del old_user_code_list[0]
        new_user_code_list = params.get("new_user_code_list")
        department_id = params.get("department_id")
        department_code = params.get("department_code")
        org_code = params.get("org_code")
        # 获取需要变化的用户编号
        change_user_code_list = []
        if not old_user_code_list and new_user_code_list:
            change_user_code_list = new_user_code_list
        elif old_user_code_list and not new_user_code_list:
            change_user_code_list = old_user_code_list
        elif old_user_code_list and new_user_code_list:
            change_user_code_list = list(set(old_user_code_list) ^ set(new_user_code_list))

        # 获取当前选中员工对象
        change_user_obj_list = User.get_user_list_by_user_code_list(change_user_code_list)
        remove_user_code_list = []
        insert_user_code_list = []
        for change_user_obj in change_user_obj_list:
            if change_user_obj.user_code in old_user_code_list:
                # 原先在此部门 本次操作之后不在 需要进行移除
                remove_user_code_list.append(change_user_obj.user_code)
            if change_user_obj.user_code in new_user_code_list:
                # 原先不在此部门 本次操作之后存在 需要进行添加
                insert_user_code_list.append(change_user_obj.user_code)
        if len(remove_user_code_list) > 0:
            User.update_current_department_user_by_data(remove_user_code_list, org_code, department_id,
                                                        "remove")
            # 级联移除 若操作部门旗下存在子部门 则需将此用户从子部门移除
            department_list = Sys_org.get_org_info(org_code).department
            for department in department_list:
                if department.code.startswith(department_code) and department.status != "3":
                    User.update_current_department_user_by_data(remove_user_code_list, org_code,
                                                                department.id,
                                                                "remove")
        if len(insert_user_code_list) > 0:
            User.update_current_department_user_by_data(insert_user_code_list, org_code, department_id,
                                                        "insert")
            parent_department_code = department_code
            while len(parent_department_code) > 4:
                parent_department_code = parent_department_code[: -4]
                parent_department_id = Sys_org.get_department_info(org_code, parent_department_code).id
                # 级联追加 若操作部门存在父部门 则需将员工追加至父部门
                User.update_current_department_user_by_data(insert_user_code_list, org_code,
                                                            parent_department_id,
                                                            "insert")
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


def format_department_user_info(department_user_list):
    """
    格式化返回的用户信息
    :param department_user_list:
    :return:
    """
    format_department_user_list = []
    gender_dict = {"M": "男", "F": "女", "N": "性别未知"}
    for department_user in department_user_list:
        update_time = str(department_user.update_time).split(".")[0]
        birthday = department_user.info.birthday
        if not birthday or birthday == "":
            birthday = "暂无出生日期"
        email = department_user.account.email
        if not email or email == "":
            email = "暂无邮箱"
        mobile = department_user.account.mobile
        if not mobile or mobile == "":
            mobile = "暂无手机号"
        format_department_user_dict = {
            "user_code": department_user.user_code,
            "username": department_user.username,
            "name": department_user.info.name,
            "birthday": birthday,
            "gender": gender_dict.get(department_user.info.gender),
            "email": email,
            "mobile": mobile,
            "status": SysDict.get_dict_info_by_type_and_id("sys_user_status", str(department_user.status)).dict_name,
            "update_time": update_time
        }
        format_department_user_list.append(format_department_user_dict)
    return format_department_user_list


def get_current_user_list_select(org_code, current_department_id):
    """
    获取用户信息列表信息加载到select(当前操作机构下的所有用户)
    :return:
    """
    # 获取当前机构所有员工信息
    result_dict = User.get_user_list_by_current_org(org_code)
    response_data_list = []
    # 存储当前已存在此部门的员工编号
    department_user_code_list = ""
    for user in result_dict["current_org_user_list"]:
        # 判断当前员工是否已存在此部门
        for org_role in user.org_role:
            if org_role.org_code == org_code:
                if current_department_id in org_role.department_id:
                    department_user_code_list = department_user_code_list + "," + user.user_code
                    response_data_list.append({
                        "user_name": user.username,
                        "user_code": user.user_code,
                        "name": user.info.name,
                        "selected": "true"
                    })
                else:
                    response_data_list.append({
                        "user_name": user.username,
                        "user_code": user.user_code,
                        "name": user.info.name,
                        "selected": "false"
                    })
    return {"response_data_list": response_data_list, "department_user_code_list": department_user_code_list}


def get_org_users():
    """
    获取机构及子机构下的用户
    :return:
    """
    logging.info('get_org_users')
    response_data = {}
    try:
        params = request.args
        org_code = session.get('org_code')
        page = params.get('page')
        user_name = params.get('name', "")
        user_list, count = User.get_org_users(org_code=org_code, data=user_name, page=page)
        user_info = []
        for user in user_list:
            user_info.append({
                'user_code': user.get('user_code'),
                'user_name': user.get('username')})
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = user_info
        more = int(page) * 10 < int(count)
        response_data["more"] = more
    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        return jsonify(response_data)


def reset_password():
    """
    重设密码
    :return:
    """
    logging.info("reset_password")
    try:
        params = request.get_json()
        email = params.get('email')
        new_password = params.get('password')
        repeat_password = params.get('repeat_password')
        user = User.get_by(email=email)
        if not all([email, new_password, repeat_password]):
            return jsonify({"msg": "数据不完整"})
        if new_password != repeat_password:
            return jsonify({"msg": "两次密码输入不一致"})

        # RocketChat 更新用户密码
        try:
            user.password = new_password
            return jsonify({"code": response.SUCCESS})
        except:
            return jsonify({"code": response.ERROR, 'msg': response.RESULT_ERROR})
    except Exception as e:
        logging.info(e)
        return jsonify({"code": response.ERROR, 'msg': response.RESULT_ERROR})
