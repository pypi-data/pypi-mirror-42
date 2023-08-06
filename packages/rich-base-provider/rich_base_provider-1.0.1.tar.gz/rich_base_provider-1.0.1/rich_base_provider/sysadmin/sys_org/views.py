#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 11:51
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : views.py
import base64, os, platform
import json
import logging
from flask import request, jsonify, session
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider import response
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from flask_security import current_user



def edit_org_html(org_code):
    """
    获取编辑sys_org页面
    :return:
    by denghaolin
    """
    logging.info('edit_org_html')

    org_obj = Sys_org.get_org_info(org_code)
    org_dict = {}
    org_dict['org_code'] = org_code
    org_dict['org_name'] = org_obj.org_name
    org_dict['org_short_name'] = org_obj.org_short_name
    org_dict['contacts'] = org_obj.contacts
    org_dict['bl_code'] = org_obj.bl_code
    org_dict['master'] = org_obj.master
    org_dict['id_card_number'] = org_obj.id_card_info.idcard_number
    org_dict['mobile'] = org_obj.mobile
    org_dict['concrete_address'] = org_obj.id_card_info.concrete_address
    org_dict['bl_address'] = org_obj.bl_address
    org_dict['registered_capital'] = org_obj.registered_capital
    org_dict['mail'] = org_obj.mail
    org_dict['remarks'] = org_obj.remarks
    org_dict['website'] = org_obj.website
    org_dict['bank_owner'] = org_obj.bank_cart_info.bank_owner
    org_dict['bank_name'] = org_obj.bank_cart_info.bank_name
    org_dict['bank_account'] = org_obj.bank_cart_info.bank_account
    org_dict['bank_bind_mobile'] = org_obj.bank_cart_info.mobile
    org_dict['bank_address'] = org_obj.bank_cart_info.bank_address
    org_dict['org_area'] = org_obj.org_area if org_obj.org_area else None  # 机构所在地
    org_dict['org_type'] = org_obj.org_type  # 机构类型
    org_dict['bl_code'] = org_obj.bl_code  # 经营编码
    org_dict['bank_card_type'] = org_obj.bank_cart_info.bank_card_type  # 银行卡类型
    if str(org_code) == SysDict.get_dict_list_by_type(dict_type='org_code')[0].description:  # 顶级机构
        org_dict['father_org_name'] = '顶级机构'
        org_dict['father_org_code'] = SysDict.get_dict_list_by_type(dict_type='org_code')[0].description
    else:
        father_org_obj = Sys_org.find_father_sysorg(org_code)  # 获取上级机构
        org_dict['father_org_code'] = father_org_obj.org_code
        org_dict['father_org_name'] = father_org_obj.org_name
    org_dict['cert_correct_img'] = org_obj.id_card_info.cert_correct_img  # 身份证正面照片
    org_dict['cert_opposite_img'] = org_obj.id_card_info.cert_opposite_img  # 身份证反面照片
    org_dict['hand_id_card_img'] = org_obj.id_card_info.hand_id_card_img  # 手持身份证照片
    org_dict['card_correct_img'] = org_obj.bank_cart_info.card_correct_img  # 银行卡正面照
    org_dict['card_opposite_img'] = org_obj.bank_cart_info.card_opposite_img  # 银行卡背面照
    org_dict['bl_img'] = org_obj.bl_img  # 营业执照照片
    org_dict['door_img'] = org_obj.door_img  # 门头照片
    org_dict['cashier_img'] = org_obj.cashier_img  # 收银台照片
    org_dict['province_code'] = org_obj.org_area[:2] + '0000' if org_obj.org_area else None  # 省份编码
    org_dict['city_code'] = org_obj.org_area[:4] + '00' if org_obj.org_area else None  # 城市编码
    return org_dict





