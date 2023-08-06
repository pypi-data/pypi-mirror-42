#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 下午3:49
# @Author  : Lee才晓
# @File    : models.py
# @Function: 字典模块


import datetime
import time
import logging
from flask_security import current_user
import re
from rich_base_provider import db

dict_status_normal = 1
dict_status_block_up = 2
dict_status_delete = 3

dict_normal = "正常"
dict_block_up = "停用"
dict_delete = "删除"


class SysDict(db.Document):
    """
    字典信息表
    """
    meta = {
        'collection': 'sys_dict'
    }
    dict_code = db.StringField(unique=True, required=False)  # 字典编码
    dict_id = db.StringField()  # 字典ID
    dict_name = db.StringField()  # 字典名称
    dict_type = db.StringField()  # 字典类型
    description = db.StringField()  # 类型描述
    sort = db.IntField()  # 排序
    remarks = db.StringField()
    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间
    status = db.IntField(choices=[dict_status_normal, dict_status_block_up, dict_status_delete],
                         default=dict_status_normal)  # 状态("1",正常，"2":停用 , "3":删除)
    # 字典状态
    status_dict = {dict_status_normal: dict_normal, dict_status_block_up: dict_block_up,
                   dict_status_delete: dict_delete}


    @classmethod
    def get_filetype_first_list(cls,dict_type):
        """
        查询所有文件类型种类
        :param dict_type:
        :return:
        """
        return cls.objects(dict_type__exact=dict_type).all()

    @classmethod
    def get_filetype_all_lsit(cls,type_list):
        """
        获取所有资源类型 名称
        :param type_list:
        :return:
        """
        return cls.objects(dict_type__in=type_list).all()

    @classmethod
    def deleted(cls, dict_code_list):
        """
        删除字典数据
        :return:
        """
        try:

            cls.objects(dict_code__in=dict_code_list).update(set__status=dict_status_delete,
                                                             set__update_time=datetime.datetime.now(),
                                                             set__update_by=current_user.user_code)

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def block_up(cls, dict_code_list):
        """
        停用字典数据
        :return:
        """

        try:

            cls.objects(dict_code__in=dict_code_list).update(set__status=dict_status_block_up,
                                                             set__update_time=datetime.datetime.now(),
                                                             set__update_by=current_user.user_code)

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_dict_info(cls, dict_code):
        """
        获取字典信息
        :return:
        """
        return cls.objects(dict_code=dict_code).first()

    @classmethod
    def get_dict_by_type_and_name(cls, dict_type, dict_name):
        """
        根据类型与字典名获取对象
        :return:
        """
        return cls.objects(dict_type=dict_type, dict_name=dict_name,
                           status__in=[dict_status_normal, dict_status_block_up]).first()

    @classmethod
    def get_dict_info_by_type_and_id(cls, dict_type, dict_id):
        """
        根据字典类型和字典id，获取字典信息
        :return:
        """
        try:
            if not dict_type or not dict_id:
                return None

            return cls.objects(dict_type=dict_type, dict_id=dict_id,
                               status__in=[dict_status_normal, dict_status_block_up]).first()

        except Exception as e:
            logging.debug(e)

    @classmethod
    def get_dict_list_by_type(cls, dict_type):
        """
        获取字典类型的所有字典
        :param dict_type:
        :return:
        """
        return cls.objects(dict_type=dict_type, status__in=[dict_status_normal, dict_status_block_up]).all()

    @classmethod
    def get_dict_list_by_type_and_name_list(cls, dict_type, dict_name_list):
        """
        根据类型与字典名列表获取相关的字典列表
        :param dict_type:
        :param dict_name_list:
        :return:
        """
        return cls.objects(dict_type=dict_type, dict_name__in=dict_name_list,
                           status__in=[dict_status_normal, dict_status_block_up]).all()

    @classmethod
    def create_dict(cls, info):
        """
        新增字典信息
        :param info:
        :return:
        """
        try:

            dict_obj = SysDict(dict_code=cls.get_new_dict_code(),
                               dict_name=info.get("dict_name", ""),
                               dict_id=info.get("dict_id", ""),
                               dict_type=info.get("dict_type", ""),
                               description=info.get("description", ""),
                               remarks=info.get("remarks", ""),
                               sort=info.get("sort", ""),
                               create_by=current_user.user_code,
                               create_time=datetime.datetime.now(),
                               update_by=current_user.user_code,
                               update_time=datetime.datetime.now(),
                               status=info.get("status", dict_status_normal))
            dict_obj.save()

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_new_dict_code(cls):
        """
        获取新的字典编码,以D开头加秒级时间戳
        :return:
        """
        return "D" + str(round(time.time()))

    @classmethod
    def update_dict_info(cls, new_info):
        """
        更新字典内容
        :param new_info:
        :return:
        """
        try:
            cls.objects(dict_code=new_info.get("dict_code")).update_one(set__dict_id=new_info.get("dict_id"),
                                                                        set__dict_name=new_info.get("dict_name"),
                                                                        set__dict_type=new_info.get("dict_type"),
                                                                        set__description=new_info.get("description"),
                                                                        set__remarks=new_info.get("remarks"),
                                                                        set__sort=new_info.get("sort"),
                                                                        set__update_by=current_user.user_code,
                                                                        set__update_time=datetime.datetime.now(),
                                                                        set__status=new_info.get("status"))

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_dict_list_by_search_content(cls, search_data, page=1, per_page=20, sort='create_time', sortOrder=-1):
        """
        通过搜索获取字典列表
        :return:
        """
        try:

            search_list = [k for k, v in cls.status_dict.items() if v == search_data and v is not dict_delete]
            search = {
                '__raw__': {
                    'status': {'$in': [dict_status_normal, dict_status_block_up]},
                }
            }

            if search_list:
                search['__raw__']['status'] = {'$in': search_list}
            else:
                search_list = [{'dict_name': re.compile(search_data)},
                               {'dict_type': re.compile(search_data)},
                               {'description': re.compile(search_data)},
                               {'remarks': re.compile(search_data)}]
                search['__raw__']['status'] = {'$in': [dict_status_normal, dict_status_block_up]}
                search['__raw__']['$or'] = search_list

            dict_list = cls.objects(**search).order_by(sortOrder + sort).skip(int(page)).limit(
                int(per_page)).all()
            dict_count = cls.objects(**search).count()

            return dict_list, dict_count
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_dict_list_by_file(cls, sheets, nrows):
        """
        从文件中获取字典信息
        :return:
        """
        try:
            dict_list = []
            new_dict_code = cls.get_new_dict_code()
            for i in range(1, nrows):
                dict_list.append(SysDict(dict_code=new_dict_code + str(i),
                                         dict_name=sheets.row_values(i)[0],
                                         dict_id=sheets.row_values(i)[1],
                                         dict_type=sheets.row_values(i)[2],
                                         description=sheets.row_values(i)[3],
                                         sort=sheets.row_values(i)[4],
                                         create_by=sheets.row_values(i)[5],
                                         create_time=sheets.row_values(i)[6],
                                         update_by=sheets.row_values(i)[7],
                                         update_time=sheets.row_values(i)[8],
                                         remarks=sheets.row_values(i)[9],
                                         status=sheets.row_values(i)[10]))

            return dict_list
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def batch_insert(cls, dict_list):
        """
        批量写入
        :param dict_list:
        :return:
        """
        try:
            cls.objects.insert(dict_list)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_dict_count(cls):
        """
        获取字典总数
        :return:
        """
        return cls.objects(status__in=[dict_status_normal, dict_status_block_up]).count()

    @classmethod
    def get_dict_list_by_type_without_block_up(cls, dict_type):
        """
        获取字典类型除去删除和停用的所有字典
        :param dict_type:
        :return:
        """
        return cls.objects(dict_type=dict_type, status__in=[dict_status_normal]).all()

    @classmethod
    def get_dict_list_by_type_list(cls, dict_type_list):
        """
        获取字典类型列表中的所有字典
        :param dict_type_list:
        :return:
        """
        return cls.objects(dict_type__in=dict_type_list, status__in=[dict_status_normal]).order_by("dict_type").all()