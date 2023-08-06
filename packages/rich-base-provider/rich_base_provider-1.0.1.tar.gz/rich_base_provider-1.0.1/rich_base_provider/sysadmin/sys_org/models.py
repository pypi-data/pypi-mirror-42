#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 11:43
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : models.py


import datetime as dt
import logging
import re
from rich_base_provider import db
from rich_base_provider import response
from flask_security import current_user
import time
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.settings import Config
from flask import session
import requests
from werkzeug.security import generate_password_hash, check_password_hash

department_status_normal = '1'
department_status_block_up = '2'
department_status_delete = '3'

type_suppliers = 1  # 供应商
type_buyers = 2  # 采购商
type_logistics = 3  # 物流

pay_cash = 1  # 现金
pay_prepaid = 2  # 预付
pay_account_period = 3  # 账期
pay_credit_sale = 4  # 赊销


def create_org_id():
    """
    创建机构唯一id
    :return:
    """
    base_str = str(time.time()).replace('.', '')[:13]
    return 'O{:0<13}'.format(base_str)


def create_department_id():
    """
    创建机构唯一id
    :return:
    """
    base_str = str(time.time()).replace('.', '')[:13]
    return 'D{:0<13}'.format(base_str)


class Bank_cart_info(db.EmbeddedDocument):
    """
    银行卡 信息
    """
    bank_card_type = db.StringField()  # 银行卡类型
    bank_account = db.StringField()  # 银行卡账号
    bank_name = db.StringField()  # 银行名
    bank_address = db.StringField()  # 开户银行地址
    bank_owner = db.StringField()  # 银行卡用户名
    card_correct_img = db.StringField()  # 银行卡正面照
    card_opposite_img = db.StringField()  # 银行卡背面照
    mobile = db.StringField(max_length=16)  # 银行绑定手机号码


class OrgBankCard(db.EmbeddedDocument):
    """机构钱包银行卡"""
    acc_no = db.StringField()  # 银行卡后4位
    bank_type = db.StringField()  # 银行类型
    bind_id = db.StringField()  #
    customer_id = db.StringField()  # user_code
    issInsCode = db.StringField()  # 银行名缩写
    open_id = db.StringField()  #
    pay_type = db.StringField()  #
    plant_bank_name = db.StringField()  # 银行名
    telephone = db.StringField()  # 绑定银行卡电话号码


class Id_card_info(db.EmbeddedDocument):
    """
    身份证信息
    """
    idcard_type = db.StringField()  # 身份证类型（00：身份证）
    idcard_number = db.StringField()  # 身份证号码
    concrete_address = db.StringField()  # 具体地址
    cert_correct_img = db.StringField()  # 身份证正面照
    cert_opposite_img = db.StringField()  # 身份证背面照
    hand_id_card_img = db.StringField()  # 手持身份证照片


class CouponRecords(db.EmbeddedDocument):
    """
    优惠券记录
    """
    record_id = db.StringField()  # 优惠券记录编码
    coupon_code = db.StringField()  # 优惠券编码
    get_time = db.DateTimeField(default=dt.datetime.utcnow)  # 获取时间
    org_id = db.StringField()  # 来源
    use_time = db.DateTimeField()  # 优惠券使用时间


class PointRecord(db.EmbeddedDocument):
    """
    积分记录
    """
    time = db.DateTimeField(default=dt.datetime.utcnow)  # 记录时间
    get = db.StringField(max_length=1, default='0')  # 获取  此处值为1时：该记录是获取记录
    post = db.StringField(max_length=1, default='0')  # 消耗 此处值为1时：该记录是消费记录  gain字段和expense只能一个字段为1
    amount = db.IntField()  # 获取/消耗积分值
    org_code = db.StringField()  # 来源
    way = db.StringField(max_length=255)  # 获取方式
    point_sum = db.IntField(default=0)  # 积分余额


class Transactions(db.EmbeddedDocument):
    """交易记录"""
    code = db.StringField(max_length=255)  # 流水号
    create_time = db.DateTimeField()  # 交易时间
    get = db.StringField(max_length=1, default='0')  # 获取   此处值为1时：该记录是获取记录
    post = db.StringField(max_length=1, default='0')  # 消费 此处值为1时：该记录是消费记录  gain字段和expense只能一个字段为1
    amount = db.FloatField()  # 交易金额
    org_code = db.StringField()  # 交易对象
    balance = db.FloatField(default=0)  # 余额


class OrgWallet(db.EmbeddedDocument):
    """用户钱包"""
    coupons = db.ListField(db.EmbeddedDocumentField('CouponRecords'), default=[])  # TODO:优惠券，需要和优惠表关联
    point = db.IntField(default=0)  # 积分
    point_record = db.ListField(db.EmbeddedDocumentField('PointRecord'), default=[])  # 积分记录
    transaction = db.ListField(db.EmbeddedDocumentField('Transactions'), default=[])  # 交易记录
    balance = db.FloatField(min_value=0, default=0)  # 余额
    bank_cards = db.ListField(db.EmbeddedDocumentField('OrgBankCard'), default=[])  # 银行卡信息
    pay_password = db.StringField(max_length=255)  # 支付密码hash值


class Department(db.EmbeddedDocument):
    """部门"""
    code = db.StringField()  # 部门编码
    id = db.StringField()  # 部门唯一id
    name = db.StringField()  # 部门标签名称
    create_time = db.DateTimeField(default=dt.datetime.now())  # 部门创建时间
    create_by = db.StringField()  # 创建者
    update_time = db.DateTimeField()  # 更新时间
    update_by = db.StringField  # 更新者
    status = db.StringField(choices=['1', '2', '3'], default=1)  # 部门状态("1",正常，"2":停用 "3":删除)


