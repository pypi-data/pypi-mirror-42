#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 14:04
# @Author  : zbh
# @Site    : www.rich-f.com
# @File    : models.py
import logging
import re
from rich_base_provider import db

# 关系类型

from rich_base_provider.sysadmin.sys_user.models import User

# 关系类型
suppliers = '1'  # 供应商
buyers = '2'  # 采购商
logistics = '3'  # 物流
internal_staff = '4'  # 内部员工

# 支付方式
cash = '1'  # 现金
prepaid = '2'  # 预付
account_period = '3'  # 帐期
credit = '4'  # 赊销


class Relation(db.EmbeddedDocument):
    user_code = db.StringField()
    org_id = db.StringField(required=False)
    nickname = db.StringField()  # 昵称
    is_stop = db.BooleanField(default=False)  # 添加用户的状态：是否停用
    relation_type = db.StringField(choices=[suppliers, buyers, logistics, internal_staff])  # 关系类型(供应商，采购商,物流)
    pay_type = db.StringField(choices=[cash, prepaid, account_period, credit])  # 支付方式（现金，预付，账期，赊销）
    is_share = db.IntField(default=0)  # 是否共享 上下游等关系信息


class User_relations(db.Document):
    """
    商业好友关系表
    """
    meta = {
        'collection': 'sys_user_relations'
    }
    user_code = db.StringField()
    org_id = db.StringField()
    user_relations = db.ListField(db.EmbeddedDocumentField('Relation'), default=[])

    @classmethod
    def create_user_relation(cls, user_code, org_id, nickname, relation_type, pay_type, is_share):
        """
        添加用户关系
        :param: user_name:待添加用户，relation_type：关系类型，is_share：是否共享关系信息
        :return: 用户商业好友关系对象
        """
        logging.info("create_user_relation")
        try:
            user = User.objects(user_code=user_code).first()
            # 待添加用户状态
            is_stop = user.status

            relation = Relation(user_code=user_code, org_id=org_id, nickname=nickname, is_stop=is_stop,
                                relation_type=relation_type, pay_type=pay_type, is_share=is_share)
            return relation
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_detail_info(cls, current_user_code, friend_user_code):
        """
        查询好友个人详情信息
        :param current_user_code: 当前用户user_code
        :param friend_user_code: 商业好友的user_code
        :return:
        """
        try:
            search = [
                {'$match': {
                    'user_code': current_user_code
                }},
                {'$project': {
                   'user_relations': {
                       '$filter': {
                           'input': '$user_relations',
                           'as': 'user_relations',
                           'cond': {'$eq': ['$$user_relations.user_code', friend_user_code]}
                       }
                   }
                }},
                {"$unwind": "$user_relations"},
                {
                    '$lookup': {
                        'from': 'sys_dict',
                        'localField': 'user_relations.relation_type',
                        'foreignField': 'dict_id',
                        'as': 'relation'
                    }
                },
                {'$unwind': "$relation"},
                {
                    '$lookup': {
                        'from': 'sys_dict',
                        'localField': 'user_relations.pay_type',
                        'foreignField': 'dict_id',
                        'as': 'pay'
                    }
                },
                {'$unwind': "$pay"},
                {'$match': {
                    '$and': [{"pay.dict_type": 'pay_methods'},
                             {"relation.dict_type": 'cooperation_type'}]
                }
                },
                {
                    '$lookup': {
                        'from': 'sys_user',
                        'localField': 'user_relations.user_code',
                        'foreignField': 'user_code',
                        'as': 'sys_user'
                    }
                },
                {"$unwind": "$sys_user"},
                {
                    '$lookup': {
                        'from':'sys_org',
                        'localField': 'user_relations.org_id',
                        'foreignField': 'org_id',
                        'as': 'sys_org'
                    }
                },
                {"$unwind": "$sys_org"},
                {'$project': {
                    '_id': 0,
                    'user_relations': 1,
                    'sys_user.username': 1,
                    'sys_user.account.mobile': 1,
                    'sys_org.org_name': 1,
                    'sys_org.org_code': 1,
                    'relation.dict_name': 1,
                    'pay.dict_name': 1,
                }}
            ]
            detail_info = list(cls.objects.aggregate(*search))

            if detail_info:
                return detail_info[0]
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_user_relation_by_user_code(cls, user_code):
        """
        根据user_code获取用户关系
        :param user_code:
        :return:
        """
        user_rel = cls.objects(user_code=user_code).first()
        if user_rel:
            return user_rel
        return None

    @classmethod
    def update_user_relations(cls, user_code, friend_user_code, relation):
        """
        更新用户关系
        :param user_code:
        :return:
        """
        logging.info('update_user_relations')
        try:
            cls.objects(user_code=user_code,user_relations__user_code=friend_user_code).update_one(
                __raw__={
                    '$set':{
                        'user_relations.$.user_code': relation.user_code,
                        'user_relations.$.org_id': relation.org_id,
                        'user_relations.$.nickname': relation.nickname,
                        'user_relations.$.relation_type': relation.relation_type,
                        'user_relations.$.pay_type': relation.pay_type,
                        'user_relations.$.is_share': relation.is_share,

                    }
                }
            )

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_user_relation(cls, user_code, searchdata="", page=1, per_page=8):
        """
        通过当前用户编码，获取同一关系类型所有商业关系的用户列表
        :param user_code:
        :return: user_list: 同一关系类型所有商业好友关系的用户
        """
        logging.info("get_user_relation")

        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$match': {'$and': [{"user_code": user_code}]}},
                {"$project": {
                    'user_relations': {
                        '$filter': {
                            "input": "$user_relations",
                            "as": "user_relations",
                            "cond": {"$ne": ['$$user_relations.relation_type', None]}
                        }
                    }
                }},
                {"$unwind": "$user_relations"},
                {
                    '$lookup': {
                        'from': 'sys_user',
                        'localField': 'user_relations.user_code',
                        'foreignField': 'user_code',
                        'as': 'sys_user'
                    }
                },
                {"$unwind": "$sys_user"},
                {
                    '$lookup': {
                        'from': 'sys_dict',
                        'localField': 'user_relations.relation_type',
                        'foreignField': 'dict_id',
                        'as': 'sys_dict'
                    }
                },
                {'$unwind': "$sys_dict"},
                {'$match': {
                    '$and': [
                        {"sys_dict.dict_type": 'cooperation_type'}
                    ],
                    '$or': [
                        {"sys_user.username": re.compile(searchdata)},
                        {"user_relations.nickname": re.compile(searchdata)},
                        {"sys_dict.dict_name": re.compile(searchdata)}
                    ]
                }},
            ]
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count_obj = list(cls.objects.aggregate(*search))
            if len(count_obj):
                count = count_obj[0]["count"]
            else:
                count = 0

            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})

            search.append({'$skip': skip_nums})
            search.append({'$limit': per_page})

            search.append({"$project": {
                                'user_relations': 1,
                                'sys_dict.dict_name': 1,
                                'sys_user.username': 1,
                                'sys_user.info.avatar': 1,
                                '_id': 0
                                }
                           })

            user_list = list(cls.objects.aggregate(*search))
            return {"user_list": user_list, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_user_relation_by_usercode(cls, user_code, relations_type, searchdata="", page=1, per_page=8):
        """
        通过当前用户编码，获取所有商业关系的用户列表
        :param user_code:
        :return: user_list: 所有商业好友关系的用户
        """
        logging.info("get_user_relation")
        print(user_code)
        print(relations_type)

        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$match': {'$and': [{"user_code": user_code}]}},
                {"$project": {
                    'user_relations': {
                        '$filter': {
                            "input": "$user_relations",
                            "as": "user_relations",
                            "cond": {"$eq": ['$$user_relations.relation_type', relations_type]}
                            # "cond": {"$ne": ['$$user_relations.relation_type', None]}
                        }
                    }
                }},
                {"$unwind": "$user_relations"},
                {'$lookup': {
                    'from': 'sys_org',
                    'localField': 'user_relations.org_id',
                    'foreignField': 'org_id',
                    'as': 'sys_org'
                }},
                {'$unwind': '$sys_org'},
                {
                    '$lookup': {
                        'from': 'sys_user',
                        'localField': 'user_relations.user_code',
                        'foreignField': 'user_code',
                        'as': 'sys_user'
                    }
                },
                {"$unwind": "$sys_user"},
                {
                    '$lookup': {
                        'from': 'sys_dict',
                        'localField': 'user_relations.relation_type',
                        'foreignField': 'dict_id',
                        'as': 'sys_dict'
                    }
                },
                {'$unwind': "$sys_dict"},
                {'$match': {
                    '$and': [
                        {"sys_dict.dict_type": 'cooperation_type'}
                    ],
                    '$or': [
                        {"sys_user.username": re.compile(searchdata)},
                        {"user_relations.nickname": re.compile(searchdata)},
                        {"sys_dict.dict_name": re.compile(searchdata)}
                    ]
                }},
            ]
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count_obj = list(cls.objects.aggregate(*search))
            if len(count_obj):
                count = count_obj[0]["count"]
            else:
                count = 0

            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})

            search.append({'$skip': skip_nums})
            search.append({'$limit': per_page})

            search.append({"$project": {'user_relations': 1,
                                        'sys_dict.dict_name': 1,
                                        'sys_user.username': 1,
                                        'sys_user.info.avatar': 1,
                                        'sys_user.account.mobile':1,
                                        'sys_org.org_name':1,
                                        '_id': 0}})

            user_list = list(cls.objects.aggregate(*search))
            return {"user_list": user_list, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    @property
    def relation_dict(self):
        """
        关系字典
        :return:
        :by:wangwei
        """
        return {'suppliers': suppliers,
                'buyers': buyers,
                'logistics': logistics,
                'internal_staff': internal_staff}

    @classmethod
    def get_relations_org_dict(cls, user_code, org_id, org_name='', page=1, per_page=12, relations=suppliers):
        """
        获取关系向(默认供应商) 机构id和机构名字字典
        :param user_code:
        :param org_id:
        :return:
        :by:wangwei
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$match': {
                    'org_id': org_id,
                    'user_code': user_code
                }},
                {'$project': {
                    'relations': {
                        '$filter': {
                            'input': '$user_relations',
                            'as': 'user_relations',

                            'cond': {'$and': [{'$eq': ['$$user_relations.relation_type', relations]},
                                              {'$eq': ['$$user_relations.is_stop', False]}]}

                        }
                    }
                }},
                {'$unwind': '$relations'},
                {'$lookup': {
                    'from': 'sys_org',
                    'localField': 'relations.org_id',
                    'foreignField': 'org_id',
                    'as': 'sys_org'
                }},

                {'$match': {
                    'sys_org.status': {'$in': [0, 1]},
                    'sys_org.org_id': {'$ne': org_id},
                    '$or': [{'sys_org.org_name': re.compile(org_name)}]


                }},
                {'$skip': skip_nums},
                {'$limit': int(per_page)},
                {'$project': {
                    '_id': 0,
                    'sys_org.org_name': 1,
                    'sys_org.org_id': 1,
                    'sys_org.door_img': 1
                }}

            ]
            org_list = list(cls.objects.aggregate(*search))
            if org_list:
                return org_list[0].get('sys_org')
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_validation_list(cls, cur_user_code, cur_org_id, page=1, per_page=8):
        """
        获取好友验证列表
        :param user_code:
        :return: user_list: 所有商业好友关系的用户
        """
        logging.info("get_validation_list")
        # 验证状态-未处理
        # untreated = SysDict.get_dict_by_type_and_name(dict_type='deal_status', dict_name='未处理').dict_id
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = [
                {'$lookup': {
                    'from': 'sys_user',
                    'localField': 'user_code',
                    'foreignField': 'user_code',
                    'as': 'sys_user'
                }},
                {'$unwind': '$sys_user'},
                {'$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_id',
                    'foreignField': 'org_id',
                    'as': 'sys_org'
                }},
                {'$unwind': '$sys_org'},
                {'$match': {
                    '$and': [
                        {'user_relations': {'$elemMatch': {'user_code': cur_user_code, 'org_id': cur_org_id,}}},
                        {'sys_org.status': {'$in': [0, 1]}},
                    ],
                }},
                {'$group': {'_id': 0, 'count': {'$sum': 1}}}
            ]
            count_obj = list(cls.objects.aggregate(*search))
            if len(count_obj):
                count = count_obj[0]["count"]
            else:
                count = 0
            search.pop()

            search.append({'$skip': skip_nums})
            search.append({'$limit': per_page})
            search.append({
                '$project': {
                    '_id': 0,
                    # 'user_relations.pay_type': 1,
                    'sys_user.username': 1,
                    'sys_user.account.mobile': 1,
                    'sys_user.info.avatar': 1,
                    'sys_org.org_name': 1,
                    'user_code': 1,
                    'org_id': 1
                }
            })

            validate_info = list(cls.objects.aggregate(*search))
            search.pop()
            search.append(
                {
                    '$project': {
                        'relations': {
                            '$filter': {
                                'input': "$user_relations",
                                'as': "user_relations",
                                'cond': {
                                    '$and': [
                                        {'$eq': ['$$user_relations.user_code', cur_user_code]},
                                        {'$eq': ['$$user_relations.org_id', cur_org_id]},
                                        ]
                                }
                            }
                        }
                    }
                }
            )
            search.append({"$unwind": "$relations"})
            search.append(
                {
                    '$project': {
                        '_id': 0,
                        'relations.pay_type': 1,
                    }
                }
            )
            pay_type = list(cls.objects.aggregate(*search))
            return {"validate_info": validate_info, "count": count, "pay_type": pay_type}
        except Exception as e:
            logging.debug(e)
            raise e