def get_edit_department_html(department_code, org_code=None):
    """
    获取部门编辑页面
    :param org_code:
    :param department_code:
    :return:
    by denghaolin
    """
    logging.info('get_edit_department_html')
    try:
        if not org_code:
            org_code = session.get('org_code')
        org_obj = Sys_org.get_org_info(org_code)
        departments = org_obj.department
        department_dict = {}
        for department in departments:
            if department.code == department_code:
                if len(department.code) > 4:
                    father_department = Sys_org.get_father_department(org_code=org_code,
                                                                      department_code=department.code)
                    father_department_name = father_department.get('name')
                    father_department_code = father_department.get('code')
                else:
                    father_department_name = ''
                    father_department_code = ''
                department_dict = {
                    'department_name': department.name,
                    "father_department_name": father_department_name,
                    "father_department_code": father_department_code,
                    "status": department.status
                }
                break
        return department_dict
    except Exception as e:
        logging.debug(e)
        raise e


def get_departments():
    """
    获取子部门
    :return:
    by denghaolin
    """
    logging.info('get_departments')
    response_data = {}
    try:
        params = request.args
        org_code = params.get('org_code')
        if not org_code:
            org_code = Sys_org.objects(org_id=params.get('org_id')).first().org_code
        page = params.get('page')
        department_name = params.get('name', '')
        department_code = params.get('department_code')
        departments, count = Sys_org.find_department(org_code=org_code, department_code=department_code,
                                                     department_name=department_name, page=page, sort=1)
        department_info = []
        if departments:
            for department in departments:
                department_info.append({
                    'department_code': department.get('department').get('code'),
                    'department_name': department.get('department').get('name'),
                    'department_id': department.get('department').get('id')
                })
        count = len(department_info)
        response_data['code'] = response.SUCCESS
        response_data['msg'] = response.RESULT_SUCCESS
        response_data['data'] = dict(data=department_info, count=count)
        more = int(page) * 10 < int(count)
        response_data["more"] = more
    except Exception as e:
        logging.debug(e)
        response_data["code"] = response.ERROR
        response_data['data'] = []
        response_data['msg'] = response.RESULT_ERROR
    finally:
        return jsonify(response_data)



def get_department_list():
    """
    查询部门列表
    :return:
    """
    logging.info("get_department_list")
    response_data = {}
    result_list = []
    try:
        # 接收参数
        params = request.values.to_dict()
        # 查找部门列表
        org_code = session.get('org_code')
        search_data = params.get("search_data") or ''
        per_page = int(params.get("per_page", "10"))
        page = int(params.get("page", "1")) / per_page + 1
        sort = params.get('sort') if params.get('sort') else 'create_time'
        if sort == 'department_name':
            sort = 'name'
        elif sort == 'department_code':
            sort = 'code'
        elif sort == 'father_department_name':
            sort = 'code'
        sortOrder = params.get('sortOrder')
        if sortOrder == 'desc':
            sortOrder = -1
        elif sortOrder == 'asc':
            sortOrder = 1
        department_list, count = Sys_org.find_department(org_code=org_code,
                                                         department_name=search_data, block_up=True,
                                                         page=page, per_page=per_page, sort=sort, sortOrder=sortOrder)
        if department_list:
            for department in department_list:
                result_list.append({"department_id": department.get("department").get("id"),
                                    "department_name": department.get('department').get('name'),
                                    "department_code": department.get('department').get('code'),
                                    "create_time": str(department.get('department').get('create_time')).split(".")[
                                        0],
                                    "father_department_name": '' if len(
                                        department.get('department').get(
                                            'code')) == 4 else Sys_org.get_father_department(org_code=org_code,
                                                                                             department_code=department.get(
                                                                                                 'department').get(
                                                                                                 'code')).get(
                                        'name'),
                                    "status": SysDict.get_dict_info_by_type_and_id(dict_type='public_status',
                                                                                   dict_id=department.get(
                                                                                       'department').get(
                                                                                       'status')).dict_name})

        return jsonify({'rows': result_list, 'total': count})
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        return jsonify({'rows':[],'total':0})


def add_department():
    """
    新增部门
    :return:
    by denghaolin
    """
    logging.info('add_department')
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['org_code', 'name', 'status']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break
        if not response_data:
            # 判断部门是否已存在
            old_department = Sys_org.get_exist_department(org_code=params.get('org_code'),
                                                          department_name=params.get('name'))
            if old_department:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_EXIST_ERROR
                response_data['data'] = ""
            else:
                # 新增部门
                Sys_org.add_department(params)
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



