#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 下午3:49
# @Author  : Lee才晓
# @File    : views.py
# @Function: 字典


import xlrd
from flask import jsonify, request
from werkzeug.utils import secure_filename
from rich_base_provider import response
from rich_base_provider.sysadmin.sys_dict.models import *
from rich_base_provider.utils import *


def query_dict_list():
    """
    查询字典列表
    :return:
    """
    logging.info("query_dict_list")
    response_data = {}
    result_list = []
    try:
        # 接收参数
        params = request.values.to_dict()
        # 判断参数是否完整
        search_data = params.get("search_data")
        if not search_data:
            search_data = ''
        page = int(params.get("page", ""))
        per_page = params.get("per_page")
        sort = params.get('sort') if params.get('sort') else 'create_time'
        sortOrder = params.get('sortOrder')
        if sortOrder == 'desc':
            sortOrder = '-'
        elif sortOrder == 'asc':
            sortOrder = ''
        # 查找字典列表
        dict_list, dict_count = SysDict.get_dict_list_by_search_content(search_data,page,per_page, sort, sortOrder)
        for dict_info in dict_list:
            result_list.append({"dict_code": dict_info.dict_code,
                                "dict_id": dict_info.dict_id,
                                "dict_name": dict_info.dict_name,
                                "dict_type": dict_info.dict_type,
                                "description": dict_info.description,
                                "remarks": dict_info.remarks,
                                "sort": dict_info.sort,
                                "status": SysDict.status_dict[dict_info.status]})
        return jsonify({'rows': result_list, 'total': dict_count})
    except Exception as e:
        # 捕获异常
        logging.debug(e)
        return jsonify({'rows':[],'total':0})



def add_dict():
    """
    新增字典信息
    :return:
    """
    logging.info("add_dict")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ["dict_id", 'dict_name', 'dict_type', 'description', 'status', 'sort']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""
                break

        if not response_data:
            # 判断字典是否已存在
            old_dict = SysDict.get_dict_by_type_and_name(params.get("dict_type"), params.get("dict_name"))
            if old_dict:
                response_data['code'] = response.ERROR
                response_data['msg'] = response.RESULT_EXIST_ERROR
                response_data['data'] = ""
            else:
                # 新增字典
                SysDict.create_dict(params)
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


def update_dict():
    """
    更新字典信息
    :return:
    """
    logging.info("update_dict")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        check_data = ['dict_code', 'dict_id', "dict_name", 'dict_type', 'description', 'status', 'sort']
        for data in check_data:
            if not params.get(data):
                response_data['code'] = response.PARAMETER_ERROR
                response_data['msg'] = response.RESULT_PARAMETER_ERROR
                response_data['data'] = ""

        if not response_data:
            # 判断字典是否存在
            dict_obj = SysDict.get_dict_by_type_and_name(params.get('dict_type'), params.get('dict_name'))
            if dict_obj and dict_obj.dict_code != params.get('dict_code'):
                response_data['code'] = response.ERROR
                response_data['msg'] = "该字典已存在"
                response_data['data'] = ""
            else:
                # 更新字典
                SysDict.update_dict_info(params)
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


def delete_dict():
    """
    删除指定字典
    :return:
    """
    logging.info("delete_dict")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        if params.get("dict_code_list"):
            SysDict.deleted(params.get("dict_code_list"))
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


def block_up_dict():
    """
    停用指定字典
    :return:
    """
    logging.info("block_up_dict")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        if params.get("dict_code_list"):
            SysDict.block_up(params.get("dict_code_list"))
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


def get_dict_info():
    """
    获取字典详情
    :return:
    """
    logging.info("get_dict_info")
    response_data = {}
    try:
        # 接收参数
        params = request.get_json()
        # 判断参数是否完整
        if params.get("dict_code"):
            dict_info = SysDict.get_dict_info(params.get("dict_code"))
            if dict_info:
                response_data['code'] = response.SUCCESS
                response_data['msg'] = response.RESULT_SUCCESS
                response_data['data'] = {"dict_code": dict_info.dict_code,
                                         "dict_id": dict_info.dict_id,
                                         "dict_name": dict_info.dict_name,
                                         "dict_type": dict_info.dict_type,
                                         "description": dict_info.description,
                                         "remarks": dict_info.remarks,
                                         "sort": dict_info.sort,
                                         "status": dict_info.status}
            else:
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



def import_dict():
    """
    上传字典文件
    :return:
    """
    logging.info("import_dict")
    response_data = {}
    try:
        file = request.files['file']
        file_path = import_excel(file)
        if file_path:
            response_data['code'] = response.ERROR
            response_data['data'] = ""
            response_data['msg'] = '文件格式不匹配!'
        else:

            if read_excel(file_path):
                response_data['code'] = response.SUCCESS
                response_data['data'] = ""
                response_data['msg'] = response.RESULT_SUCCESS

            else:
                response_data['code'] = response.ERROR
                response_data['data'] = ""
                response_data['msg'] = '文件内容不匹配!'

    except Exception as e:
        logging.debug(e)
        response_data['code'] = response.ERROR
        response_data['msg'] = response.RESULT_ERROR
        response_data['data'] = ""
    finally:
        return jsonify(response_data)


def import_excel(file):
    """
    上传文件
    :param file:
    :return:
    """
    logging.info('import_excel')
    try:
        if check_file_extensions(file.filename, getDictAllowdExtensions()):

            username = session.get("username", "")

            temporary_file = username + "-" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            basepath = os.path.dirname(__file__)  # 当前文件所在路径

            current_system = platform.system()
            if current_system == 'Windows':
                current_path = '..\\..\\static\\temporary\\dict_files\\'
            else:
                current_path = '../../static/temporary/dict_files'

            upload_path = os.path.join(basepath, current_path,
                                       secure_filename(temporary_file))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            file.save(upload_path)
            return upload_path
        else:
            return False
    except Exception as e:
        logging.debug(e)
        raise e


def read_excel(file_path):
    """
    读取excel文件
    :param file_path: 文件路径
    :return:
    """
    logging.info('read_excel')
    try:
        data = xlrd.open_workbook(file_path)

        Sheets = data.sheets()  # 获取工作表list。

        the_Sheet = Sheets[0]  # 获取工作表
        nrows = the_Sheet.nrows  # 行数
        ncols = the_Sheet.ncols  # 列数

        if not is_eligible_files(get_dict_keys(), ncols, the_Sheet.row_values(0)):
            return False

        dict_list = SysDict.get_dict_list_by_file(the_Sheet, nrows)
        if dict_list:
            SysDict.batch_insert(dict_list)

        # 删除临时文件
        # if os.path.isfile(file_path):
        #     os.remove(file_path)
        return True
    except Exception as e:
        logging.debug(e)
        raise e
