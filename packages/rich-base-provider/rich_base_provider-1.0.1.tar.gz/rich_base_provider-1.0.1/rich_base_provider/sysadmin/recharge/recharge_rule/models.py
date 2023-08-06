#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 下午5:24
# @Author  : chenwanyue
# @File    : models.py

import re
import random
import datetime
from rich_base_provider import db
from flask_security import current_user
from rich_base_provider.sysadmin.sys_dict.models import SysDict


class RechargeRule(db.Document):
    """
    充值方案
    """
    meta = {
        "collection": "recharge_rule"
    }
    recharge_rule_id = db.StringField()  # 充值方案ID
    org_id = db.StringField()  # 本充值方案所属机构
    rule_name = db.StringField()  # 本充值方案名称
    recharge_condition = db.StringField()  # 充值方案满足条件（金额达到...）
    giving_count = db.StringField()  # 优惠金额数目
    rule_apply_type = db.StringField()  # 充值方案适用类型(0 角色 1 部门 ....)
    rule_apply_object = db.ListField(db.StringField(), default=[])  # 本充值方案适用对象 存储唯一标识
    rule_start_time = db.DateTimeField()  # 本规则活动开始时间
    rule_end_time = db.DateTimeField()  # 本规则活动结束时间

    status = db.StringField()  # 当前充值方案状态（启用（0） 停用（1） 删除（2））
    remarks = db.StringField()  # 规则备注

    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间

    @staticmethod
    def get_dict_id(dict_type, dict_name):
        dict_obj = SysDict.get_dict_by_type_and_name(dict_type=dict_type, dict_name=dict_name)
        return dict_obj.dict_id

    @classmethod
    def get_recharge_rule_list_by_data(cls, page=1, per_page=20, org_code="", search_data=""):
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
                         'localField': 'rule_apply_type',
                         'foreignField': 'dict_id',
                         'as': 'rule_apply_type_dict'
                         }},
            {'$unwind': "$rule_apply_type_dict"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"rule_apply_type_dict.dict_type": "recharge_apply_type"},
                    {"status_dict.dict_type": "recharge_status"},
                    {'status': {'$nin': [cls.get_dict_id("recharge_status", "删除")]}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {'rule_name': re.compile(search_data)},
                    {"rule_apply_type_dict.dict_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"recharge_condition": re.compile(search_data)},
                    {"giving_count": re.compile(search_data)},
                    {'remarks': re.compile(search_data)}
                ]
            }},
            {'$skip': start_index},
            {'$limit': int(per_page)},
            {'$sort': {"create_time": -1}},
            {'$project': {'recharge_rule_id': 1,
                          'sys_org.org_name': 1,
                          'rule_name': 1,
                          'recharge_condition': 1,
                          'giving_count': 1,
                          'rule_apply_type_dict.dict_name': 1,
                          'rule_start_time': 1,
                          'rule_end_time': 1,
                          'status_dict.dict_name': 1,
                          'remarks': 1,
                          'update_time': 1
                          }}
        ]
        return cls.objects.aggregate(*search)

    @classmethod
    def get_recharge_rule_total_count(cls, org_code, search_data):
        """
        获取充值方案总记录数
        :return:
        """
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
                         'localField': 'rule_apply_type',
                         'foreignField': 'dict_id',
                         'as': 'rule_apply_type_dict'
                         }},
            {'$unwind': "$rule_apply_type_dict"},

            {'$lookup': {'from': 'sys_dict',
                         'localField': 'status',
                         'foreignField': 'dict_id',
                         'as': 'status_dict'
                         }},
            {'$unwind': "$status_dict"},

            {'$match': {
                "$and": [
                    {"sys_org.org_code": re.compile(r'^{}'.format(org_code))},
                    {"rule_apply_type_dict.dict_type": "recharge_apply_type"},
                    {"status_dict.dict_type": "recharge_status"},
                    {'status': {'$nin': [cls.get_dict_id("recharge_status", "删除")]}}
                ],
                "$or": [
                    {"sys_org.org_name": re.compile(search_data)},
                    {'rule_name': re.compile(search_data)},
                    {"rule_apply_type_dict.dict_name": re.compile(search_data)},
                    {"status_dict.dict_name": re.compile(search_data)},
                    {"recharge_condition": re.compile(search_data)},
                    {"giving_count": re.compile(search_data)},
                    {'remarks': re.compile(search_data)}
                ]
            }},
            {'$sort': {"create_time": -1}},
            {'$group': {'_id': 0,
                        'count': {'$sum': 1}}}
        ]
        return list(cls.objects.aggregate(*search))[0].get('count')

    @classmethod
    def get_recharge_rule_all_by_data(cls, rule_apply_object, current_org_id, rule_apply_type):
        """
        根据充值方案 所属机构、适用对象查询所有启用状态下、并且还未过期的充值方案
        :param rule_apply_object:
        :param current_org_id:
        :param rule_apply_type:
        :return:
        """
        current_time = datetime.datetime.now()
        return cls.objects(status__in=[cls.get_dict_id("recharge_status", "启用")], org_id=current_org_id,
                           rule_apply_type__in=rule_apply_type,
                           rule_apply_object__in=rule_apply_object, rule_start_time__lte=current_time,
                           rule_end_time__gte=current_time)

    @classmethod
    def get_recharge_rule_list_by_kwargs(cls, **kwargs):
        """
        根据kwargs字典获取充值方案列表
        :param kwargs:
        :return:
        """
        org_id = kwargs.get("org_id")
        rule_apply_type = kwargs.get("rule_apply_type")
        if kwargs.get("rule_name"):
            return cls.objects(org_id=org_id, rule_apply_type=rule_apply_type, rule_name=kwargs.get("rule_name"),
                               status__nin=[cls.get_dict_id("recharge_status", "删除")]).all()
        if kwargs.get("recharge_condition") and kwargs.get("giving_count"):
            return cls.objects(org_id=org_id, rule_apply_type=rule_apply_type,
                               recharge_condition=kwargs.get("recharge_condition"),
                               giving_count=kwargs.get("giving_count"),
                               status__nin=[cls.get_dict_id("recharge_status", "删除")]).all()

    @classmethod
    def insert_recharge_rule_by_create_dict(cls, create_dict):
        """
        根据create_dict创建充值方案
        :param create_dict:
        :return:
        """
        recharge_rule_id = "RR" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 999999))
        login_user_code = current_user.user_code
        new_recharge_rule = RechargeRule(
            recharge_rule_id=recharge_rule_id,
            org_id=create_dict["org_id"],
            rule_name=create_dict["rule_name"],
            recharge_condition=str(create_dict["recharge_condition"]),
            giving_count=str(create_dict["giving_count"]),
            rule_apply_type=create_dict["rule_apply_type"],
            rule_apply_object=create_dict["rule_apply_object"],
            rule_start_time=create_dict["rule_start_time"],
            rule_end_time=create_dict["rule_end_time"],
            status=create_dict["status"],
            remarks=create_dict["remarks"],
            create_by=login_user_code,
            update_by=login_user_code,
            create_time=datetime.datetime.now(),
            update_time=datetime.datetime.now()
        )
        new_recharge_rule.save()

    @classmethod
    def get_recharge_rule_by_recharge_rule_id(cls, recharge_rule_id):
        """
        根据充值方案ID获取记录详细信息
        :param recharge_rule_id:
        :return:
        """
        return cls.objects(recharge_rule_id=recharge_rule_id,
                           status__nin=[cls.get_dict_id("recharge_status", "删除")]).first()

    @classmethod
    def update_recharge_rule_by_update_dict(cls, update_dict):
        """
        根据update_dict字典数据编辑充值方案记录
        :param update_dict:
        :return:
        """
        login_user_code = current_user.user_code
        old_recharge_rule = cls.get_recharge_rule_by_recharge_rule_id(update_dict["recharge_rule_id"])
        # 判断数据是否修改
        if old_recharge_rule.rule_apply_type != update_dict["rule_apply_type"]:
            old_recharge_rule.rule_apply_type = update_dict["rule_apply_type"]
        if old_recharge_rule.rule_apply_object != update_dict["rule_apply_object"]:
            old_recharge_rule.rule_apply_object = update_dict["rule_apply_object"]
        if old_recharge_rule.rule_name != update_dict["rule_name"]:
            old_recharge_rule.rule_name = update_dict["rule_name"]
        if old_recharge_rule.recharge_condition != str(update_dict["recharge_condition"]):
            old_recharge_rule.recharge_condition = str(update_dict["recharge_condition"])
        if old_recharge_rule.giving_count != str(update_dict["giving_count"]):
            old_recharge_rule.giving_count = str(update_dict["giving_count"])
        if old_recharge_rule.rule_start_time != update_dict["rule_start_time"]:
            old_recharge_rule.rule_start_time = update_dict["rule_start_time"]
        if old_recharge_rule.rule_end_time != update_dict["rule_end_time"]:
            old_recharge_rule.rule_end_time = update_dict["rule_end_time"]
        if old_recharge_rule.status != update_dict["status"]:
            old_recharge_rule.status = update_dict["status"]
        if old_recharge_rule.remarks != update_dict["remarks"]:
            old_recharge_rule.remarks = update_dict["remarks"]

        old_recharge_rule.update_by = login_user_code
        old_recharge_rule.update_time = datetime.datetime.now()
        old_recharge_rule.save()

    @classmethod
    def delete_recharge_rule_by_recharge_rule_id(cls, recharge_rule_id):
        """
        根据充值方案ID删除充值方案记录
        :param recharge_rule_id:
        :return:
        """
        login_user_code = current_user.user_code
        delete_recharge_rule = cls.get_recharge_rule_by_recharge_rule_id(recharge_rule_id)
        delete_recharge_rule.status = cls.get_dict_id("recharge_status", "删除")
        delete_recharge_rule.update_by = login_user_code
        delete_recharge_rule.update_time = datetime.datetime.now()
        delete_recharge_rule.save()
