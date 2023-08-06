#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    : models.py
# @Function: 优惠券模块

import logging
import re, time, datetime
from rich_base_provider import db
from rich_base_provider.sysadmin.sys_user.models import User, CouponRecords
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_org.models import CouponRecords as Og


class Coupon(db.Document):
    """
    优惠券管理
    """

    meta = {
        'collection': 'coupons'
    }

    coupon_code = db.StringField(unique=True, required=False)  # 优惠券编码 C + 时间戳
    org_id = db.StringField()  # 绑定创建机构
    title = db.StringField()  # 优惠券活动标题
    content = db.StringField()  # 优惠券活动内容
    type = db.StringField()  # 优惠券类型  1满减，2折扣，3代金券
    condition = db.FloatField(default=0)  # 优惠券使用条件
    value = db.FloatField()  # 优惠力度
    start_time = db.DateTimeField()  # 优惠券开始时间
    end_time = db.DateTimeField()  # 优惠券结束时间
    product_type = db.StringField()  # 商品对象范围 1 全场 2 类型 3 商品
    target_product = db.ListField(db.StringField())  # 优惠券对应产品
    user_type = db.StringField()  # 用户对象范围类型
    target_user = db.ListField(db.StringField())  # 优惠券对应用户
    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_by = db.StringField()  # 修改人
    update_time = db.DateTimeField(default=datetime.datetime.now)  # 更新时间
    status = db.StringField()  # 状态("0",正常，"1":停用 "2":删除)
    coupon_num = db.IntField(default=1)  # 优惠券数量
    send_num = db.IntField(default=0)  # 已经发放数量

    @staticmethod
    def make_code(prefix):
        base_str = str(time.time()).replace('.', '')[:13]
        return '{}{:0<13}'.format(prefix, base_str)

    # 字典相关操作
    @staticmethod
    def get_status(dict_name):
        """状态"""
        data = SysDict.get_dict_by_type_and_name(dict_type='coupon_status', dict_name=dict_name)
        return data

    @staticmethod
    def get_dict_list(dict_type):
        """查询字典"""
        data = SysDict.get_dict_list_by_type(dict_type)
        data_dict = {}
        for info in data:
            data_dict[info.dict_id] = info.dict_name
        return data_dict

    @staticmethod
    def get_product_type(dict_name):
        """优惠商品范围"""
        data = SysDict.get_dict_by_type_and_name(dict_type='coupon_product_type', dict_name=dict_name)
        return data

    @staticmethod
    def get_coupon_type(dict_name):
        """优惠券类型"""
        data = SysDict.get_dict_by_type_and_name(dict_type='coupon_type', dict_name=dict_name)
        return data

    @staticmethod
    def get_user_type(dict_name):
        """用户对象范围"""
        data = SysDict.get_dict_by_type_and_name(dict_type='coupon_user_type', dict_name=dict_name)
        return data

    @staticmethod
    def get_coupon_type_and_product_type():
        """
        查询优惠券类型和优惠商品范围
        :return:
        """
        try:
            search = {
                '__raw__': {
                    'dict_type': {'$in': ['coupon_product_type', 'coupon_type']},
                },
            }
            sys_dict = SysDict.objects(**search)
            return sys_dict
        except Exception as e:
            return False

    @staticmethod
    def get_status_product_user_type():
        """
        查询该表所对应的所有字典值
        :return:
        """
        try:
            search = {
                '__raw__': {
                    'dict_type': {'$in': ['coupon_status', 'coupon_product_type', 'coupon_type', 'coupon_user_type']},
                },
            }
            sys_dict = SysDict.objects(**search)
            data = {'coupon_status': [],
                    'coupon_product_type': [],
                    'coupon_type': [],
                    'coupon_user_type': []}
            for info in sys_dict:
                if info.dict_type == 'coupon_status':
                    data['coupon_status'].append({'dict_name': info.dict_name,
                                                  'dict_id': info.dict_id})
                if info.dict_type == 'coupon_product_type':
                    data['coupon_product_type'].append({'dict_name': info.dict_name,
                                                        'dict_id': info.dict_id})
                if info.dict_type == 'coupon_type':
                    data['coupon_type'].append({'dict_name': info.dict_name,
                                                'dict_id': info.dict_id})
                if info.dict_type == 'coupon_user_type':
                    data['coupon_user_type'].append({'dict_name': info.dict_name,
                                                     'dict_id': info.dict_id})
            return data
        except Exception as e:
            raise e

    @classmethod
    def create(cls, **kw):
        """
        新建优惠券
        :param kw:
        :return:
        """
        try:
            start_time = datetime.datetime.strptime(kw.get("start_time"), '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(kw.get("end_time"), '%Y-%m-%d %H:%M:%S')
            coupon_obj = Coupon(coupon_code=cls.make_code("C"),
                                org_id=kw.get("org_id"),
                                title=kw.get("title"),
                                content=kw.get("content"),
                                type=kw.get('type'),
                                condition=float(kw.get('condition')),
                                value=float(kw.get('value')),
                                start_time=start_time,
                                end_time=end_time,
                                product_type=kw.get("product_type"),
                                target_product=kw.get("target_product", []),
                                user_type=kw.get("user_type"),
                                target_user=kw.get("target_user", []),
                                status=kw.get("status", "0"),
                                create_by=kw.get("create_by"),
                                update_by=kw.get("update_by"),
                                coupon_num=kw.get("coupon_num")
                                )
            coupon_obj.save()
        except Exception as e:
            raise e

    @staticmethod
    def coupon_send_num(coupon_code):
        """
        判断优惠券是否发放
        :param coupon_code:
        :return:
        """
        try:
            coupon = Coupon.objects(coupon_code=coupon_code).first()
            return coupon.send_num
        except Exception as e:
            return False

    @staticmethod
    def get_use_users_by_coupon_code(coupon_code):
        """
        通过优惠券编码获取使用过优惠券的用户
        :param coupon_code:
        :return:
        """
        try:
            return User.objects(wallet__coupons__coupon_code=coupon_code, wallet__coupons__use_time__ne=None)
        except Exception as e:
            return False

    @classmethod
    def query_coupons_by_org_code(cls, org_code, search_data='', page=1, per_page=12):
        """
        通过机构编码获该机构及其子机构所有的优惠券
        :param org_id:
        :return:
        """
        try:
            status = cls.get_status('删除').dict_id
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [{'$lookup': {'from': 'sys_org',
                                   'localField': 'org_id',
                                   'foreignField': 'org_id',
                                   'as': 'sys_org'
                                   }},
                      {'$unwind': "$sys_org"},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'status',
                                   'foreignField': 'dict_id',
                                   'as': 'status_dict'
                                   }},
                      {'$unwind': "$status_dict"},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'type',
                                   'foreignField': 'dict_id',
                                   'as': 'type_dict'
                                   }},
                      {'$unwind': "$type_dict"},
                      {'$match': {'$and': [{'sys_org.org_code': re.compile(r'^{}'.format(org_code))},
                                           {'type_dict.dict_type': 'coupon_type'},
                                           {'status_dict.dict_type': 'coupon_status'},
                                           {'status': {'$nin': [status]}},
                                           {'sys_org.status': {'$in': [0, 1]}},
                                           ],
                                  '$or': [{'title': re.compile(search_data)},
                                          {'sys_org.org_name': re.compile(search_data)},
                                          {'type_dict.dict_name': re.compile(search_data)}],
                                  }},
                      {'$sort': {'create_time': -1}},
                      {'$skip': skip_nums},
                      {'$limit': int(per_page)},
                      {'$project': {'sys_org.org_name': 1,
                                    'title': 1,
                                    'coupon_code': 1,
                                    'type_dict.dict_name': 1,
                                    'status_dict.dict_name': 1,
                                    'start_time': 1,
                                    'end_time': 1,
                                    'status': 1
                                    }}
                      ]
            coupons_obj = cls.objects.aggregate(*search)
            return coupons_obj
        except Exception as e:
            raise e

    @classmethod
    def get_coupon_count(cls, org_code, search_data=''):
        try:
            status = cls.get_status('删除').dict_id
            search = [{'$lookup': {'from': 'sys_org',
                                   'localField': 'org_id',
                                   'foreignField': 'org_id',
                                   'as': 'sys_org'
                                   }},
                      {'$unwind': "$sys_org"},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'type',
                                   'foreignField': 'dict_id',
                                   'as': 'type_dict'
                                   }},
                      {'$unwind': "$type_dict"},
                      {'$match': {'$and': [{'sys_org.org_code': re.compile(r'^{}'.format(org_code))},
                                           {'type_dict.dict_type': 'coupon_type'},
                                           {'status': {'$nin': [status]}},
                                           {'sys_org.status': {'$in': [0, 1]}},
                                           ],
                                  '$or': [{'title': re.compile(search_data)},
                                          {'sys_org.org_name': re.compile(search_data)},
                                          {'type_dict.dict_name': re.compile(search_data)}]
                                  }},
                      {'$sort': {'create_time': 1}},
                      {'$group': {'_id': 0,
                                  'count': {'$sum': 1}}}
                      ]
            obj_data = cls.objects.aggregate(*search)
            info = list(obj_data)
            count = info[0].get('count') if info else 0
            return count
        except Exception as e:
            raise e

    @classmethod
    def get_coupon_obj_by_coupon_code(cls, coupon_code):
        """
        通过优惠券编码查询优惠券
        :param coupon_code:
        :return:
        """
        try:
            return cls.objects(coupon_code=coupon_code).first()
        except Exception as e:
            return False

    @classmethod
    def delete_by_coupon_code(cls, coupon_code):
        """
        通过优惠券编码删除优惠券
        :param coupon_code:
        :return:
        """
        try:
            cls.objects(coupon_code=coupon_code).update_one(set__status=cls.get_status('删除').dict_id)
            return True
        except Exception as e:
            return False

    def edit_coupon(self, **kw):
        """
        编辑
        :param kw:
        :return:
        """
        try:
            start_time = datetime.datetime.strptime(kw.get("start_time"), '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(kw.get("end_time"), '%Y-%m-%d %H:%M:%S')
            self.org_id = kw.get("org_id")
            self.title = kw.get("title")
            self.content = kw.get("content")
            self.condition = float(kw.get("condition"))
            self.type = kw.get("type")
            self.value = float(kw.get("value"))
            self.start_time = start_time
            self.end_time = end_time
            self.product_type = kw.get("product_type")
            self.target_product = kw.get("target_product")
            self.user_type = kw.get("user_type")
            self.target_user = kw.get("target_user")
            self.update_by = kw.get("update_by")
            self.coupon_num = kw.get("coupon_num")
            self.save()
        except Exception as e:
            raise e

    @staticmethod
    def send_coupon_to_users(org_id, coupon_code, users_code):
        """
        机构给用户发优惠券
        :param org_id:
        :param coupon_code:
        :param users_code:
        :return:
        """
        try:
            record_id = Coupon.make_code('CR')

            coupon_record = CouponRecords(record_id=record_id,
                                          coupon_code=coupon_code,
                                          org_id=org_id)
            users = User.objects(user_code__in=users_code)
            users.update(push__wallet__coupons=coupon_record)
            coupon = Coupon.objects(coupon_code=coupon_code).first()
            send_num = coupon.send_num + len(users_code)
            coupon.update(set__send_num=send_num)
            return True
        except Exception as e:
            return False

    @classmethod
    def get_coupons_by_coupon_code_list(cls, code_list):
        """
        通过已使用优惠券code_list查询优惠券
        :param coupons_list:
        :return:
        """
        try:
            return cls.objects(coupon_code__in=code_list)
        except Exception as e:
            return False

    @staticmethod
    def get_unused_coupons(coupon_code_list, page=1, per_page=12):
        """
        查询用户未使用的优惠券
        :param code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            coupons = Coupon.objects(coupon_code__in=coupon_code_list,
                                     end_time__gt=datetime.datetime.now()).skip(skip_nums).limit(int(per_page))
            return coupons
        except Exception as e:
            return False

    @staticmethod
    def get_expired_coupons(coupon_code_list, page=1, per_page=12):
        """
        查询用户过期未使用的优惠券
        :param code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            coupons = Coupon.objects(coupon_code__in=coupon_code_list,
                                     end_time__lt=datetime.datetime.now()).skip(skip_nums).limit(int(per_page))
            return coupons
        except Exception as e:
            return False

    @staticmethod
    def get_used_coupons(user_code, page=1, per_page=12):
        """
        查询用户已使用的优惠券
        :param code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$lookup': {
                    'from': 'coupons',
                    'localField': 'wallet.coupons.coupon_code',
                    'foreignField': 'coupon_code',
                    'as': 'coupons'
                }},
                {'$unwind': "$wallet.coupons"},

                {'$match': {
                    'user_code': user_code,
                    'wallet.coupons.use_time': {'$exists': True},
                }},
                {'$skip': skip_nums},
                {'$limit': int(per_page)},
                {'$project': {
                    '_id': 0,
                    'coupons': 1,
                    'wallet.coupons.coupon_code': 1
                }}
            ]
            used_coupons = User.objects.aggregate(*search)
            return list(used_coupons)
        except Exception as e:
            return False

    @staticmethod
    def get_org_used_coupons(org_code, page=1, per_page=12):
        """
        查询机构已使用的优惠券
        :param code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$lookup': {
                    'from': 'coupons',
                    'localField': 'wallet.coupons.coupon_code',
                    'foreignField': 'coupon_code',
                    'as': 'coupons'
                }},
                {'$unwind': "$wallet.coupons"},

                {'$match': {
                    'org_code': org_code,
                    'wallet.coupons.use_time': {'$exists': True},
                }},
                {'$skip': skip_nums},
                {'$limit': int(per_page)},
                {'$project': {
                    '_id': 0,
                    'coupons': 1,
                    'wallet.coupons.coupon_code': 1
                }}
            ]
            used_coupons = Sys_org.objects.aggregate(*search)
            return list(used_coupons)
        except Exception as e:
            return False

    @classmethod
    def get_coupon_info_update(cls, coupon_code):
        """
        通过优惠券id 获取编辑优惠券页面优惠券信息
        :return:
        """
        try:
            search = [{'$lookup': {'from': 'sys_org',
                                   'localField': 'org_id',
                                   'foreignField': 'org_id',
                                   'as': 'sys_org'
                                   }},
                      {'$unwind': "$sys_org"},
                      {'$match': {'coupon_code': coupon_code}},
                      {'$project': {'sys_org.org_name': 1,
                                    'title': 1,
                                    'org_id': 1,
                                    'content': 1,
                                    'type': 1,
                                    'condition': 1,
                                    'value': 1,
                                    'product_type': 1,
                                    'target_product': 1,
                                    'user_type': 1,
                                    'target_user': 1,
                                    'target_list': 1,
                                    'coupon_code': 1,
                                    'start_time': 1,
                                    'end_time': 1,
                                    'status': 1,
                                    'coupon_num': 1,
                                    'send_num': 1
                                    }}
                      ]

            coupons_obj = list(cls.objects.aggregate(*search))[0]
            return coupons_obj
        except Exception as e:
            return False

    @staticmethod
    def get_unused_coupon_info(coupon_code_list, page=1, per_page=12):
        """
        通过优惠券编码获取未使用优惠券信息
        :param coupon_code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [{'$lookup': {'from': 'sys_dict',
                                   'localField': 'type',
                                   'foreignField': 'dict_id',
                                   'as': 'type_dict'}},
                      {'$unwind': '$type_dict'},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'product_type',
                                   'foreignField': 'dict_id',
                                   'as': 'product_type'}},
                      {'$unwind': '$product_type'},
                      {'$lookup': {'from': 'sys_org',
                                   'localField': 'org_id',
                                   'foreignField': 'org_id',
                                   'as': 'sys_org'}},
                      {'$match':
                           {'type_dict.dict_type': 'coupon_type',
                            'product_type.dict_type': 'coupon_product_type',
                            'end_time': {'$gt': datetime.datetime.now()},
                            'coupon_code': {'$in': coupon_code_list},
                            'sys_org.status': {'$in':[0,1]}
                            },
                       },
                      {'$skip': skip_nums},
                      {'$limit': int(per_page)},
                      {'$project': {'type_dict.dict_name': 1,
                                    'product_type.dict_name': 1,
                                    'content': 1,
                                    'condition': 1,
                                    'value': 1,
                                    'coupon_code': 1,
                                    'start_time': 1,
                                    'end_time': 1,
                                    }}
                      ]
            coupons = Coupon.objects.aggregate(*search)
            return list(coupons)
        except Exception as e:
            return False

    @staticmethod
    def get_expired_coupon_info(coupon_code_list, page=1, per_page=12):
        """
        通过优惠券编码获取已过期优惠券信息
        :param coupon_code_list:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [{'$lookup': {'from': 'sys_dict',
                                   'localField': 'type',
                                   'foreignField': 'dict_id',
                                   'as': 'type_dict'}},
                      {'$unwind': '$type_dict'},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'product_type',
                                   'foreignField': 'dict_id',
                                   'as': 'product_type'}},
                      {'$unwind': '$product_type'},

                      {'$match':
                           {'type_dict.dict_type': 'coupon_type',
                            'product_type.dict_type': 'coupon_product_type',
                            'end_time': {'$lt': datetime.datetime.now()},
                            'coupon_code': {'$in': coupon_code_list}
                            },
                       },
                      {'$sort': {'create_time': -1}},
                      {'$skip': skip_nums},
                      {'$limit': int(per_page)},
                      {'$project': {'type_dict.dict_name': 1,
                                    'product_type.dict_name': 1,
                                    'content': 1,
                                    'condition': 1,
                                    'value': 1,
                                    'coupon_code': 1,
                                    'start_time': 1,
                                    'end_time': 1,
                                    }}
                      ]

            coupons_obj = list(Coupon.objects.aggregate(*search))
            return coupons_obj
        except Exception as e:
            return False

    @staticmethod
    def send_coupon_to_orgs(org_id, coupon_code, orgs_code):
        """
        机构给子机构发优惠券
        :param org_id:
        :param coupon_code:
        :return:
        """
        try:
            record_id = Coupon.make_code('CR')
            coupon_record = Og(coupon_code=coupon_code, org_id=org_id, record_id=record_id)
            Sys_org.objects(org_id__in=orgs_code).update(push__wallet__coupons=coupon_record)
            coupon = Coupon.objects(coupon_code=coupon_code).first()
            send_num = coupon.send_num + len(orgs_code)
            coupon.update(set__send_num=send_num)
            return True
        except Exception as e:
            return False

    @classmethod
    def get_coupon_info(cls, coupon_code):
        """
        通过优惠券编码获取优惠券信息
        :param coupon_code:
        :return:
        """
        try:
            search = [{'$lookup': {'from': 'sys_dict',
                                   'localField': 'type',
                                   'foreignField': 'dict_id',
                                   'as': 'type_dict'}},
                      {'$unwind': '$type_dict'},
                      {'$lookup': {'from': 'sys_dict',
                                   'localField': 'product_type',
                                   'foreignField': 'dict_id',
                                   'as': 'product_type'}},
                      {'$unwind': '$product_type'},
                      {'$match': {'$and': [
                          {'type_dict.dict_type': 'coupon_type'},
                          {'product_type.dict_type': 'coupon_product_type'},
                          {'coupon_code': coupon_code}
                      ]}},
                      {'$project': {'type_dict.dict_name': 1,
                                    'product_type.dict_name': 1,
                                    'condition': 1,
                                    'value': 1,
                                    'start_time': 1,
                                    'end_time': 1,
                                    }}
                      ]
            coupons_obj = list(cls.objects.aggregate(*search))[0]
            return coupons_obj
        except Exception as e:
            return False