def edit_department():
    """
    编辑部门
    :return:
    by denghaolin
    """
    logging.info('edit_department')
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['org_code', 'department_code', 'status']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
        if not response_data:
            # 更新部门
            res = Sys_org.edit_department(params)
            if res == response.ERROR:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_EXIST_ERROR
                response_data['data'] = ""
            else:
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


def delete_department():
    """
    删除部门
    :return:
    by denghaolin
    """
    logging.info("delete_department")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['department_code', 'org_code']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
        if not response_data:
            # 删除部门
            Sys_org.delete_department(params)
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



def get_org_list():
    """
    获取sys_org机构列表
    :return:
    by denghaolin
    """
    response_data = {
        'code': response.ERROR,
        'msg': '系统错误',
        'data': []
    }
    logging.info('get_org_list')
    try:
        params = request.values.to_dict() if request.values.to_dict() else json.loads(request.data)
        search_data = params.get('search_data', '')
        if not search_data:
            search_data = ''
        per_page = int(params.get("per_page", "10"))
        page = int(params.get("page", "1")) / per_page + 1
        org_code = session.get('org_code')

        res_code, result_list, count = get_org_data(org_code=org_code, page=page, per_page=per_page,
                                                    search_data=search_data)
        if res_code == '0':
            return jsonify({'rows':result_list,'total':count})
        else:
            raise Exception
    except Exception as e:
        logging.debug(e)
        return jsonify({'rows':[],'total':0})


def get_org_data(org_code, search_data, page=1, per_page=10):
    """
    获取sys_org数据
    :param org_code:机构编码
    :param page: 当前页
    :param per_page: 请求数量
    :param search_data: 搜索内容
    :return:
    by denghaolin
    """
    logging.info('get_org_data')
    try:
        # 获取包括自己的所有机构
        temp_org_data, count = Sys_org.find_sysorg(org_code=org_code, org_name=search_data, page=page,
                                                   per_page=per_page, order_by_param='-create_time').get(
            'orgs'), Sys_org.find_sysorg(org_code=org_code, org_name=search_data, page=page, per_page=per_page).get(
            'count')
        result_list = []
        for org_data in temp_org_data:
            org_data_dict = {}
            org_data_dict['org_name'] = org_data.org_name if org_data.org_name else ''
            org_data_dict['mobile'] = org_data.mobile if org_data.mobile else ''
            org_data_dict['org_code'] = org_data.org_code if org_data.org_code else ''
            org_data_dict['status'] = '正常' if org_data.status == 0 else '停用'
            result_list.append(org_data_dict)
        return response.SUCCESS, result_list, count
    except Exception as e:
        logging.debug(e)
        raise e


def check_org(org_name, mail, idcard_number, mobile):
    """
    判断参数是否已存在
    :param org_name:
    :param mail:
    :param idcard_number:
    :param mobile:
    :return:
    """
    logging.info('check_org')
    error_msg = {}
    org = Sys_org.get_by(org_name=org_name)
    if org:
        error_msg['org_name'] = '机构名已存在!'
    org = Sys_org.get_by(mail=mail)
    if org:
        error_msg['mail'] = '邮箱已存在!'
    org = Sys_org.get_by(idcard_number=idcard_number)
    if org:
        error_msg['idcard_number'] = '身份证号已存在!'
    org = Sys_org.get_by(mobile=mobile)
    if org:
        error_msg['mobile'] = '联系电话已存在!'
    return error_msg


