#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 11:16
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : models.py

import datetime, time, re, logging
from rich_base_provider import db
from flask_security import current_user
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from flask import session

dict_status_normal = '1'
dict_status_delete = '3'

dict_normal = "正常"
dict_delete = "删除"


def create_present_id():
    """
    创建积分兑换唯一id
    :return:
    """
    base_str = str(time.time()).replace('.', '')[:13]
    return 'P{:0<13}'.format(base_str)


class IntegralCharge(db.Document):
    """
    积分兑换
    """
    meta = {
        "collection": "integral_charge"
        # "collection": "integral_charge_test"
    }
    present_name = db.StringField()  # 礼品名称
    present_id = db.StringField()  # 礼品编码
    integral = db.StringField()  # 所需积分
    stock = db.StringField()  # 库存
    org_id = db.StringField()  # 所属机构
    appropriate_types = db.StringField()  # 充值方案适用类型    # '0'机构  '1'角色  '2'部门
    appropriate_value = db.ListField(db.StringField())  # 充值方案适用值
    # appropriate_value = db.StringField()  # 充值方案适用值
    start_time = db.DateTimeField()  # 活动开始时间
    end_time = db.DateTimeField()  # 活动结束时间
    status = db.StringField(choices=[dict_status_normal, dict_status_delete],
                            default=dict_status_normal)  # 当前积分规则状态（启用（'1'）、删除（'3'））
    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.now())  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间

    @staticmethod
    def get_status(dict_name):
        status_value = SysDict.get_dict_by_type_and_name(dict_type='public_status', dict_name=dict_name)
        return status_value.dict_id

    @classmethod
    def get_integral_charge_list_by_data(cls, org_id=None, page=1, per_page=20, search_data=""):
        """
        根据页码、搜索条件查询指定数目记录
        :param page:
        :param per_page:
        :param search_data:
        :return:
        by denghaolin
        """
        try:
            status = cls.get_status('删除')
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            org_code = session.get('org_code')
            org_objs = Sys_org.find_son_sys_org(org_code)
            org_id_list = []
            if org_objs:
                for org_obj in org_objs:
                    org_id_list.append(org_obj.org_id)
            search = []
            search.append({'$lookup': {'from': 'sys_org',
                                       'localField': 'org_id',
                                       'foreignField': 'org_id',
                                       'as': 'sys_org'
                                       }})
            search.append({'$unwind': "$sys_org"})
            search.append({'$match': {
                '$and': [
                    {'status': {'$nin': [status]}},
                    {'org_id': {'$in': org_id_list}}
                ],
                '$or': [{'present_name': re.compile(search_data)},
                        {'sys_org.org_name': re.compile(search_data)}],
            }})
            search.append({'$sort': {'create_time': -1}})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})
            search.append({'$sort': {'create_time': -1}})
            search.append({'$project': {'sys_org.org_name': 1,
                                        'present_id': 1,
                                        'present_name': 1,
                                        'integral': 1,
                                        'stock': 1,
                                        'org_id': 1,
                                        'end_time': 1,
                                        'start_time': 1}})
            integral_charge_obj = cls.objects.aggregate(*search)
            return list(integral_charge_obj), count
        except Exception as e:
            raise e

    @classmethod
    def get_exist_present_name(cls, org_id, present_name):
        """
        获取同一机构下是否存在相同的礼物名称
        :param org_id:
        :param present_name:
        :return:
        by denghaolin
        """
        try:
            return cls.objects(org_id=org_id, status=dict_status_normal, present_name__exact=present_name).first()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def add_integral_charge(cls, params):
        """
        新增积分兑换
        :param params:
        :return:
        by denghaolin
        """
        try:
            start_time = datetime.datetime.strptime(params.get("start_time"), '%Y-%m-%d %H:%M:%S')  # 格式化日期
            end_time = datetime.datetime.strptime(params.get("end_time"), '%Y-%m-%d %H:%M:%S')  # 格式化日期
            present_id = create_present_id()  # 生成present_id
            org_id = params.get('org_id')
            present_name = params.get('present_name')
            integral = params.get('integral')
            stock = params.get('stock')
            appropriate_types = params.get('appropriate_types')
            appropriate_value = params.get('appropriate_value')
            create_by = current_user.user_code
            create_time = datetime.datetime.now()
            integral_charge = IntegralCharge(
                start_time=start_time, end_time=end_time, present_id=present_id, org_id=org_id,
                integral=integral, stock=stock, appropriate_types=appropriate_types,
                appropriate_value=appropriate_value, present_name=present_name,
                create_by=create_by, create_time=create_time, status=dict_status_normal)
            integral_charge.save()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_integral_charge_by_id(cls, present_id):
        """
        根据id获取积分兑换对象
        :param present_id:
        :return:
        by denghaolin
        """
        try:
            charge_obj = cls.objects(present_id=present_id, status=dict_status_normal).first()
            if charge_obj:
                return charge_obj
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def deleted(cls, present_id):
        """
        删除积分兑换
        :param present_id:
        :return:
        by denghaolin
        """
        try:
            cls.objects(present_id=present_id).update(set__status=dict_status_delete,
                                                      set__update_time=datetime.datetime.now(),
                                                      set__update_by=current_user.user_code)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def edit_integral_charge(cls, params):
        """
        编辑积分兑换
        :param params:
        :return:
        by denghaolin
        """
        try:
            cls.objects(present_id=params.get('present_id')).update_one(set__org_id=params.get('org_id'),
                                                                        set__present_name=params.get('present_name'),
                                                                        set__integral=params.get('integral'),
                                                                        set__stock=params.get('stock'),
                                                                        set__appropriate_types=params.get(
                                                                            'appropriate_types'),
                                                                        set__appropriate_value=params.get(
                                                                            'appropriate_value'),
                                                                        set__start_time=params.get('start_time'),
                                                                        set__end_time=params.get('end_time'),
                                                                        set__update_by=current_user.user_code,
                                                                        set__update_time=datetime.datetime.now())
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exit_present_name_in_edit(cls, params):
        """
        编辑操作时获取除自己外相同的礼物名称
        :param params:
        :return:
        by denghaolin
        """
        try:
            org_id = params.get('org_id')
            present_id = params.get('present_id')
            present_name = params.get('present_name')
            return cls.objects(org_id=org_id, present_id__ne=present_id, status=dict_status_normal,
                               present_name__exact=present_name).first()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_org_code_in_model(cls):
        """
        获取所有有积分的机构code列表
        :return:
        """
        try:
            integral_charge_obj_list = cls.objects(status=dict_status_normal).all()
            org_code_list = []
            for integral_charge_obj in integral_charge_obj_list:
                org_code_list.append(Sys_org.get_org_info_by_org_id(org_id=integral_charge_obj.org_id).org_code)
            org_code_list = list(set(org_code_list))
            return org_code_list
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_integral_charge_by_id_list(cls, present_id_list):
        """
        根据id获取积分兑换对象
        :param present_id:
        :return:
        by denghaolin
        """
        try:
            charge_obj = cls.objects(present_id__in=present_id_list, status=dict_status_normal).all()
            if charge_obj:
                return charge_obj
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def update_stock(cls, params):
        """
        更新礼品库存
        :param params:
        :return:
        """
        try:
            update_by = current_user.user_code
            update_time = datetime.datetime.now()
            old_stock = int(cls.objects(present_id=params.get('present_id')).first().stock)
            new_stock = old_stock - 1
            cls.objects(present_id=params.get('present_id')).update_one(set__stock=str(new_stock),
                                                                        set__update_by=update_by,
                                                                        set__update_time=update_time)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def present_is_charge(cls, present_id):
        """
        查询礼品是否已经兑换过
        :param present_id:
        :return:
        """
        try:
            from rich_base_provider.sysadmin.integral.integral_charge_record.models import IntegralChargeRecord
            record = IntegralChargeRecord.get_record_by_present_id(present_id)
            if record:
                return True
            return False
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_appropriate_value(cls, integral_charge_obj):
        """
        获取积分兑换管理适用值
        :param integral_charge_obj:
        :return:
        """
        try:
            res_list = []
            appropriate_type = integral_charge_obj.appropriate_types
            if appropriate_type == '0':  # 适用类型是机构
                org_name_list = Sys_org.get_org_name_by_org_id_list(integral_charge_obj.appropriate_value)
                for each in org_name_list:
                    res_list.append(dict(id=each.org_id, name=each.org_name))
                return res_list
            elif appropriate_type == '1':  # 适用类型是角色
                from rich_base_provider.sysadmin.sys_role.models import Role
                role_name_list = Role.get_role_list_by_code(integral_charge_obj.appropriate_value)
                for each in role_name_list:
                    res_list.append(dict(id=each.role_code, name=each.name))
                return res_list
            elif appropriate_type == '2':  # 适用类型是部门
                department_name_list = Sys_org.get_department_info_by_org_id_and_department_id(
                    org_id=integral_charge_obj.org_id,
                    department_id=integral_charge_obj.appropriate_value)
                for each in department_name_list:
                    res_list.append(dict(id=each.get('department').get('id'), name=each.get('department').get('name')))
                return res_list
            else:
                return []
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_user_can_charge_present_id_list(cls, orgs, roles, departments):
        """
        根据用户身份获取可兑换礼品id列表
        :param orgs:   当前用户属于的机构
        :param roles:   当前用户属于的角色
        :param departments:  当前用户属于的部门
        :return:
        """
        try:
            req_data = []
            if orgs:
                for org in orgs:
                    org_id = Sys_org.get_org_info(org).org_id
                    req_data.append(org_id)
            if roles:
                for role in roles:
                    req_data.append(role)
            if departments:
                for department in departments:
                    req_data.append(department)
            present_id_list = []
            search = [
                {'$match': {
                    '$and': [
                        {'status': {'$in': [dict_status_normal]}},
                        {'appropriate_value': {'$in': req_data}},
                        {'start_time': {
                            '$lte': datetime.datetime.now()}},
                        {'end_time': {
                            '$gte': datetime.datetime.now()}},
                    ]
                }},
                {'$sort': {'create_time': -1}},
                {'$project': {'present_id': 1
                              }}
            ]
            present_result = list(cls.objects.aggregate(*search))
            if present_result:
                for present_obj in present_result:
                    present_id_list.append(present_obj.get('present_id'))
            return present_id_list
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_present_list_by_present_id_list(cls, present_id_list, search_data='', page=1, per_page=20):
        """
        根据礼品id列表查询
        :param present_id_list:
        :param search_data:
        :param page:
        :param per_page:
        :return:
        """
        try:
            start_index = (int(page) - 1) * int(per_page)
            search = {
                '__raw__': {
                    'status': {'$in': [dict_status_normal]},
                    'present_id': {'$in': present_id_list},
                    '$or': [
                        {'present_name': re.compile(search_data)}
                    ]
                }
            }
            count = cls.objects(**search).count()
            return cls.objects(**search).skip(start_index).limit(int(per_page)).order_by("-create_time").all(), count

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_org_can_charge_present_id_list(cls, org_id):
        """
        根据用户身份获取可兑换礼品id列表
        :param orgs:   当前用户属于的机构
        :param roles:   当前用户属于的角色
        :param departments:  当前用户属于的部门
        :return:
        """
        try:
            present_id_list = []
            search = [
                {'$match': {
                    '$and': [
                        {'status': {'$in': [dict_status_normal]}},
                        {'appropriate_types': {'$in': ['0']}},
                        {'appropriate_value': {'$in': [org_id]}},
                        {'start_time': {
                            '$lte': datetime.datetime.now()}},
                        {'end_time': {
                            '$gte': datetime.datetime.now()}},
                    ]
                }},
                {'$sort': {'create_time': -1}},
                {'$project': {'present_id': 1
                              }}
            ]
            present_result = list(cls.objects.aggregate(*search))
            if present_result:
                for present_obj in present_result:
                    present_id_list.append(present_obj.get('present_id'))
            return present_id_list
        except Exception as e:
            logging.debug(e)
            raise e