class Contact(db.EmbeddedDocument):
    """本机构与其它机构的关系"""
    org_id = db.StringField()  # 部门唯一id
    org_name = db.StringField()  # 机构名称
    org_type = db.StringField(choices=[type_suppliers, type_buyers, type_logistics])  # 机构类别(供应商，采购商,物流)
    pay_type = db.ListField(choice=[pay_cash, pay_prepaid, pay_account_period, pay_credit_sale],
                            default=[])  # 付款方式(现金,预付,账期,赊销)
    create_time = db.DateTimeField(default=dt.datetime.now())


class Sys_org(db.Document):
    """
    机构信息表
    """
    meta = {
        'collection': 'sys_org'
        # 'collection': 'sys_org_test'
    }
    org_code = db.StringField(unique=True, required=False)  # 机构编码
    org_id = db.StringField()  # 机构唯一id
    org_name = db.StringField()  # 机构名称
    org_short_name = db.StringField()  # 机构简称
    contacts = db.StringField()  # 联系人名称
    bl_code = db.StringField()  # 经营编码
    registered_capital = db.StringField()  # 注册资金
    longitude = db.StringField()  # 经度
    latitude = db.StringField()  # 纬度
    org_area = db.StringField()  # 机构所在区域编码
    master = db.StringField()  # 法人名称
    bl_address = db.StringField()  # 经营地址
    mail = db.EmailField(max_length=80)  # 邮箱
    mobile = db.StringField()  # 电话号码
    bl_img = db.StringField()  # 营业执照照片
    door_img = db.StringField()  # 门头照
    cashier_img = db.StringField()  # 收银台照
    authorization_img = db.StringField()  # 授权书照
    bank_cart_info = db.EmbeddedDocumentField('Bank_cart_info')  # 用户银行卡信息
    id_card_info = db.EmbeddedDocumentField('Id_card_info')  # 用户身份证信息
    wallet = db.EmbeddedDocumentField('OrgWallet')  # 用户钱包信息
    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField(default=dt.datetime.now())  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间
    website = db.StringField()  # 网址
    remarks = db.StringField()  # 备注
    audit = db.BooleanField()  # 是否审核（True：是；False：否）
    org_type = db.StringField()  # 机构类型
    department = db.ListField(db.EmbeddedDocumentField('Department'))  # 部门
    status = db.IntField(choices=[0, 1, 2], default=0)  # 状态("0",正常，"1":停用 "2":删除)
    org_relations = db.ListField(db.EmbeddedDocumentField('Contact'), default=[])

    # 从字典表获取状态
    @staticmethod
    def get_status(dict_name):
        data = SysDict.get_dict_by_type_and_name(dict_type='public_status', dict_name=dict_name)
        return data.dict_id

    # 支付密码
    @property
    def pay_password(self):
        if self.wallet.pay_password:
            return True
        return False

    @pay_password.setter
    def pay_password(self, pay_password):
        self.wallet.pay_password = generate_password_hash(pay_password)
        self.save()

    def check_pay_password(self, pay_password):
        return check_password_hash(self.wallet.pay_password, pay_password)

    @classmethod
    def create_department_code(cls, org_code, father_department_code=None):
        """
        创建部门编码
        :param org_code: 要添加部门的机构
        :param father_department_code: 选择的所属部门
        :return:
        by denghaolin
        """
        try:
            # 没有所属部门，即添加顶级部门
            if not father_department_code:
                # 查询该机构下顶级的部门的个数
                org_obj = cls.objects(org_code=org_code, status__in=[0, 1]).first()
                department_count = len(org_obj.department)
                # 该机构下没有部门
                if not department_count:
                    department_code = SysDict.get_dict_list_by_type(dict_type='department_code')[0].description
                    return department_code
                else:
                    # 根据已有的部门，追加要添加的顶级部门
                    temp_department_code = int(department_count) + 1
                    # 不足4位时自动补0的函数
                    department_code = str(temp_department_code).zfill(4)
                    return department_code
            # 有所属部门
            else:
                # 查询该机构下的部门下的子部门
                search = [{"$unwind": "$department"},
                          {'$match': {'org_code': org_code,
                                      '$and': [{'department.status': {
                                          '$in': [re.compile(department_status_normal),
                                                  re.compile(department_status_block_up)]}},
                                          {'department.code': re.compile(r"^" + father_department_code + "[0-9]{4}$")}],
                                      }},
                          {'$project': {'department': 1,
                                        }}
                          ]
                child_departments = list(cls.objects.aggregate(*search))
                child_department_count = len(child_departments)
                # 根据已有的子部门，追加要添加的部门
                temp_department_code = int(child_department_count) + 1
                # 不足4位时自动补0的函数
                temp_departmenr = str(temp_department_code).zfill(4)
                insert_department_code = str(father_department_code) + str(temp_departmenr)
                return insert_department_code
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_department(cls, org_code, department_name='', department_code=None, block_up=False, page=1, per_page=10, sort='create_time', sortOrder=-1):
        """
        根据机构编号获取本机构下所有部门信息
        :param org_code:
        :param department_name: 部门名称
        :param department_code: 是否包含该部门
        :param block_up: 是否显示停用的部门
        :param page:
        :param per_page:
        :param sort:
        :return:
        by denghaolin
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = []
            search.append({"$unwind": "$department"})
            search.append({'$match': {'org_code': org_code,
                                      '$and': [{'department.status': {
                                          '$in': [re.compile(department_status_normal),
                                                  re.compile(department_status_block_up) if block_up else '']},
                                          'department.code': {'$ne': department_code if department_code else ''}}],
                                      '$or': [{'department.name': re.compile(department_name)}],
                                      }})
            search.append({'$sort': {'department.' + sort: sortOrder}})
            search.append({'$project': {'department': 1, }})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})
            departments = list(cls.objects.aggregate(*search))
            return departments, count
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exist_department(cls, org_code, department_name):
        """
        获取同一机构下是否存在相同的部门
        :param org_code: 机构编号
        :param department_name: 部门编号
        :return:
        by denghaolin
        """
        try:
            search = [{"$unwind": "$department"},
                      {'$match': {'org_code': org_code,
                                  '$and': [{'department.status': {
                                      '$in': [re.compile(department_status_normal),
                                              re.compile(department_status_block_up)]},
                                      'department.name': department_name}],
                                  }},
                      {'$sort': {'create_time': -1}},
                      {'$project': {'department': 1,
                                    }},
                      ]
            department = list(cls.objects.aggregate(*search))
            return department
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def add_department(cls, params):
        """
        新增部门
        :param params:
        :return:
        by denghaolin
        """
        try:
            org_code = params.get('org_code')
            org_obj = cls.get_org_info(org_code)
            father_department_code = params.get('father_department')
            department_code = cls.create_department_code(org_code=org_code,
                                                         father_department_code=father_department_code)  # 生成部门code
            department_id = create_department_id()  # 生成部门id
            logging.info(department_code)
            department_name = params.get('name')
            status = params.get('status')
            create_time = dt.datetime.now()
            create_by = current_user.user_code
            department = Department(id=department_id, code=department_code, name=department_name, status=status,
                                    create_time=create_time, create_by=create_by)
            old_department = org_obj.department
            old_department.append(department)
            # org_obj.department = list(department)
            org_obj.update(department=old_department)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def edit_department(cls, params):
        """
        编辑部门
        :param params:
        :return:
        by denghaolin
        """
        try:
            org_code = params.get('org_code')
            org_obj = cls.get_org_info(org_code)  # 获取编辑部门的机构对象
            org_departments = org_obj.department  # 获取编辑部门的机构对象下的所有部门
            department_code = params.get('department_code')
            departments_names = []
            for department in org_departments:
                if department.code == department_code:
                    edit_department_obj = department
            old_department_name = edit_department_obj.name  # 编辑前的部门名称
            old_department_status = edit_department_obj.status  # 获取编辑前的部门状态
            old_department_father_department_code = str(edit_department_obj.code)[:-4]  # 获取编辑前的所属部门
            # 修改了部门名称
            if old_department_name != params.get('name'):
                # 判断该机构下除该部门编辑前的名称外是否有相同的部门名称
                for department in org_departments:
                    if department.status != department_status_delete:
                        if department.code != department_code:
                            departments_names.append(department.name)
                if params.get('name') in departments_names:
                    return response.ERROR
                # 修改基础字段
                for department in org_departments:
                    if department.code == department_code:  # 编辑部门对象
                        department.name = params.get('name')
                        department.update_time = dt.datetime.now()
                        department.update_by = current_user.user_code
                org_obj.update(department=org_departments)
            # 修改了部门状态且修改状态为停用，修改下属部门均为停用
            if old_department_status != params.get('status') and params.get('status') == department_status_block_up:
                for department in org_departments:
                    # 获取该部门及其下属部门并停用
                    if str(department.code).startswith(department_code):
                        department.status = department_status_block_up
                        department.update_time = dt.datetime.now()
                        department.update_by = current_user.user_code
                org_obj.update(department=org_departments)
            # 原本为停用，修改为正常
            elif old_department_status != params.get('status') and params.get('status') == department_status_normal:
                for department in org_departments:
                    if department.code == department_code:  # 编辑部门对象
                        department.status = department_status_normal
                        department.update_time = dt.datetime.now()
                        department.update_by = current_user.user_code
                org_obj.update(department=org_departments)
            # 修改了部门所属部门
            if old_department_father_department_code != params.get('father_department'):
                # 生成新的部门department_code
                new_department_code = cls.create_department_code(org_code=org_code,
                                                                 father_department_code=params.get('father_department'))
                # 从头开始匹配编辑部门，获取编辑部门及其下属部门
                department_re = re.compile(r'^{}'.format(department_code))
                # 替换编辑部门的下属部门的原所属部门为新所属部门
                for department in org_departments:
                    new_son_department_code = department_re.sub(new_department_code, department.code)
                    department.code = new_son_department_code
                    department.update_time = dt.datetime.now()
                    department.update_by = current_user.user_code
                org_obj.update(department=org_departments)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def delete_department(cls, params):
        """
        删除部门
        :param params:
        :return:
        by denghaolin
        """
        try:
            org_code = params.get('org_code')
            org_obj = cls.get_org_info(org_code)  # 获取编辑部门的机构对象
            department_code = params.get('department_code')
            org_departments = org_obj.department  # 获取该机构下所有部门
            for department in org_departments:
                # 获取该部门及其下属部门并删除
                if str(department.code).startswith(department_code):
                    department.status = department_status_delete
                    department.update_time = dt.datetime.now()
                    department.update_by = current_user.user_code
            org_obj.update(department=org_departments)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_department_info(cls, org_code, department_code):
        """
        获取部门信息
        :return:
        """
        try:
            org_obj = cls.get_org_info(org_code)  # 获取编辑部门的机构对象
            org_departments = org_obj.department  # 获取该机构下所有部门
            for department in org_departments:
                if str(department.code) == department_code:
                    return department
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_department_info_by_org_id_and_department_id(cls, org_id, department_id):
        """
        根据机构id和部门id获取部门对象
        :param org_id:
        :param department_id:
        :return:
        """
        try:
            search = [{"$unwind": "$department"},
                      {'$match': {'org_id': org_id,
                                  '$and': [{'department.status': {
                                      '$in': [re.compile(department_status_normal),
                                              re.compile(department_status_block_up)]},
                                      'department.id': {'$in': department_id}}],
                                  }},
                      {'$sort': {'create_time': -1}},
                      {'$project': {'department': 1,
                                    }},
                      ]
            department = list(cls.objects.aggregate(*search))
            return department

        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_father_department(cls, org_code, department_code):
        """
        获取上级部门名称
        :param org_code:
        :param department_code:
        :return:
        """
        try:
            fa_code = str(department_code)[:-4]  # 去掉department_code的后四位得到上级部门department_code
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
                {'$match': {'$and': [{"sys_org.org_code": re.compile(r'^{}$'.format(org_code))},
                                     {'department.code': re.compile(r'^{}$'.format(fa_code))}, ],
                            },
                 },
                {'$project': {
                    "department.name": 1,
                    "department.code": 1
                }},
            ]
            departments = list(cls.objects.aggregate(*search))[0].get('department')
            for department in departments:
                if department.get('code') == fa_code:
                    # fa_name = department.get('name')
                    return department
                    # return cls.objects(org_code=org_code, department__code=fa_code, status__in=[0, 1]).first()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def deleted(cls, org_code):
        """
        系统删除机构信息
        :param org_code:
        :return:
        """
        try:
            org = cls.objects(org_code=org_code).first()
            if not org:
                return response.ERROR
            update_time = dt.datetime.now()
            update_by = current_user.user_code
            # 获取该机构及其下属机构
            org_list = cls.find_son_sys_org(org_code)
            # 替换编辑对象的下属机构的原所属机构为新所属机构
            for org in org_list:
                org.status = 2
                org.update_by = current_user.user_code
                org.update_time = dt.datetime.now()
                org.save()
            from rich_base_provider.sysadmin.sys_role.models import Role
            # 删除sys_role下对应的角色
            roles = Role.get_role_by_org_code(org_code)  # 获取对应的角色列表
            for role in roles:
                role.role_status = 2
                role.update_time = update_time
                role.update_by = update_by
                role.save()
            # 删除sys_user下对应的用户
            from rich_base_provider.sysadmin.sys_user.models import User
            users = User.objects.filter(status__in=[0, 1]).filter(org_role__org_code=org_code).all()  # 获取对应的角色列表
            if users:
                for user in users:
                    for item in user.org_role:
                        if item['org_code'] == org_code:
                            user.org_role.remove(item)
                            user.update_time = update_time
                            user.update_by = update_by
                            user.save()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_org_info(cls, org_code):
        '''
        根据机构编号查询机构信息
        by:chenwanyue
        :param org_code:
        :return:
        '''
        org_obj = cls.objects(org_code=org_code, status__in=[0, 1]).first()
        if org_obj:
            return org_obj
        return None

    @classmethod
    def get_org_info_by_org_name(cls, org_name):
        """
        根据机构名称查询机构信息
        by:zbh
        :param org_name:
        :return:
        """
        org_obj = cls.objects(org_name=org_name, status__in=[0, 1]).first()
        if org_obj:
            return org_obj
        return None

    @classmethod
    def get_org_name_by_org_id(cls, org_id):
        """
        根据org_id获取本机构机构名称
        :param org_id:
        :return:
        """
        org_obj = cls.objects(org_id=org_id).only("org_name", "org_code").first()
        if org_obj:
            return org_obj
        else:
            return None

    @classmethod
    def get_org_name_by_org_id_list(cls, org_id_list):
        """
        根据org_id获取本机构机构名称
        :param org_id:
        :return:
        """
        org_obj_list = cls.objects(org_id__in=org_id_list).only("org_name", "org_id").all()
        if org_obj_list:
            return org_obj_list
        else:
            return None

    @classmethod
    def get_all_org_info(cls):
        """
        获取所有机构的信息
        :return:
        by denghaolin
        """
        all_org_obj_list = cls.objects(status__in=[0, 1]).all()
        if all_org_obj_list:
            return all_org_obj_list
        return None

    @classmethod
    def find_sysorg(cls, org_code, org_name='', page=1, per_page=10, order_by_param='create_time'):
        """
        根据机构编号获取本机构旗下包括自己的所有机构信息
        :param org_code:
        :return:
        by denghaolin
        """
        try:
            search = {
                '__raw__': {
                    'org_name': re.compile(org_name),
                    'org_code': re.compile(r'^{}'.format(org_code)),
                    'status': {'$ne': 2}
                },
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            orgs = cls.objects(**search).skip(skip_nums).limit(int(per_page)).order_by(
                order_by_param)
            count = cls.objects(**search).count()
            return {"orgs": orgs, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_sysorg_by_data(cls, org_code, org_name=""):
        """
        根据机构编号获取本机构旗下包括自己的所有机构信息
        :param org_code:
        :param org_name:
        :return:
        """
        try:
            search = {
                '__raw__': {
                    'org_name': re.compile(org_name),
                    'org_code': re.compile(r"^" + org_code + ".*$"),
                    'status': {'$ne': 2}
                },
            }
            return cls.objects(**search).all()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_son_sysorg(cls, org_code):
        """
        根据机构编号获取本机构旗下所有机构信息
        :param org_code:
        :return:
        """
        return cls.objects(org_code__startswith=org_code, status__in=[0, 1]).order_by("org_code").all()

    @classmethod
    def change_org_balance(cls, change_type, change_money_count):
        """
        根据余额改变方式（recharge 充值 （消费...）） 改变金额大小, 机构ID对某机构钱包余额进行更新
        :param change_type:
        :param change_money_count:
        :return:
        """
        current_org_obj = Sys_org.get_org_info(session.get("org_code"))
        old_org_balance = current_org_obj.wallet.balance
        if change_type == "recharge":
            current_org_obj.wallet.balance = old_org_balance + float(change_money_count)
            current_org_obj.save()

    @classmethod
    def change_org_point(cls, change_type, change_point_count, way):
        """
        根据积分改变方式（get 获取 post 消费）改变机构积分数目
        :param change_type:
        :param change_point_count:
        :param way:
        :return:
        """
        current_org_obj = Sys_org.get_org_info(session.get("org_code"))
        old_org_point = current_org_obj.wallet.point
        if change_type == "get":
            current_org_obj.wallet.point = old_org_point + int(change_point_count)
            # 添加积分流水记录
            new_point_record = PointRecord(time=dt.datetime.now(), get="1", post="0",
                                           amount=change_point_count, org_code=session.get("org_code"),
                                           way=way, point_sum=old_org_point + int(change_point_count))
            current_org_obj.wallet.point_record.append(new_point_record)
            current_org_obj.save()

    @classmethod
    def get_sys_son_orgs(cls, org_code, search_data='', page=1, per_page=10):
        """
        根据机构编号获取本机构旗下所有子机构信息
        :param org_code:
        :return:
        by shuyi
        """
        try:

            search = {
                '__raw__': {
                    '$and': [
                        {'org_code': re.compile(r"^" + org_code + ".*$")},
                        {'org_code': {'$ne': org_code}},
                        {'status': {'$ne': 2}}
                    ],
                    '$or': [{'org_name': re.compile(search_data)},
                            {'org_id': re.compile(search_data)},
                            {'mobile': re.compile(search_data)}, ]
                },
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            orgs = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            return orgs
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_son_sysorg_count(cls, org_code):
        """
        根据机构编号获取本机构旗下所有机构信息数量
        :param org_code:
        :return:
        """
        return cls.objects(org_code__startswith=org_code, status__in=[0, 1]).count()

    @classmethod
    def find_son_sys_org(cls, org_code):
        """
        查询子机构
        :param org_code:
        :return:
        by denghaolin
        """
        try:
            search_re = "(^" + org_code + ".*$)" + "(?!(" + org_code + "))"
            search = {
                '__raw__': {
                    'org_code': re.compile(search_re),
                    'status': {'$ne': 2}
                },
            }
            return cls.objects(**search)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_father_sysorg(cls, org_code):
        """
        查询上级机构,不管是否已删除,用于渲染机构管理所属机构
        :param org_code:
        :return:
        by denghaolin
        """
        try:
            # 顶级机构
            if str(org_code) == '0001':
                return cls.objects(org_code=org_code).first()
            fa_code = str(org_code)[:-4]  # 去掉org_code的后四位得到上级机构org_code
            return cls.objects(org_code=fa_code).first()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exist_mail(cls, query_mail):
        """
        查询是否存在该邮箱
        :param query_mail:
        :return:
        by denghaolin
        """
        try:
            exist_mail = Sys_org.objects(mail__exact=query_mail, status__in=[0, 1]).first()
            if exist_mail:
                return True
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exist_name(cls, query_name):
        """
        查询是否存在相同的机构名
        :param query_name:  要查询的机构名
        :return:
        """
        try:
            exist_name = Sys_org.objects(org_name__exact=query_name, status__in=[0, 1]).first()
            if exist_name:
                return True
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exist_mobile(cls, query_mobile):
        """
        查询是否存在相同的手机号
        :param query_mobile:  要查询的手机号
        :return:
        """
        try:
            exist_mobile = Sys_org.objects(mobile__exact=query_mobile, status__in=[0, 1]).first()
            if exist_mobile:
                return True
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_exist_id_card_num(cls, query_id_num):
        """
        查询是否存在相同的身份证号
        :param query_id_num:  要查询的身份证号
        :return:
        """
        try:
            exist_num = cls.objects.filter(id_card_info__idcard_number=query_id_num).first()
            if exist_num:
                return True
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_by(cls, **kwargs):
        """
        使用机构名,邮件,身份证号, 联系电话查询用户信息。
        :param kwargs:
        :return:
        """
        logging.info('get_by')
        try:
            if kwargs.get('org_name'):
                org = cls.objects(org_name=kwargs.get('org_name'), status__in=[0, 1]).first()
                return org
            if kwargs.get('mail'):
                org = cls.objects(mail=kwargs.get('mail'), status__in=[0, 1]).first()
                return org
            if kwargs.get('idcard_number'):
                org = cls.objects(id_card_info__idcard_number=kwargs.get('idcard_number'), status__in=[0, 1]).first()
                return org
            if kwargs.get('mobile'):
                org = cls.objects(mobile=kwargs.get('mobile'), status__in=[0, 1]).first()
                return org
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def create_org_code(cls, org_code):
        """
        创建org_code
        :param org_code: 用户选择的所属机构
        :return:
        """
        # 获取用户选择的所属机构的子机构的数量
        # 以org_code为开头的，长度为4的正则匹配   (即匹配用户选择所属机构的下属机构)
        search = {
            'org_code': re.compile(r"^" + org_code + "[0-9]{4}$")
        }
        child_org_count = cls.objects(**search).count()
        # 根据已有的子机构，追加要添加的机构
        temp_org_code = int(child_org_count) + 1
        # 不足4位时自动补0的函数
        temp_org = str(temp_org_code).zfill(4)
        insert_org_code = str(org_code) + str(temp_org)
        return insert_org_code

    @classmethod
    def insert_org(cls, req_data, org_code):
        """
        新增机构
        :param req_data: 包含请求的所有数据
        :param org_code: 插入的org_code
        :return:
        by denghaolin
        """
        try:
            create_by = current_user.user_code
            create_time = dt.datetime.now()
            org_id = create_org_id()  # 获取机构唯一id
            # 获取请求的身份证信息数据
            from rich_base_provider.sysadmin.sys_org.views import save_img
            # 获取图片url
            cert_correct_img_url = save_img(req_data.get('cert_correct_img', ''), org_code + 'cert_correct_img')
            cert_opposite_img_url = save_img(req_data.get('cert_opposite_img', ''), org_code + 'cert_opposite_img')
            hand_id_card_img_url = save_img(req_data.get('hand_id_card_img', ''), org_code + 'hand_id_card_img')
            id_card_info = Id_card_info(idcard_type=req_data.get('idcard_type', ''),
                                        idcard_number=req_data.get('idcard_number', ''),
                                        cert_correct_img=cert_correct_img_url,
                                        cert_opposite_img=cert_opposite_img_url,
                                        hand_id_card_img=hand_id_card_img_url,
                                        concrete_address=req_data.get('concrete_address', ''))
            # 获取请求的银行卡信息数据
            card_opposite_img_url = save_img(req_data.get('card_opposite_img', ''), org_code + 'card_opposite_img')
            card_correct_img_url = save_img(req_data.get('card_correct_img', ''), org_code + 'card_correct_img')
            bank_cart_info = Bank_cart_info(bank_card_type=req_data.get('bank_card_type', ''),
                                            bank_account=req_data.get('bank_account', ''),
                                            bank_name=req_data.get('bank_name', ''),
                                            bank_owner=req_data.get('bank_owner', ''),
                                            bank_address=req_data.get('bank_address'),
                                            card_opposite_img=card_opposite_img_url,
                                            card_correct_img=card_correct_img_url,
                                            mobile=req_data.get('bank_bind_mobile', ''))
            # 获取请求的钱包信息数据
            req_wallet_info = req_data.get('wallet')
            if req_wallet_info:
                # 子集数据结构 -- "coupons": [{"coupon_code": "987456123", "org_code": "0001", "use_time": "2018-09-14"}]
                req_coupons = req_wallet_info.get('coupons', [])  # 获取钱包下的优惠券信息
                req_point_reqord = req_wallet_info.get('point_record', [])  # 获取钱包下的积分记录
                req_transaction = req_wallet_info.get('transaction', [])  # 获取钱包下的交易记录
                # 处理用户钱包
                wallet = OrgWallet(coupons=req_coupons, point_record=req_point_reqord, transaction=req_transaction,
                                   point=req_wallet_info.get('point', 0), balance=req_wallet_info.get('balance'))
            else:
                wallet = OrgWallet()
            # 获取地区名
            area_name = req_data.get('area_name', '')
            if area_name:
                longitude, latitude = get_longitude_latitude(area_name)  # 地区名转换为经纬度
            bl_img_url = save_img(req_data.get('bl_img', ''), org_code + 'bl_img')
            door_img_url = save_img(req_data.get('door_img', ''), org_code + 'door_img')
            cashier_img_url = save_img(req_data.get('cashier_img', ''), org_code + 'cashier_img')
            sys_org = Sys_org(org_code=org_code, org_name=req_data.get('org_name', ''), org_id=org_id,
                              org_short_name=req_data.get('org_short_name', ''),
                              contacts=req_data.get('contacts', ''),
                              bl_code=req_data.get('bl_code', ''),
                              registered_capital=req_data.get('registered_capital', ''),
                              bl_img=bl_img_url, door_img=door_img_url,
                              cashier_img=cashier_img_url,
                              latitude=str(latitude), longitude=str(longitude), org_area=req_data.get('org_area', ''),
                              master=req_data.get('master', ''), bl_address=req_data.get('bl_address', ''),
                              mail=req_data.get('mail', ''), mobile=req_data.get('mobile', ''),
                              website=req_data.get('website', ''), remarks=req_data.get('remarks', ''),
                              org_type=req_data.get('org_type', ''), audit=req_data.get('audit', False),
                              status=req_data.get('status', 0), id_card_info=id_card_info,
                              bank_cart_info=bank_cart_info, wallet=wallet, create_by=create_by,
                              create_time=create_time)
            sys_org.save()
            return True
        except Exception as e:
            logging.debug(e)
            return False

    @classmethod
    def edit_org(cls, org_obj, edit_data):
        """
        更新机构
        :param org_obj: 待编辑的机构对象
        :param edit_data: 编辑的数据
        :return:
        by denghaolin
        """
        try:
            # 验证数据唯一性
            from rich_base_provider.sysadmin.sys_org.views import check_edit_org
            check_msg = check_edit_org(org_obj=org_obj, org_name=edit_data.get('org_name'), mail=edit_data.get('mail'),
                                       idcard_number=edit_data.get('idcard_number'),
                                       mobile=edit_data.get('mobile'))
            if check_msg:
                res_msg = ''
                for key, value in check_msg.items():
                    res_msg += value
                return response.ERROR, res_msg
            # 用户更改所属机构
            father_org_code = edit_data.get('father_org_code')  # 要更改的所属机构
            old_father_org_code = str(org_obj.org_code)[:-4]  # 原所属机构
            # 编辑顶级机构
            from rich_base_provider.sysadmin.sys_dict.models import SysDict
            if str(org_obj.org_code) == SysDict.get_dict_list_by_type(dict_type='org_code')[0].description:
                old_father_org_code = str(org_obj.org_code)
            if str(old_father_org_code) != str(father_org_code):  # 用户更改了所属机构
                # 查询用户所更改的所属机构是否存在
                father_org = cls.get_org_info(father_org_code)
                if not father_org:
                    return response.ERROR, '所选择的所属机构不存在'
                new_org_code = cls.create_org_code(father_org_code)  # 生成待编辑的机构的新机构号
                # 获取原本该机构及其下属机构
                old_org_list = cls.find_son_sys_org(org_obj.org_code)
                org_re = re.compile(r'^{}'.format(org_obj.org_code))  # 从头开始匹配编辑对象的下属机构的原所属机构
                # 替换编辑对象的下属机构的原所属机构为新所属机构
                for old_org in old_org_list:
                    new_son_org_code = org_re.sub(new_org_code, old_org.org_code)
                    old_org.org_code = new_son_org_code
                    old_org.update_by = current_user.user_code
                    old_org.update_time = dt.datetime.now()
                    old_org.save()
            # 获取请求的身份证信息数据
            from rich_base_provider.sysadmin.sys_org.views import save_img
            cert_correct_img_url = org_obj.id_card_info.cert_correct_img
            cert_opposite_img_url = org_obj.id_card_info.cert_opposite_img
            hand_id_card_img_url = org_obj.id_card_info.hand_id_card_img
            if edit_data.get('cert_correct_img'):
                cert_correct_img_url = save_img(edit_data.get('cert_correct_img', ''),
                                                org_obj.org_code + str(time.time()).split('.')[0] + 'cert_correct_img')
            if edit_data.get('cert_opposite_img'):
                cert_opposite_img_url = save_img(edit_data.get('cert_opposite_img', ''),
                                                 org_obj.org_code + str(time.time()).split('.')[
                                                     0] + 'cert_opposite_img')
            if edit_data.get('hand_id_card_img'):
                hand_id_card_img_url = save_img(edit_data.get('hand_id_card_img', ''),
                                                org_obj.org_code + str(time.time()).split('.')[0] + 'hand_id_card_img')
            id_card_info = Id_card_info(idcard_type=edit_data.get('idcard_type', ''),
                                        idcard_number=edit_data.get('idcard_number'),
                                        cert_correct_img=cert_correct_img_url,
                                        cert_opposite_img=cert_opposite_img_url,
                                        hand_id_card_img=hand_id_card_img_url,
                                        concrete_address=edit_data.get('concrete_address', ''))
            # 获取请求的银行卡信息数据
            card_correct_img_url = org_obj.bank_cart_info.card_correct_img
            card_opposite_img_url = org_obj.bank_cart_info.card_opposite_img
            if edit_data.get('card_opposite_img'):
                card_opposite_img_url = save_img(edit_data.get('card_opposite_img', ''),
                                                 org_obj.org_code + str(time.time()).split('.')[
                                                     0] + 'card_opposite_img')
            if edit_data.get('card_correct_img'):
                card_correct_img_url = save_img(edit_data.get('card_correct_img', ''),
                                                org_obj.org_code + str(time.time()).split('.')[0] + 'card_correct_img')
            bank_cart_info = Bank_cart_info(bank_card_type=edit_data.get('bank_card_type', ''),
                                            bank_account=edit_data.get('bank_account', ''),
                                            bank_name=edit_data.get('bank_name', ''),
                                            bank_owner=edit_data.get('bank_owner', ''),
                                            bank_address=edit_data.get('bank_address'),
                                            card_opposite_img=card_opposite_img_url,
                                            card_correct_img=card_correct_img_url,
                                            mobile=edit_data.get('bank_bind_mobile', ''))
            # 获取请求的钱包信息数据
            req_wallet_info = edit_data.get('wallet')
            if req_wallet_info:
                # 子集数据结构 -- "coupons": [{"coupon_code": "987456123", "org_obj.org_code": "0001", "use_time": "2018-09-14"}]
                req_coupons = req_wallet_info.get('coupons', [])  # 获取钱包下的优惠券信息
                req_point_reqord = req_wallet_info.get('point_record', [])  # 获取钱包下的积分记录
                req_transaction = req_wallet_info.get('transaction', [])  # 获取钱包下的交易记录
                # 处理用户钱包
                wallet = OrgWallet(coupons=req_coupons, point_record=req_point_reqord, transaction=req_transaction,
                                   point=req_wallet_info.get('point', 0), balance=req_wallet_info.get('balance'))
            else:
                wallet = OrgWallet()
            # 获取地区名
            area_name = edit_data.get('area_name', '')
            if area_name:
                longitude, latitude = get_longitude_latitude(area_name)  # 地区名转换为经纬度
            bl_img_url = org_obj.bl_img
            door_img_url = org_obj.door_img
            cashier_img_url = org_obj.cashier_img
            if edit_data.get('bl_img'):
                bl_img_url = save_img(edit_data.get('bl_img', ''),
                                      org_obj.org_code + str(time.time()).split('.')[0] + 'bl_img')
            if edit_data.get('door_img'):
                door_img_url = save_img(edit_data.get('door_img', ''),
                                        org_obj.org_code + str(time.time()).split('.')[0] + 'door_img')
            if edit_data.get('cashier_img'):
                cashier_img_url = save_img(edit_data.get('cashier_img', ''),
                                           org_obj.org_code + str(time.time()).split('.')[0] + 'cashier_img')
            org_obj.update(org_name=edit_data.get('org_name'), mail=edit_data.get('mail'), bl_img=bl_img_url,
                           org_short_name=edit_data.get('org_short_name', ''),
                           contacts=edit_data.get('contacts', ''), bl_code=edit_data.get('bl_code', ''),
                           registered_capital=edit_data.get('registered_capital', ''),
                           door_img=door_img_url, cashier_img=cashier_img_url,
                           org_area=edit_data.get('org_area', ''), latitude=str(latitude), longitude=str(longitude),
                           master=edit_data.get('master', ''), bl_address=edit_data.get('bl_address', ''),
                           mobile=edit_data.get('mobile'), website=edit_data.get('website', ''),
                           remarks=edit_data.get('remarks', ''), org_type=edit_data.get('org_type', ''),
                           audit=edit_data.get('audit', False), status=edit_data.get('status', 0),
                           id_card_info=id_card_info, bank_cart_info=bank_cart_info, wallet=wallet,
                           update_time=dt.datetime.now(), update_by=current_user.user_code)
            return response.SUCCESS, '编辑成功'
        except Exception as e:
            logging.debug(e)
            return response.ERROR

    @classmethod
    def add_mechanism_contact(cls, org_name, contact_type, pay_type, username):
        """
        添加机构关联
        :param : org_name: 机构名字
        :param : contact_type： 机构联系
        :param : pay_type： 付款方式
        :param : username: 用户
        :return :
        """
        pay_type = [i for i in pay_type]
        r = Sys_org.objects(org_name=org_name).first()
        org_id = r.org_id
        user = Sys_org.objects(org_name=username).first()
        contact = Contact(org_id=org_id, org_name=org_name, org_type=contact_type, pay_type=pay_type)
        user.org_relations.append(contact)
        user.save()

    @classmethod
    def get_edit_by(cls, org_obj, **kwargs):
        """
        机构编辑查询是否存在除自己本身外相同的机构名,邮件,身份证号, 联系电话
        :param org_obj:
        :param kwargs:
        :return:
        by denghaolin
        """
        logging.info('get_edit_by')
        try:
            if kwargs.get('org_name'):
                old_org_name = org_obj.org_name
                org = cls.objects(org_name__exact=kwargs.get('org_name'), org_name__ne=old_org_name).first()
                return org
            if kwargs.get('mail'):
                old_mail = org_obj.mail
                org = cls.objects(mail__exact=kwargs.get('mail'), mail__ne=old_mail).first()
                return org
            if kwargs.get('idcard_number'):
                old_idcard_number = org_obj.id_card_info.idcard_number
                org = cls.objects(id_card_info__idcard_number__exact=kwargs.get('idcard_number'),
                                  id_card_info__idcard_number__ne=old_idcard_number).first()
                return org
            if kwargs.get('mobile'):
                old_mobile = org_obj.mobile
                org = cls.objects(mobile__exact=kwargs.get('mobile'), mobile__ne=old_mobile).first()
                return org
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_org_info_by_org_id(cls, org_id):
        """
        根据org_id获取机构信息
        :param org_id:
        :return:
        """
        org_obj = cls.objects(org_id=org_id, status__in=[0, 1]).first()
        if org_obj:
            return org_obj
        return None


    @classmethod
    def find_sysorg_without_myself(cls, org_code, org_name='', page=1, per_page=10):
        """
        根据机构编号获取本机构旗下的所有机构信息
        :param org_code:
        :return:
        by denghaolin
        """
        try:
            search = {
                '__raw__': {
                    'org_code': {'$regex': "(^" + org_code + ".*$)" + "(?!(" + org_code + "))"},
                    'status': {'$ne': 2},
                    '$or': [{'org_name': re.compile(org_name)}]
                },
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            orgs = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            count = cls.objects(**search).count()
            return {"orgs": orgs, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def find_other_sysorg(cls, org_code, org_name='', page=1, per_page=10):
        """
        根据机构编号获取除本机构及下属机构的所有机构信息
        :param org_code:
        :return:
        """
        try:
            org_code_and_son_org_code = cls.find_son_sys_org(org_code)
            search = {
                '__raw__': {
                    'org_code': {'$nin': [org_obj.org_code for org_obj in org_code_and_son_org_code]},
                    'status': {'$ne': 2},
                    '$or': [{'org_name': re.compile(org_name)}]
                },
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            orgs = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            count = cls.objects(**search).count()
            return {"orgs": orgs, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e

    # 钱包操作
    def update_bank_card_info(self, bank_card_list):
        """
        更新钱包银行卡信息
        :param bank_card_list:
        :return:
        """
        try:
            bank_cards = self.wallet.bank_cards
            bank_cards.clear()
            for card in bank_card_list:
                org_bank_card = OrgBankCard(**card)
                bank_cards.append(org_bank_card)
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            return False

    def get_bank_cards_info(self):
        """
        获取银行卡信息
        :param :
        :return:
        """
        try:
            bank_cards = self.wallet.bank_cards
            card_info_list = []
            if bank_cards:
                bank_type_info = SysDict.get_dict_list_by_type('bank_type')
                bank_type_dict = {}
                for bank_type in bank_type_info:
                    bank_type_dict[bank_type.dict_id] = bank_type.dict_name
                for card in bank_cards:
                    card_info = dict(plant_bank_name=card.plant_bank_name,
                                     acc_no=card.acc_no,
                                     bank_type=bank_type_dict[card.bank_type]
                                     )
                    card_info_list.append(card_info)
            return card_info_list

        except Exception as e:
            raise e

    @classmethod
    def get_record_by_org_id(cls, org_id=None, start_time=None, end_time=None, page=1, per_page=20):
        """
        根据机构id获取积分获取记录对象
        :param org_id:
        :param start_time:
        :param end_time:
        :param page:
        :param per_page:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = []
            search.append({'$unwind': "$wallet.point_record"})
            if start_time and end_time:
                start_time = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = dt.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                search.append({'$match': {
                    '$and': [
                        {'org_id': org_id},
                        {'wallet.point_record.time': {'$gte': start_time}},
                        {'wallet.point_record.time': {'$lte': end_time}},
                    ],
                }})
            else:
                search.append({'$match': {
                    '$and': [
                        {'org_id': org_id},
                    ],
                }})
            search.append({'$sort': {'wallet.point_record.time': -1}})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append(
                {'$project': {'wallet.point_record.time': 1,
                              'wallet.point_record.amount': 1,
                              'wallet.point_record.org_code': 1,
                              'wallet.point_record.way': 1,
                              'wallet.point_record.point_sum': 1,
                              'org_name': 1,
                              }})
            search.append({'$skip': skip_nums})
            search.append({'$limit': per_page})
            record_list = list(cls.objects.aggregate(*search))
            return record_list, count
        except Exception as e:
            logging.debug(e)
            raise e

    # 使用优惠券
    @classmethod
    def use_coupon(cls, org_code, record_id, order_id):
        try:
            org = cls.get_org_info(org_code)
            for coupon in org.wallet.coupons:
                if coupon.record_id == record_id:  # 判断优惠券是否被使用
                    if not coupon.use_time:
                        coupon.order_id = order_id
                        coupon.use_time = dt.datetime.now()
                        org.save()
                        return True
                    else:
                        return False
            return False
        except Exception as e:
            raise e

    @classmethod
    def get_child_org(cls, org_code="", search_data="", page=1, per_page=12):
        """
        通过搜索,获取该机构下所有子机构的所有信息
        :param org_code:
        :param page:
        :param search_data:
        :param per_page:
        :return:
        by wujiehua
        """
        try:
            search = {
                '__raw__': {
                    'org_code': {'$regex': "(^" + org_code + ".*$)"},
                    'status': {'$ne': 2},
                    '$or': [{'org_name': re.compile(search_data),
                             'contacts': re.compile(search_data),
                             'bl_address': re.compile(search_data),
                             'mobile': re.compile(search_data)
                             }]
                }
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            orgs = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            count = cls.objects(**search).count()
            return {"orgs": orgs, "count": count}
        except Exception as e:
            logging.debug(e)
            raise e


def get_longitude_latitude(area_name):
    """
    根据地区名获取经纬度
    :param area_name:
    :return:
    by denghaolin
    """
    logging.info(get_longitude_latitude)
    try:
        url = Config.BAIDU_MAP_URL + '/?address=' + area_name + Config.BAIDU_OUTPUT
        response_data = requests.get(url)
        answer = response_data.json()
        return answer['result']['location']['lng'], answer['result']['location']['lat']
    except Exception as e:
        logging.debug(e)
        return '', ''
