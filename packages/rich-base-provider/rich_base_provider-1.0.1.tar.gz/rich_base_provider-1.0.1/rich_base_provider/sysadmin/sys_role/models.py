#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 13:50
# @Author  : chenwanyue
# @Site    : www.rich-f.com
# @File    : models.py
# @Software: Rich Web Platform
# @Function: 角色管理模型

import logging
import datetime as dt
import re
from rich_base_provider import db
from flask_security import RoleMixin
from flask import session
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from flask_security import current_user

dict_status_normal = 0
dict_status_block_up = 1
dict_status_delete = 2

dict_normal = "正常"
dict_block_up = "停用"
dict_delete = "删除"


class Role(db.Document, RoleMixin):
    """
        角色信息表
    """
    meta = {
        "collection": "sys_role"
    }
    name = db.StringField(max_length=255)  # 角色名称
    role_code = db.StringField(unique=True)  # 角色编号 不可重复
    org_code = db.StringField()  # (存储机构编号)
    description = db.StringField()  # 角色描述 对于本角色的一些说明信息
    create_time = db.DateTimeField(default=dt.datetime.utcnow)  # 本记录创建时间(2018-6-6 6:12:54) 精确至秒
    update_time = db.DateTimeField()  # 本记录修改时间(2018-6-6 6:12:54) 精确至秒
    create_by = db.StringField()  # 本记录创建人 记录此人唯一标识 ID 或者 编号
    update_by = db.StringField()  # 本记录修改人 记录此人唯一标识 ID 或者 编号
    role_status = db.IntField(choices=[dict_status_normal, dict_status_block_up],
                              default=dict_status_normal)  # 本角色状态(0 正常 1 停用 2 删除)
    # 状态字典
    status_dict = {dict_status_normal: dict_normal, dict_status_block_up: dict_block_up,
                   dict_status_delete: dict_delete}

    def __repr__(self):
        """
        设置str返回值
        :return
        """
        return '<Role({name!r})>'.format(name=self.name)

        # 字典相关操作

        # 字典相关操作

    @staticmethod
    def get_status(dict_name):
        """状态"""
        data = SysDict.get_dict_by_type_and_name(dict_type='sys_role_status', dict_name=dict_name)
        return data

    @classmethod
    def get_role_by_org(cls, org_code, searchdata="", page=1, per_page=12, sort='create_time', sortOrder=-1):
        """
        分页查询机构角色信息
        :param page:
        :param org_code_list
        :param per_page
        :param type
        :return:
        """
        logging.info('get_role_by_org')
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search_list = [k for k, v in cls.status_dict.items() if v == searchdata and v is not dict_delete]
            search = [
                {'$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_code',
                    'foreignField': 'org_code',
                    'as': 'sys_org'
                }},
                {'$unwind': "$sys_org"},
            ]

            if search_list:
                search.append({'$match': {'$and': [{"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                                                   {"sys_org.status": {"$in": [0, 1]}},
                                                   {'role_status': {'$in': search_list}}
                                                   ]},
                               })
            else:
                search.append({'$match': {'$and': [{"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                                                   {"sys_org.status": {"$in": [0, 1]}},
                                                   {'role_status': {'$in': [dict_status_normal, dict_status_block_up]}}
                                                   ],
                                          "$or": [{"sys_org.org_name": re.compile(r'^{}'.format(searchdata))},
                                                  {'name': re.compile(searchdata)},
                                                  {'description': re.compile(searchdata)},
                                                  ]},
                               })

            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})

            count_obj = list(cls.objects.aggregate(*search))

            if len(count_obj):
                count = count_obj[0]["count"]
            else:
                count = 0

            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$sort': {sort: sortOrder}})
            search.append({'$project': {'name': 1, 'role_code': 1, 'description': 1, 'role_status': 1, 'org_code': 1,
                                        "sys_org.org_name": 1}})

            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})

            user_list = list(cls.objects.aggregate(*search))
            return {"user_list": user_list, "count": count}

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_total_count(cls, org_code_list):
        """
        获取记录总数
        :param org_code_list:
        :return:
        """
        return cls.objects(org_code__in=org_code_list,
                           role_status__in=[dict_status_normal, dict_status_block_up]).order_by(
            "-org_code").count()

    @classmethod
    def get_role_info(cls, role_code):
        """
        根据机角色编号获取角色信息
        :param role_code:
        :return:
        """
        return cls.objects(role_code=role_code, role_status__in=[dict_status_normal, dict_status_block_up]).first()

    @classmethod
    def insert_role(cls, create_dict):
        """
        创建新角色
        :param create_dict:
        :return:
        """
        try:
            role = Role(name=create_dict["role_name"],
                        role_code=create_dict["role_code"],
                        org_code=create_dict["org_code"],
                        role_status=create_dict["role_status"],
                        description=create_dict["role_desc"],
                        create_time=dt.datetime.now(),
                        update_time=dt.datetime.now(),
                        create_by=current_user.user_code,
                        update_by=current_user.user_code
                        )
            role.save()

        except Exception as e:
            logging.debug(e)
            return None

    @classmethod
    def delete_role(cls, role_code):
        """
        根据角色编号删除角色
        :param org_code:
        :param role_code:
        :param update_time
        :param login_org_code
        :return:
        """
        try:

            cls.objects(role_code=role_code).update(set__role_status=dict_status_delete,
                                                    set__update_time=dt.datetime.now(),
                                                    set__update_by=current_user.user_code)

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def update_role_info(cls, new_info):
        """
        更新字典内容
        :param new_info:
        :return:
        """
        try:

            logging.info(new_info.get("role_code"))
            cls.objects(role_code=new_info.get("role_code")).update_one(set__org_code=new_info.get("org_code"),
                                                                        set__role_code=new_info.get("new_role_code"),
                                                                        set__name=new_info.get("role_name"),
                                                                        set__description=new_info.get("role_desc"),
                                                                        set__role_status=int(
                                                                            new_info.get("role_status")),
                                                                        set__update_by=current_user.user_code,
                                                                        set__update_time=dt.datetime.now())

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def update_role_info_by_role_code(cls, new_info):
        """
        更新字典内容
        :param new_info:
        :return:
        """
        try:
            logging.info(new_info.get("role_code"))
            role = cls.objects(role_code=new_info.get("role_code")).first()
            role.name = new_info.get("role_name")
            role.description = new_info.get("role_desc")
            role.role_status = int(new_info.get("role_status"))
            role.update_by = current_user.user_code
            role.update_time = dt.datetime.now()
            role.save()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def judge_role_name(cls, org_code, role_name):
        """
        判断本机构是否存在此角色名称的角色对象
        :param org_code:
        :param role_name:
        :return:
        """
        return cls.objects(org_code=org_code, name=role_name,
                           role_status__in=[dict_status_normal, dict_status_block_up]).first()

    @classmethod
    def get_role_code_new(cls, org_code):
        """
        根据机构编号获取本机构最新角色编号 已删除的角色 其角色编号不复用
        :return:
        """

        # 获取role_code最大的role对象
        new_role = Role.objects(org_code=org_code).only("role_code").order_by(
            "-role_code").first()

        if not new_role:
            return "0"
        else:
            return new_role.role_code

    @classmethod
    def create_role_code(cls, org_code):
        """
        创建一个角色编号 规则：org_code-0001、0002自增字段
        :return:
        """
        # 根据机构编号获取本机构最大角色编号
        new_role_code = Role.get_role_code_new(org_code)
        if new_role_code == "0":
            dict_data = SysDict.get_dict_info_by_type_and_id("org_code", "1").description
            # 创建的角色为本机构第一个角色 admin
            return str(org_code) + "-" + dict_data
        else:
            count_role_code = str(int(new_role_code[-4:]) + 1)
            # 自动补充0
            return str(org_code) + "-" + str(count_role_code.zfill(4))

    @classmethod
    def get_role_by_org_code(cls, org_code):
        """
        根据机构编号查询本机构及其旗下子机构所有角色信息
        :param org_code:
        :return:
        """
        logging.info('get_role_by_org_code')
        try:
            search = {
                '__raw__': {
                    'role_status': {'$in': [dict_status_normal, dict_status_block_up]},
                    'org_code': re.compile(r'^{}'.format(org_code))
                }
            }
            return cls.objects(**search).all()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_role_list(cls, org_code):
        """
        根据机构编号查询本机构（不包含子机构）所有角色对象
        :param org_code:
        :return:
        """
        return cls.objects(org_code=org_code, role_status__in=[dict_status_normal, dict_status_block_up]).all()

    @classmethod
    def get_normal_role_list(cls, org_code):
        """
        根据机构编号查询本机构（不包含子机构）状态为正常的角色对象
        :param org_code:
        :return:
        """
        return cls.objects(org_code=org_code, role_status=dict_status_normal).all()

    @classmethod
    def get_role_list_by_code(cls, role_code):
        """
        根据角色编号获取角色列表
        :param role_code:
        :return:
        """
        return cls.objects(role_code__in=role_code,
                           role_status=dict_status_normal).all()

    @classmethod
    def get_role_dict_by_org_id(cls, org_id, role_name="", page=1, per_page=12):
        """
        通过机构id获取角色信息
        :param org_id:
        :param page:
        :param per_page:
        :return:
        by: wangwei
        """

        try:
            org = Sys_org.objects(org_id=org_id).first()
            org_code = org.org_code
            search = {
                '__raw__': {
                    'name': re.compile(role_name),
                    'org_code': re.compile(r"^" + org_code + ".*$"),
                    'role_status': {'$ne': 2}
                },
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            role_list = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            logging.info(role_list)
            count = cls.objects(**search).count()
            return {"role_list": role_list, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_role_list_by_role_code_org_code(cls, org_code, role_code_list=[], page=1, per_page=12, search_data=""):
        """
        根据角色编号以及机构编号 获取属于此机构的角色信息
        :param org_code:
        :param role_code_list:
        :param page:
        :param per_page:
        :param search_data:
        :return:
        """
        start_index = (int(page) - 1) * int(per_page)
        search = [
            {
                '$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_code',
                    'foreignField': 'org_code',
                    'as': 'sys_org'
                }
            },
            {'$unwind': "$sys_org"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'role_status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"status_dict.dict_type": "sys_role_status"},
                    {'role_code': {'$in': role_code_list}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"name": re.compile(search_data)},
                    {"description": re.compile(search_data)},
                ]
            }},
            {'$skip': start_index},
            {'$limit': int(per_page)},
            {'$sort': {"create_time": -1}},
            {'$project': {'_id': 0,
                          'role_code': 1,
                          'name': 1,
                          'sys_org.org_name': 1,
                          'status_dict.dict_name': 1,
                          'description': 1,
                          'update_time': 1
                          }}
        ]
        return cls.objects.aggregate(*search)

    @classmethod
    def get_role_list_by_role_code_org_code_total_count(cls, org_code, role_code_list=[], search_data=""):
        """
        根据角色编号以及机构编号 获取属于此机构的角色信息记录数目
        :param org_code:
        :param role_code_list:
        :param search_data:
        :return:
        """
        search = [
            {
                '$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_code',
                    'foreignField': 'org_code',
                    'as': 'sys_org'
                }
            },
            {'$unwind': "$sys_org"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'role_status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"status_dict.dict_type": "sys_role_status"},
                    {'role_code': {'$in': role_code_list}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"name": re.compile(search_data)},
                    {"description": re.compile(search_data)},
                ]
            }},
            {'$sort': {"create_time": -1}},
            {'$group': {'_id': 0,
                        'count': {'$sum': 1}}}
        ]
        return list(cls.objects.aggregate(*search))[0].get('count')