def insert_org():
    """
    新增机构
    :return:
    by denghaolin
    """
    response_data = {
        'code': response.ERROR,
        'msg': '系统错误',
        'data': ''
    }
    logging.info('insert_org')
    try:
        params = request.values.to_dict() if request.values.to_dict() else json.loads(request.data)
        father_org_code = params.get('org_code')  # 用户选择的所属机构
        if not father_org_code:
            response_data['msg'] = '请选择所属机构'
            return jsonify(response_data)
        insert_org_code = Sys_org.create_org_code(father_org_code)  # 获取要插入的org_code
        insert_mail = params.get('mail')
        insert_org_name = params.get('org_name')
        insert_mobile = params.get('mobile')
        insert_id_card_num = params.get('idcard_number')
        # 判断参数是否完整
        check_data = ['mail', 'org_name', 'mobile', 'idcard_number']
        for data in check_data:
            if not params.get(data):
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                return jsonify(response)
        # 验证参数唯一性
        check_msg = check_org(org_name=insert_org_name, mail=insert_mail, idcard_number=insert_id_card_num,
                              mobile=insert_mobile)
        if check_msg:
            res_msg = ''
            for key, value in check_msg.items():
                res_msg += value
            response_data['msg'] = res_msg
            return jsonify(response_data)
        result = Sys_org.insert_org(req_data=params, org_code=insert_org_code)
        if result:
            response_data['code'] = response.SUCCESS
            response_data['msg'] = '新增机构成功'
            return jsonify(response_data)
        else:
            response_data['msg'] = '新增机构失败'
            return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        return jsonify(response_data)



def delete_org():
    """
    删除机构
    :return:
    by denghaolin
    """
    response_data = {
        'code': response.ERROR,
        'msg': '系统错误',
        'data': ''
    }
    logging.info('delete_org')
    try:
        params = request.values.to_dict() if request.values.to_dict() else json.loads(request.data)
        org_code = params.get('org_code')
        # 用户尝试删除顶级机构
        if org_code == '0001':
            response_data['code'] = response.ERROR
            response_data['msg'] = '不能删除顶级机构'
            return jsonify(response_data)
        user_own_org_codes = current_user.org_codes
        for user_own_org_code in user_own_org_codes:
            if user_own_org_code == org_code:
                response_data['code'] = response.ERROR
                response_data['msg'] = '不能删除自己所属的机构'
                return jsonify(response_data)
        res_code = Sys_org.deleted(org_code)
        if res_code == '-1':
            response_data['msg'] = '请选择正确的机构'
            return jsonify(response_data)
        response_data['code'] = response.SUCCESS
        response_data['msg'] = '删除机构成功'
        return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        return jsonify(response_data)



def edit_org(org_code):
    """
    编辑机构
    :return:
    :param: org_code    要编辑的机构的org_code
    by denghaolin
    """
    response_data = {
        'code': response.ERROR,
        'msg': '系统错误',
        'data': ''
    }
    logging.info('edit_org')
    try:
        if not org_code:
            response_data['msg'] = '请输入机构编码'
            return jsonify(response_data)
        org_obj = Sys_org.get_org_info(org_code)  # 获取待编辑的机构对象
        if not org_obj:
            response_data['msg'] = '该机构不存在'
            return jsonify(response_data)
        # 获取编辑信息
        params = request.values.to_dict() if request.values.to_dict() else json.loads(request.data)
        res_code, res_msg = Sys_org.edit_org(org_obj=org_obj, edit_data=params)
        if res_code == '0':
            response_data['code'] = response.SUCCESS
            response_data['msg'] = '机构更新成功'
            return jsonify(response_data)
        response_data['msg'] = res_msg
        return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        return jsonify(response_data)


def get_all_org_info():
    """
    获取所有机构的信息,用于新增机构时渲染所属机构
    :return:
    by denghaolin
    """
    response_data = {
        'code': response.ERROR,
        'msg': '系统错误',
        'data': ''
    }
    logging.info('get_all_org_info')
    try:
        all_org_obj_list = Sys_org.get_all_org_info()
        if not all_org_obj_list:
            return jsonify(response_data)
        org_data_dict = {}  # 机构信息列表
        for org_obj in all_org_obj_list:
            org_data_dict[org_obj.org_code] = org_obj.org_name
        response_data['data'] = org_data_dict
        response_data['msg'] = '查询成功'
        response_data['code'] = response.SUCCESS
        return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        raise e



