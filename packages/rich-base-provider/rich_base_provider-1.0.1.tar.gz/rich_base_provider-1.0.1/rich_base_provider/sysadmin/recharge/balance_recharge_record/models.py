#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/01 下午5:30
# @Author  : chenwanyue
# @File    : models.py

import random
import datetime
from rich_base_provider import db
from flask_security import current_user
from rich_base_provider.sysadmin.sys_dict.models import SysDict


class BalanceRechargeRecord(db.Document):
    """
    余额充值记录(用户个人、机构余额充值)
    """
    meta = {
        "collection": "balance_recharge_record"
    }
    record_id = db.StringField()  # 充值记录ID
    recharge_object_type = db.StringField()  # 充值对象类型（用户充值（0） 机构充值（1））
    recharge_object_code = db.StringField()  # 充值对象编号（机构ID、用户编号）
    recharge_money_count = db.StringField()  # 充值金额（可接受至两位小数（分））
    recharge_rule_id = db.StringField(default="")  # 充值方案ID（没有选择充值方案值为""）
    real_pay_count = db.StringField()  # 本次充值实付金额（充值金额 - 充值方案优惠金额）
    recharge_time = db.DateTimeField(default=datetime.datetime.now)  # 本次充值成立时间
    payment_method = db.StringField()  # 付款方式（银行卡（0）...{微信（1）、支付宝（2）}）
    payment_account = db.StringField()  # 付款账号（银行卡号...）
    recharge_status = db.StringField()  # 充值状态（充值成功（0）、充值失败（1））
    recharge_status_remarks = db.StringField()  # 充值状态备注（充值成功、（其余系统层级原因）....）
    giving_integral_count = db.IntField(default=0)  # 赠送积分（本次操作可得积分 默认0）

    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间

    @staticmethod
    def get_dict_id(dict_type, dict_name):
        dict_obj = SysDict.get_dict_by_type_and_name(dict_type=dict_type, dict_name=dict_name)
        return dict_obj.dict_id

    @classmethod
    def get_recharge_record_by_data(cls, recharge_object_code_list, recharge_rule_id_list):
        """
        根据充值对象编号列表、充值方案ID 获取本充值对象适用此类充值方案的充值记录(返回值 所用充值方案ID)
        :param recharge_object_code_list:
        :param recharge_rule_id_list:
        :return:
        """
        return cls.objects(recharge_object_code__in=recharge_object_code_list,
                           recharge_status__in=[cls.get_dict_id("balance_recharge_status", "充值成功")],
                           recharge_rule_id__in=recharge_rule_id_list).only(
            "recharge_rule_id").all()

    @classmethod
    def insert_balance_recharge_record_by_create_dict(cls, create_dict):
        """
        根据create_dict 内容创建余额充值记录
        :param create_dict:
        :return:
        """
        current_time = datetime.datetime.now()
        record_id = "BRR" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 999999))
        new_balance_recharge_record_obj = BalanceRechargeRecord(
            record_id=record_id, recharge_object_type=create_dict["recharge_object_type"],
            recharge_object_code=create_dict["recharge_object_code"],
            recharge_money_count=create_dict["recharge_money_count"],
            recharge_rule_id=create_dict["recharge_rule_id"], real_pay_count=str(create_dict["real_pay_count"]),
            recharge_time=current_time, payment_method=create_dict["payment_method"],
            payment_account=create_dict["payment_account"],
            giving_integral_count=create_dict["giving_integral_count"],
            recharge_status=cls.get_dict_id("balance_recharge_status", "充值成功"), recharge_status_remarks="充值成功",
            create_by=current_user.user_code,
            create_time=current_time, update_by=current_user.user_code, update_time=current_time
        )
        new_balance_recharge_record_obj.save()

    @classmethod
    def get_record_by_record_id(cls, record_id):
        """
        根据记录id获取记录
        :param record_id:
        :return:
        """
        search = [
            {'$lookup': {
                'from': 'sys_dict',
                'localField': 'payment_method',
                'foreignField': 'dict_id',
                'as': 'payment_dict'
            }},
            {'$unwind': '$payment_dict'},
            {'$lookup': {
                'from': 'sys_dict',
                'localField': 'recharge_status',
                'foreignField': 'dict_id',
                'as': 'status_dict'
            }},
            {'$unwind': '$status_dict'},
            {'$match': {
                'payment_dict.dict_type': 'recharge_payment_method',
                'status_dict.dict_type': 'balance_recharge_status',
                'record_id': record_id
            }},
            {'$project': {
                '_id': 0,
                'record_id': 1,
                'payment_dict.dict_name': 1,
                'status_dict.dict_name': 1,
                'recharge_money_count': 1,
                'real_pay_count': 1,
                'recharge_time': 1
            }}
        ]
        return list(cls.objects.aggregate(*search))

    @classmethod
    def get_record_by_recharge_object_code(cls, code, page=1, per_page=12, start_time=None, end_time=None):
        """
        根据充值对象编号获取记录(分页)
        :param code:
        :return:
        """
        try:
            skip_num = (int(page) - 1) * int(per_page)
            search = [
                {'$lookup': {
                    'from': 'sys_dict',
                    'localField': 'recharge_status',
                    'foreignField': 'dict_id',
                    'as': 'sys_dict'
                }},
                {'$unwind': '$sys_dict'},
                {'$match': {
                    'sys_dict.dict_type': 'balance_recharge_status',
                    'recharge_object_code': code
                }},
                {'$sort': {'create_time': -1}},
                {'$skip': skip_num},
                {'$limit': int(per_page)},
                {'$project': {
                    '_id': 0,
                    'record_id': 1,
                    'sys_dict.dict_name': 1,
                    'recharge_money_count': 1,
                    'giving_integral_count': 1,
                    'recharge_time': 1
                }}

            ]
            if start_time and end_time:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                return cls.objects(recharge_time__gte=start_time, recharge_time__lte=end_time).aggregate(*search)
            else:
                return cls.objects.aggregate(*search)
        except Exception as e:
            raise e
