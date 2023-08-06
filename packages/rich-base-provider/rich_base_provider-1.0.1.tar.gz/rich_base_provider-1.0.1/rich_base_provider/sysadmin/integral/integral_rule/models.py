#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 下午5:07
# @Author  : chenwanyue
# @File    : models.py

import re
import random
import datetime
from rich_base_provider import db
from flask_security import current_user
from rich_base_provider.sysadmin.sys_dict.models import SysDict


class IntegralRule(db.Document):
    """
    积分规则
    """
    meta = {
        "collection": "integral_rule"
    }
    integral_rule_id = db.StringField()  # 积分规则ID
    org_id = db.StringField()  # 本积分规格所属机构
    integral_rule_type = db.StringField()  # 积分规则类型（消费（0）、充值（1）、系统（2）...）
    child_rule_type = db.StringField(default="")  # 子规则类型 作为integral_rule_type的子规则类型
    integral_condition = db.IntField()  # 积分规则成立条件（金额（消费、充值））
    receive_integral_count = db.IntField(default=0)  # 得到的积分数目
    status = db.StringField()  # 当前积分规则状态（启用（0）、停用（1）、删除（2））
    remarks = db.StringField()  # 规则备注

    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间

    @staticmethod
    def get_dict_id(dict_type, dict_name):
        status_value = SysDict.get_dict_by_type_and_name(dict_type=dict_type, dict_name=dict_name)
        return status_value.dict_id

    @classmethod
    def get_integral_rule_list_by_data(cls, page=1, per_page=20, org_code="", search_data=""):
        """
        根据页码、搜索条件查询指定数目记录
        :param page:
        :param per_page:
        :param org_code:
        :param search_data:
        :return:
        """
        start_index = (int(page) - 1) * int(per_page)
        search = [
            {
                '$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_id',
                    'foreignField': 'org_id',
                    'as': 'sys_org'
                }
            },
            {'$unwind': "$sys_org"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'integral_rule_type',
                         'foreignField': 'dict_id',
                         'as': 'integral_rule_type_dict'
                         }},
            {'$unwind': "$integral_rule_type_dict"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"status_dict.dict_type": "integral_status"},
                    {"integral_rule_type_dict.dict_type": "integral_rule_type"},
                    {'status': {'$nin': [cls.get_dict_id("integral_status", "删除")]}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {"integral_rule_type_dict.dict_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"integral_condition": re.compile(search_data)},
                    {"receive_integral_count": re.compile(search_data)},
                    {'remarks': re.compile(search_data)}
                ]
            }},
            {'$skip': start_index},
            {'$limit': int(per_page)},
            {'$sort': {"create_time": -1}},
            {'$project': {'integral_rule_id': 1,
                          'sys_org.org_name': 1,
                          'integral_rule_type_dict.dict_name': 1,
                          'child_rule_type': 1,
                          'integral_condition': 1,
                          'receive_integral_count': 1,
                          'status_dict.dict_name': 1,
                          'remarks': 1,
                          'update_time': 1
                          }}
        ]
        return cls.objects.aggregate(*search)

    @classmethod
    def get_integral_rule_total_count(cls, org_code, search_data):
        """获取积分规则记录总数"""
        search = [
            {
                '$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_id',
                    'foreignField': 'org_id',
                    'as': 'sys_org'
                }
            },
            {'$unwind': "$sys_org"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'integral_rule_type',
                         'foreignField': 'dict_id',
                         'as': 'integral_rule_type_dict'
                         }},
            {'$unwind': "$integral_rule_type_dict"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"status_dict.dict_type": "integral_status"},
                    {"integral_rule_type_dict.dict_type": "integral_rule_type"},
                    {'status': {'$nin': [cls.get_dict_id("integral_status", "删除")]}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {"integral_rule_type_dict.dict_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"integral_condition": re.compile(search_data)},
                    {"receive_integral_count": re.compile(search_data)},
                    {'remarks': re.compile(search_data)}
                ]
            }},
            {'$sort': {"create_time": -1}},
            {'$group': {'_id': 0,
                        'count': {'$sum': 1}}}
        ]
        return list(cls.objects.aggregate(*search))[0].get('count')

    @classmethod
    def get_org_integral_rule_list_by_data(cls, current_org_id, integral_condition):
        """
        根据积分规则所属机构以及满足金额获取本机构启用状态下的积分规则
        :param current_org_id:
        :param integral_condition:
        :return:
        """
        return cls.objects(org_id=current_org_id, status__in=[cls.get_dict_id("integral_status", "启用")],
                           integral_rule_type=cls.get_dict_id("integral_rule_type", "充值"),
                           integral_condition__lte=integral_condition).order_by("-integral_condition").all()

    @classmethod
    def get_integral_rule_list_by_kwargs(cls, **kwargs):
        """
        根据kwargs字典获取积分规则数据
        :param kwargs:
        :return:
        """
        org_id = kwargs.get("org_id", "")
        integral_rule_type = kwargs.get("integral_rule_type", "")
        child_rule_type = kwargs.get("child_rule_type", "")
        integral_condition = kwargs.get("integral_condition", "")
        receive_integral_count = kwargs.get("receive_integral_count", "")
        if org_id and integral_rule_type and child_rule_type and integral_condition and receive_integral_count:
            return cls.objects(org_id=org_id, integral_rule_type=integral_rule_type, child_rule_type=child_rule_type,
                               integral_condition=integral_condition,
                               receive_integral_count=receive_integral_count,
                               status__nin=[cls.get_dict_id("integral_status", "删除")]).all()
        elif org_id and integral_rule_type and integral_condition and receive_integral_count:
            return cls.objects(org_id=org_id, integral_rule_type=integral_rule_type,
                               integral_condition=int(integral_condition),
                               receive_integral_count=int(receive_integral_count),
                               status__nin=[cls.get_dict_id("integral_status", "删除")]).all()

    @classmethod
    def insert_integral_rule_by_create_dict(cls, create_dict):
        """
        根据create_dict创建积分规则
        :param create_dict:
        :return:
        """
        integral_rule_id = "IR" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 999999))
        login_user_code = current_user.user_code
        new_integral_rule = IntegralRule(
            integral_rule_id=integral_rule_id,
            org_id=create_dict["org_id"],
            integral_rule_type=create_dict["integral_rule_type"],
            child_rule_type=create_dict["child_rule_type"],
            integral_condition=create_dict["integral_condition"],
            receive_integral_count=create_dict["receive_integral_count"],
            status=create_dict["status"],
            remarks=create_dict["remarks"],
            create_by=login_user_code,
            update_by=login_user_code,
            create_time=datetime.datetime.now(),
            update_time=datetime.datetime.now()
        )
        new_integral_rule.save()

    @classmethod
    def get_integral_rule_by_integral_rule_id(cls, integral_rule_id):
        """
        根据积分规则ID获取本记录详细信息
        :param integral_rule_id:
        :return:
        """
        return cls.objects(integral_rule_id=integral_rule_id,
                           status__nin=[cls.get_dict_id("integral_status", "删除")]).first()

    @classmethod
    def update_integral_rule_by_update_dict(cls, update_dict):
        """
        根据update_dict字典数据编辑积分规则记录
        :param update_dict:
        :return:
        """
        login_user_code = current_user.user_code
        old_integral_rule = cls.get_integral_rule_by_integral_rule_id(update_dict["integral_rule_id"])
        # 判断数据是否修改
        if old_integral_rule.integral_rule_type != update_dict["integral_rule_type"]:
            old_integral_rule.integral_rule_type = update_dict["integral_rule_type"]
        if old_integral_rule.child_rule_type != update_dict["child_rule_type"]:
            old_integral_rule.child_rule_type = update_dict["child_rule_type"]
        if old_integral_rule.integral_condition != update_dict["integral_condition"]:
            old_integral_rule.integral_condition = update_dict["integral_condition"]
        if old_integral_rule.receive_integral_count != update_dict["receive_integral_count"]:
            old_integral_rule.receive_integral_count = update_dict["receive_integral_count"]
        if old_integral_rule.status != update_dict["status"]:
            old_integral_rule.status = update_dict["status"]
        if old_integral_rule.remarks != update_dict["remarks"]:
            old_integral_rule.remarks = update_dict["remarks"]

        old_integral_rule.update_by = login_user_code
        old_integral_rule.update_time = datetime.datetime.now()
        old_integral_rule.save()

    @classmethod
    def delete_integral_rule_by_integral_rule_id(cls, integral_rule_id):
        """
        根据积分规则编号删除积分规则记录
        :param integral_rule_id:
        :return:
        """
        login_user_code = current_user.user_code
        delete_integral_rule = cls.get_integral_rule_by_integral_rule_id(integral_rule_id)
        delete_integral_rule.status = cls.get_dict_id("integral_status", "删除")
        delete_integral_rule.update_by = login_user_code
        delete_integral_rule.update_time = datetime.datetime.now()
        delete_integral_rule.save()