def get_bank_card_type_code():
    """
    获取银行卡类型及编码
    :return:
    """
    logging.info("get_bank_card_type_code")
    try:
        res = SysDict.get_dict_list_by_type(dict_type='bank_card_type')
        bank_card_code_list = []  # 银行卡类型信息列表
        for bank_card_type in res:
            _dict = {}
            _dict["id"] = bank_card_type.dict_id
            _dict["name"] = bank_card_type.dict_name
            bank_card_code_list.append(_dict)
        response_data = {"code": response.SUCCESS, "msg": "查询成功", "data": bank_card_code_list}
        return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        response_data = {"code": response.ERROR, "msg": "查询失败", "data": []}
        return jsonify(response_data)



def get_org_type_bl_code_father_org():
    """
    获取机构新增编辑页面基本信息下拉框
    :return:
    by denghaolin
    """
    logging.info('get_org_type_bl_code_father_org')
    try:
        org_types = SysDict.get_dict_list_by_type_without_block_up(dict_type='sys_org_status')
        org_type_list = []  # 机构信息列表
        for type in org_types:
            _dict = {}
            _dict["id"] = type.dict_id
            _dict["name"] = type.dict_name
            org_type_list.append(_dict)
        bl_codes = SysDict.get_dict_list_by_type_without_block_up(dict_type='business_code')
        bl_code_list = []  # 经营类型信息列表
        for bl in bl_codes:
            _dict = {}
            _dict["id"] = bl.dict_id
            _dict["name"] = bl.dict_name
            bl_code_list.append(_dict)
        res_data = {
            'org_type': org_type_list,
            'bl_code': bl_code_list
        }
        response_data = {"code": response.SUCCESS, "msg": "查询成功", "data": res_data}
        return jsonify(response_data)
    except Exception as e:
        logging.debug(e)
        response_data = {"code": response.ERROR, "msg": "查询失败", "data": []}
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
        page = params.get('page')
        org_name = params.get('name', "")
        org_list = Sys_org.find_sysorg_without_myself(org_code=org_code, org_name=org_name, page=page)
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



def get_orgs_without_this_and_this_son():
    """
    通过当前机构code除去其和其子机构的 code：name键值对
    :return: code：name键值对
    """
    logging.info('get_orgs_without_this_and_this_son')
    response_data = {}
    try:
        params = request.args
        org_id = params.get('org_id')
        if org_id:
            org_code = Sys_org.objects(org_id=org_id).first().org_code
        else:
            org_code = params.get('org_code')
        page = params.get('page')
        org_name = params.get('name', "")
        org_list = Sys_org.find_other_sysorg(org_code=org_code, org_name=org_name, page=page)
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


def save_img(img, desc):
    """
    保存图片到本地
    :param img:
    :param desc:  图片描述
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
                image_path = path + '\\rich_base_provider\\static\\images\\sys_org\\'
            else:
                image_path = path + '/rich_base_provider/static/images/sys_org/'

            file = open(image_path + str(desc) + '.png', 'wb+')
            file.write(imgdata)
            file.close()
            image_url = str(desc) + '.png'
        return image_url
    except Exception as e:
        logging.debug(e)
        raise e


def check_edit_org(org_obj, org_name, mail, idcard_number, mobile):
    """
    判断参数是否已存在
    :param org_name:
    :param mail:
    :param idcard_number:
    :param mobile:
    :return:
    """
    logging.info('check_edit_org')
    error_msg = {}
    org = Sys_org.get_edit_by(org_obj=org_obj, org_name=org_name)
    if org:
        error_msg['org_name'] = '机构名已存在!'
    org = Sys_org.get_edit_by(org_obj=org_obj, mail=mail)
    if org:
        error_msg['mail'] = '邮箱已存在!'
    org = Sys_org.get_edit_by(org_obj=org_obj, idcard_number=idcard_number)
    if org:
        error_msg['idcard_number'] = '身份证号已存在!'
    org = Sys_org.get_edit_by(org_obj=org_obj, mobile=mobile)
    if org:
        error_msg['mobile'] = '联系电话已存在!'
    return error_msg
