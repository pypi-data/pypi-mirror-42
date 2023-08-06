#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 13:30
# @Author  : wangwei
# @Site    : www.rich-f.com
# @File    : models.py
# @Software: Rich Web Platform
# @Function: 用户模型

import json, time, logging, re
import datetime as dt
from dateutil.relativedelta import relativedelta
from flask import session

from rich_base_provider import db
from flask_security import UserMixin
from flask_security.utils import hash_password, verify_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import current_user

from rich_base_provider.sysadmin.sys_permission.models import Permissions
from rich_base_provider.sysadmin.sys_org.models import Sys_org
from rich_base_provider.sysadmin.sys_role.models import Role
from rich_base_provider.sysadmin.sys_dict.models import SysDict

dict_status_normal = 0
dict_status_block_up = 1
dict_status_delete = 2

dict_normal = "正常"
dict_block_up = "停用"
dict_delete = "删除"


def make_user_code():
    base_str = str(time.time()).replace('.', '')[:13]
    return 'U{:0<13}'.format(base_str)


class SocialOAuth(db.EmbeddedDocument):
    site = db.StringField(max_length=255)  # 第三方机构名  1、微信 2、QQ 3、微博
    uid = db.StringField(max_length=255)  # 第三方提供用户id
    open_id = db.StringField(max_length=255)
    site_uname = db.StringField(max_length=255)  # 第三方机构下用户名称（nickname）
    site_avatar = db.StringField(max_length=255)  # 第三方提供的头像 (headimagurl)
    access_token = db.StringField()  # 第三方提供访问令牌
    create_time = db.DateTimeField(default=dt.datetime.now)  # 创建时间
    update_time = db.DateTimeField()  # 更新时间


class UserAccount(db.EmbeddedDocument):
    """用户账号字段集合"""
    email = db.StringField(max_length=80, required=False)  # 用户邮箱
    mobile = db.StringField(max_length=16)  # 移动电话号码
    password = db.StringField(max_length=255)  # 密码hash值
    other_auth = db.EmbeddedDocumentField('SocialOAuth')  # 第三方账户信息
    active = db.BooleanField(default=True)  # 验证
    
    @property
    def _password(self):
        return self.password
    
    @_password.setter
    def _password(self, password):
        self.password = hash_password(password)
    
    def set_other_auth(cls, **kwargs):
        """
        设置第三方账户信息
        :param kwargs:
        :return:
        """
        
        oauth = SocialOAuth()
        oauth.site = kwargs.get('site')
        oauth.uid = kwargs.get('uid')
        oauth.open_id = kwargs.get('open_id')
        oauth.site_uname = kwargs.get('site_uname')
        oauth.site_avatar = kwargs.get('site_avatar')
        oauth.access_token = kwargs.get('access_token')
        oauth.create_time = kwargs.get('create_time')
        oauth.update_time = kwargs.get('update_time')
        cls.other_auth = oauth


class UserInfo(db.EmbeddedDocument):
    """用户详情信息"""
    name = db.StringField(max_length=64)  # 姓名
    birthday = db.DateTimeField()  # 生日
    gender = db.StringField(max_length=1, choices=['M', 'F', 'N'])  # 性别， 男:M (Male) 女:F (Female) 未知：N
    address = db.StringField(max_length=255, )  # 地址
    avatar = db.StringField(max_length=255, default='default.png')  # 头像地址
    id_card = db.DictField(default={})  # 身份证号:1121212,  dict


class Transactions(db.EmbeddedDocument):
    """交易记录"""
    transaction_id = db.StringField(max_length=255)  # 流水号
    create_time = db.DateTimeField(default=dt.datetime.now)  # 交易时间
    get = db.BooleanField(default=False)  # 是否为获取记录
    post = db.BooleanField(default=False)  # 是否为消费记录
    amount = db.FloatField()  # 交易金额
    org_code = db.StringField()  # 交易对象(机构）
    user_code = db.StringField()  # 交易对象（用户）
    balance = db.FloatField(default=0)  # 余额


class CouponRecords(db.EmbeddedDocument):
    """
    优惠券记录
    """
    record_id = db.StringField()  # 优惠券记录编码
    coupon_code = db.StringField()  # 优惠券编码
    get_time = db.DateTimeField(default=dt.datetime.now())  # 获取时间
    org_id = db.StringField()  # 来源
    order_id = db.StringField()  # 订单编号
    use_time = db.DateTimeField()  # 优惠券使用时间


class PointRecord(db.EmbeddedDocument):
    """积分记录"""
    create_time = db.DateTimeField(default=dt.datetime.now)  # 记录时间
    get = db.BooleanField(default=False)  # 是否为获取记录
    post = db.BooleanField(default=False)  # 是否为消费记录
    amount = db.IntField()  # 获取/消耗积分值
    org_code = db.StringField()  # 来源
    way = db.StringField(max_length=255)  # 获取方式
    point_sum = db.IntField(default=0)  # 积分余额


class UserBankCard(db.EmbeddedDocument):
    """用户银行卡"""
    acc_no = db.StringField()  # 银行卡后4位
    bank_type = db.StringField()  # 银行类型
    bind_id = db.StringField()  #
    customer_id = db.StringField()  # user_code
    issInsCode = db.StringField()  # 银行名缩写
    open_id = db.StringField()  #
    pay_type = db.StringField()  #
    plant_bank_name = db.StringField()  # 银行名
    telephone = db.StringField()  # 绑定银行卡电话号码


class UserWallet(db.EmbeddedDocument):
    """用户钱包"""
    coupons = db.ListField(db.EmbeddedDocumentField('CouponRecords'), default=[])  # TODO:优惠券，需要和优惠表关联
    point = db.IntField(default=0)  # 积分
    point_record = db.ListField(db.EmbeddedDocumentField('PointRecord'), default=[])  # 积分记录
    transaction = db.ListField(db.EmbeddedDocumentField('Transactions'), default=[])  # 交易记录
    balance = db.FloatField(min_value=0, default=0)  # 余额
    bank_cards = db.ListField(db.EmbeddedDocumentField('UserBankCard'), default=[])  # 银行卡信息
    pay_password = db.StringField(max_length=255)  # 支付密码hash值


class OrgRole(db.EmbeddedDocument):
    """机构和角色键值对"""
    org_code = db.StringField()
    role_code = db.ListField(db.StringField())
    is_stop = db.BooleanField(default=False)  # 是否停用
    department_id = db.ListField(db.StringField())  # 存储部门ID 表示当前用户所属部门列表


class AuthorizationRecord(db.EmbeddedDocument):
    resource_id = db.StringField()  # 授权资源id
    resource_name = db.StringField()  # 授权资源名名称
    start_date = db.DateTimeField()  # 授权开始时间
    finish_date = db.DateTimeField()  # 授权结束时间


class User(UserMixin, db.Document):
    """用户模型."""
    meta = {
        'collection': 'sys_user'
    }
    user_code = db.StringField()
    username = db.StringField(max_length=255, required=False)  # 用户名
    org_role = db.ListField(db.EmbeddedDocumentField('OrgRole'))  # 机构和角色键值对
    info = db.EmbeddedDocumentField('UserInfo')  # 用户详情信息
    account = db.EmbeddedDocumentField('UserAccount')  # 用户账户信息
    wallet = db.EmbeddedDocumentField('UserWallet')  # 用户钱包信息
    create_time = db.DateTimeField(default=dt.datetime.now)  # 创建时间
    create_by = db.StringField()  # 创建人
    update_time = db.DateTimeField()  # 更新时间
    update_by = db.StringField()  # 更新人
    status = db.IntField(choices=[dict_status_normal, dict_status_block_up, dict_status_delete],
                         default=dict_status_normal)  # 状态("0",正常，"1":停用 "2":删除)
    desc = db.StringField()  # 用户描述 对于用户的一些说明信息
    # 允许追踪 login activities 需要User有以下5个字段
    last_login_at = db.DateTimeField()  # 上次登录时间
    current_login_at = db.DateTimeField()  # 本次登录时间
    last_login_ip = db.StringField()  # 上次登录ip
    current_login_ip = db.StringField()  # 本次登录ip
    login_count = db.IntField()  # 登录次数
    authorization_record = db.ListField(db.EmbeddedDocumentField('AuthorizationRecord'))
    # 状态字典
    status_dict = {dict_status_normal: dict_normal, dict_status_block_up: dict_block_up,
                   dict_status_delete: dict_delete}
    bassnise_type = db.StringField()  # 业务类型
    company_info = db.StringField()  # 公司信息(合作伙伴id)
    
    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
    
    # 账号密码
    @property
    def password(self):
        return self.account.password
    
    @password.setter
    def password(self, password):
        self.account.password = hash_password(password)
        self.save()
    
    def check_password(self, password):
        return verify_password(password, self.account.password)
    
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
    
    @property
    def active(self):
        return self.account.active
    
    @property
    def org_codes(self):
        """所在机构 list"""
        return [org.org_code for org in self.org_role]
    
    @classmethod
    def get_auth_record_by_uesr_code(cls, user_code):
        '''
        根据user_code拿所有的已授权的资源列表
        :param user_code:
        :return:
        '''
        try:
            user = None
            user = cls.objects(user_code=user_code).first()
            return user.authorization_record
        except Exception as e:
            logging.error('%s %s' % (user, e))
    
    @classmethod
    def update_user_by_authorizationRecord(cls, user_code, info):
        """
        资源授权时间
        :param info: 
        :return: 
        """
        try:

            user = cls.objects(user_code=user_code).first()
            old_recode_list = user.authorization_record
            new_recode_list = []
            combine_dict_list = info.get('product_list')
            combine_id_list = [i['product_id'] for i in combine_dict_list]
            current_time = time.time()
            cache_combine_dict_list = []
            for j in old_recode_list:
                if j.resource_id in combine_id_list:
                    index = combine_id_list.index(j.resource_id)
                    eff_time = int(combine_dict_list[index]['eff_time'])
                    if eff_time == 0:
                        finish_date =None
                    else:
                        finish_date = dt.datetime.fromtimestamp(current_time + int(eff_time) * 24 * 3600)
                    j.finish_date = finish_date
                    cache_combine_dict_list.append(combine_dict_list[index])
            for i in cache_combine_dict_list:
                combine_dict_list.remove(i)
            for i in combine_dict_list:
                eff_time = int(i['eff_time'])
                if eff_time == 0:
                    finish_date = None
                else:
                    finish_date = dt.datetime.fromtimestamp(current_time + int(eff_time) * 24 * 3600)
                a = AuthorizationRecord(
                    resource_id=i.get('product_id'),
                    resource_name=i.get('product_name'),
                    start_date=dt.datetime.fromtimestamp(current_time),
                    finish_date=finish_date
                )
                new_recode_list.append(a)
            user.update_time = dt.datetime.now()
            user.update_by = session.get('org_code')
            new_recode_list.extend(old_recode_list)
            user.authorization_record = new_recode_list
            user.save()
            return True
        except Exception as e:
            logging.error(e)
            return False
    
    def create_tourist_info(self):
        """
        创建游客信息
        :return:
        """
        tourist_org_code = Sys_org.objects(org_name='游客机构').first().org_code
        tourist_role_code = Role.objects(org_code=tourist_org_code).first().role_code
        tourist = OrgRole(org_code=tourist_org_code, role_code=[tourist_role_code])
        return tourist
    
    def get_org_role_by_org_code(self, org_code):
        """
        通过机构编码获取org_role子集
        :param kwargs:
        :return:
        """
        try:
            for org_role in self.org_role:
                if org_role.org_code == org_code:
                    return org_role
        except Exception as e:
            raise e
    
    def update_org_role(self, session_org, new_org, new_roles):
        """
        更新(新增)用户机构和角色
        :param new_org: 机构编码
        :param new_roles: 角色编码列表
        :return:
        """
        try:
            if not isinstance(new_roles, list):
                new_roles = [new_roles]
            if new_org in self.org_codes:  # 机构不变，更新角色
                self.update_role_by_org(new_org, new_roles)
            else:  # 机构改变(或机构不存在用户org_role中)
                for org_role in self.org_role:
                    if org_role.org_code.startswith(session_org):  # 是否为当前机构的子机构
                        self.org_role.remove(org_role)  # 删除该机构和角色
                        break
                itm = OrgRole()  # 新建org_role
                itm.org_code = new_org
                itm.role_code = new_roles
                self.org_role.append(itm)
            self.save()
            return True
        except Exception as e:
            raise False
    
    def get_role_by_org(self, org_code):
        """
        通过机构编码查询角色编码
        :param org_code:
        :return:
        """
        logging.info('get_role_by_org')
        try:
            for org in self.org_role:
                if org.org_code == org_code and not org.is_stop:
                    return org.role_code
        except Exception as e:
            logging.debug(e)
            raise e
    
    def update_role_by_org(self, org_code, role_codes):
        """
        通过机构修改角色
        :param org_code:
        :param role_codes:  传值为list
        :return:
        """
        try:
            org_role = self.get_org_role_by_org_code(org_code)
            if not isinstance(role_codes, list):
                role_codes = [role_codes]
            org_role['role_code'] = role_codes
            self.save()
            return True
        except Exception as e:
            raise False
    
    def update_role_and_org(self, old_role_code, new_role_code, new_old_org):
        """
        角色移入其他机构后，更新机构和角色
        :param new_role:
        :param nwe_org:
        :param old_role:
        :param old_org:
        :return:
        """
        logging.info('update_role_and_org')
        try:
            for info in self.org_role:
                if old_role_code in info.role_code:
                    info.role_code.remove(str(old_role_code))
                    info.role_code.append(str(new_role_code))
                    info.org_code = new_old_org
                    break
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            raise False
    
    def delete_role_and_org(self, role_code):
        """
        角色删除后 用户绑定的角色删除
        :param role_code:
        :return:
        """
        logging.info("delete_role_and_org")
        try:
            for info in self.org_role:
                if role_code in info.role_code:
                    info.role_code.remove(str(role_code))
                    if not info.role_code:
                        self.org_role.remove(info)
                    # if not self.org_role:  # 赋予用户游客权限
                    #     tourist = self.create_tourist_info()
                    #     self.org_role.append(tourist)
                    break
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            raise False
    
    def update_org_by_role(self, org_code, role_code):
        """
        通过机构修改角色
        :param org_code:
        :param role_code:
        :return:
        """
        logging.info('update_role_by_org')
        try:
            for org in self.org_role:
                if org.role_code == role_code:
                    org.org_code = org_code
                    break
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            raise False
    
    def delete_org(self, org_code):
        """
        删除用户所在机构
        :param org_code:
        :return:
        """
        logging.info('delete_org')
        try:
            for org_role in self.org_role:
                if org_role.org_code == org_code:
                    self.org_role.remove(org_role)
                    break
            if not self.org_role:
                tourist = self.create_tourist_info()
                self.org_role.append(tourist)
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            return False

    def delete_user_by_code(self, user_code):
        """
        根据user_code删除用户
        :param user_code:
        :return:
        """
        logging.info('delete_user')
        try:
            if self.user_code == user_code:
                self.status = dict_status_delete
                self.save()
                return True
        except Exception as e:
            logging.debug(e)
            return False
    
    @classmethod
    def create(cls, **kwargs):
        """
        新建用户
        :param kwargs:
        :return:
        """
        try:
            
            username = kwargs.get('username', '')
            if kwargs.get('email'):
                email = kwargs.get('email').lower()
            else:
                email = ''
            
            account = UserAccount(email=email,
                                  mobile=kwargs.get('mobile', ''))
            
            if kwargs.get('other_auth'):
                account.set_other_auth(**kwargs.get('other_auth'))
            
            if kwargs.get('password'):
                account._password = kwargs.get('password')
            
            # info子集合
            if not kwargs.get('gender'):
                gender = 'N'
            else:
                gender = kwargs.get('gender')
            info = UserInfo(name=kwargs.get('name', username),
                            gender=gender,
                            birthday=kwargs.get('birthday'),
                            address=kwargs.get('address', ''),
                            avatar=kwargs.get('info_avatar', 'default.png'))
            
            # org_role 子集合
            org_role = []
            
            # 添加指定机构、权限
            if kwargs.get('org_code') and kwargs.get('role_code'):
                org_code = kwargs.get('org_code')
                role_code = kwargs.get('role_code')
                if not isinstance(role_code, list):
                    role_code = [role_code]
                org_role_data = OrgRole(org_code=org_code, role_code=role_code)
                if kwargs.get('is_stop') and isinstance(kwargs.get('is_stop'), bool):  # 如果值为True
                    org_role_data.is_stop = True
            else:
                # 初始化添加用户游客机构、游客权限
                tourist_org_code = Sys_org.objects(org_name='游客机构').first().org_code
                tourist_role_code = Role.objects(org_code=tourist_org_code).first().role_code
                org_role_data = OrgRole(org_code=tourist_org_code, role_code=[tourist_role_code])
            org_role.append(org_role_data)
            wallet = UserWallet()

            # 用户业务类型、
            bassnise_type = kwargs.get('bassnise_type')
            company_info = kwargs.get('company_info')

            user_code = session.get('user_code', "")
            
            user = cls(user_code=make_user_code(),
                       username=username,
                       account=account,
                       info=info,
                       org_role=org_role,
                       wallet=wallet,
                       update_time=dt.datetime.now(),
                       create_by=user_code,
                       update_by=user_code,
                       desc=kwargs.get('desc', ''),
                       bassnise_type=bassnise_type,
                       company_info=company_info)

            user.save()
            return user
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def oauth_sign(cls, **kwargs):
        """
        第三方登录
        :param kwargs:
        :return:
        """
        logging.info('oauth_sign')
        try:
            site = kwargs.get('site')
            uid = kwargs.get('uid')
            user = cls.objects(account__other_auth__site=site, account__other_auth__uid=uid).first()
            if user:
                return user
        except Exception as e:
            logging.debug(e)
            raise None
    
    @classmethod
    def create_by_oauth(cls, **kwargs):
        """
        通过第三方新建用户
        :return:
        """
        logging.info('create_by_oauth')
        try:
            site = kwargs.get('site')
            uid = kwargs.get('uid')
            uname = kwargs.get('uname')
            avatar = kwargs.get('avatar')
            token = kwargs.get('token')
            oauth = SocialOAuth(site=site, uid=uid, site_uname=uname, site_avatar=avatar, access_token=token)
            oauth_dict = {'01': 'wx', '02': 'QQ', '03': 'wb'}  # TODO
            first_name = oauth_dict.get('site')
            last_name = str(int(time.time()))
            username = first_name + last_name
            user = cls.create(username=username)
            user.account.oauth = oauth
            user.save()
            return user
        except Exception as e:
            logging.debug(e)
            raise None
    
    def update_oauth(self, **kw):
        """
        更新(创建)第三方登录信息
        :param info:
        :return:
        """
        logging.info('update_oauth')
        try:
            if not self.account.other_auth:
                oauth = SocialOAuth()
                self.account.other_auth = oauth
            self.account.other_auth.site = kw.get('site')
            self.account.other_auth.uid = kw.get('uid')
            self.account.other_auth.open_id = kw.get('open_id')
            self.account.other_auth.site_uname = kw.get('uname')
            self.account.other_auth.site_avatar = kw.get('avatar')
            self.account.other_auth.access_token = kw.get('access_token')
            self.account.other_auth.update_time = dt.datetime.now()
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            raise False
    
    @classmethod
    def get_by(cls, **kwargs):
        """
        使用用户名,邮件,code, 电话查询用户信息。
        :param kwargs:
        :return:
        """
        try:
            if kwargs.get('username'):
                user = cls.objects(username=kwargs.get('username'), status__ne=2).first()
                return user
            if kwargs.get('email'):
                user = cls.objects(account__email=kwargs.get('email'), status__ne=2).first()
                return user
            if kwargs.get('user_code'):
                user = cls.objects(user_code=kwargs.get('user_code')).first()
                return user
            if kwargs.get('mobile'):
                user = cls.objects(account__mobile=kwargs.get('mobile'), status__ne=2).first()
                return user
            if kwargs.get('open_id'):
                user = cls.objects(account__other_auth__open_id=kwargs.get('open_id')).first()
                return user
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def fuzzy_get_by(cls, username, email, mobile):
        """
        模糊匹配username or mobile or email查询用户
        :param data:
        :return:
        """
        try:
            search_list = []
            if username:
                search_list.append({'username': username})
            if mobile:
                search_list.append({'account.mobile': mobile})
            if email:
                search_list.append({'account.email': email})
            if search_list:
                search = {
                    '__raw__': {
                        'status': {'$in': [0, 1]},
                        '$or': search_list
                    }
                }
                users = cls.objects(**search).only('username', 'account.email', 'account.mobile').all()
            else:
                users = []
            return users
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def get_users_by_org_code(cls, org_code):
        try:
            search = {
                '__raw__': {
                    'status': {'$in': [0, 1]},
                    'org_role.org_code': org_code,
                }
            }
            users = cls.objects(**search).all()
            return users
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def get_users_by_role(cls, role_code, data='', page=1, per_page=20):
        """
         查询有同一角色的用户(分页)
        :param role_code:
        :param page: 当前页
        :param per_page: 请求数量
        :return:
        """
        logging.info('get_users_by_role')
        try:
            search = {
                '__raw__': {
                    'status': {'$in': [0, 1]},
                    'org_role.role_code': role_code,
                    '$or': [{'username': re.compile(data)},
                            {'account.mobile': re.compile(data)},
                            {'account.email': re.compile(data)}]
                }
            }
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            users = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            return users
        except Exception as e:
            logging.debug(e)
            raise e
    
    def get_coupon(self, coupon_code):
        """
        查询优惠券
        :param coupon_code:
        :return:
        """
        logging.info('get_coupon')
        try:
            coupon = self.wallet.objects(coupon_code=coupon_code).first()
            if coupon:
                return dict(get_time=coupon.get_time, get_by=coupon.get_by, use_time=coupon.use_time,
                            use_by=coupon.use_by)
            else:
                return None
        except Exception as e:
            logging.debug(e)
            raise None
    
    # 使用优惠券
    @classmethod
    def use_coupon(cls, user_code, record_id, order_id):
        try:
            user = cls.get_by(username=user_code)
            for coupon in user.wallet.coupons:
                if coupon.record_id == record_id:  # 判断优惠券是否被使用
                    if not coupon.use_time:
                        coupon.order_id = order_id
                        coupon.use_time = dt.datetime.now()
                        user.save()
                        return True
                    else:
                        return False
            return False
        except Exception as e:
            raise e
    
    def get_info(self, *args):
        """
        查询用户基础信息
        :param args: 信息键名
        :return:
        """
        logging.info('get_info')
        try:
            info = dict(name=self.info.name,
                        birthday=self.info.birthday,
                        gender=self.info.gender,
                        address=self.info.address,
                        avatar=self.info.avatar,
                        id_card=self.info.id_card
                        )
            if not args:
                return info
            ret = {}
            for key in args:
                itm = {key: info.get(key)}
                ret.update(itm)
            return ret
        except Exception as e:
            logging.debug(e)
            raise None
    
    def update_info(self, **kw):
        """
        更新(新增)用户基础信息
        :return:
        """
        logging.info('update_info')
        try:
            if not self.info:
                info = UserInfo()
                self.info = info
            if kw.get('name'):
                self.info.name = kw.get('name')
            if kw.get('birthday'):
                self.info.birthday = kw.get('birthday')
            if kw.get('gender'):
                self.info.gender = kw.get('gender')
            if kw.get('address'):
                self.info.address = kw.get('address')
            if kw.get('id_card'):
                self.info.id_card = kw.get('id_card')
            self.save()
        except Exception as e:
            logging.debug(e)
            raise e
    
    def to_dict(self):
        """
        返回用户非敏感信息
        :return:
        """
        logging.info('to_dict')
        try:
            data = self.to_json()
            data = json.loads(data)
            data.pop('_id')
            account = data.get('account')
            if account:
                account.pop('password')
            return data
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def get_info_by_org_role_code(cls, role_code):
        """
        根据机构id + 角色id 返回用户 org_role 信息
        :param org_code:
        :param role_code:
        :return:
        """
        logging.info("get_info_by_org_role_code")
        try:
            search = {
                '__raw__': {
                    'status': {'$in': [0, 1]},
                    'org_role.role_code': re.compile(r'^{}'.format(role_code)),
                }
            }
            users = cls.objects(**search).all()
            return users
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def get_user_by_org_and_data(cls, org_code, data):
        """
        通过机构和用户资料查询用户具体信息
        :param org_code:
        :param data:
        :return:
        """
        try:
            search = [
                {
                    '$lookup': {
                        'from': 'sys_org',
                        'localField': 'org_role.org_code',
                        'foreignField': 'org_code',
                        'as': 'sys_org'
                    }
                },
                {
                    '$lookup': {
                        'from': 'sys_role',
                        'localField': 'org_role.role_code',
                        'foreignField': 'role_code',
                        'as': 'sys_role'
                    }
                },
                {'$match': {
                    '$and': [
                        {'status': {'$in': [0, 1]}},
                        {'sys_org.org_code': re.compile(r'^{}'.format(org_code))}
                    ],
                    '$or': [{'username': data},
                            {'account.mobile': data},
                            {'account.email': data},
                            {'user_code': data}]
                }},
                
                {'$project': {'username': 1,
                              'user_code': 1,
                              'desc': 1,
                              'status': 1,
                              'account.email': 1,
                              'account.mobile': 1,
                              'wallet': 1,
                              'info': 1,
                              'org_role': 1,
                              'sys_org.org_code': 1,
                              'sys_org.org_name': 1,
                              'sys_role.name': 1,
                              'sys_role.role_code': 1,
                              'update_time': 1,
                              'last_login_time': 1,
                              'bassnise_type': 1,
                              'company_info': 1,
                              }}
            
            ]
            users = list(cls.objects.aggregate(*search))
            return users
        except Exception as e:
            raise e
    
    @classmethod
    def get_users_by_org(cls, org_code, data='', page=1, per_page=20, sort='create_time', sortOrder=-1):
        """
        查询有同一机构（及子机构）下的用户(分页)
        :param org_code:
        :param page: 当前页
        :param per_page: 请求数量
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            if data == '停用':
                search_match = {'org_role.is_stop': True}
            elif data == '正常':
                search_match = {'org_role.is_stop': False}
            else:
                search_match = {'$or': [{'username': re.compile(data)},
                                        {'account.mobile': re.compile(data)},
                                        {'account.email': re.compile(data)},
                                        {'info.name': re.compile(data)},
                                        {'sys_org.org_name': re.compile(data)},
                                        {'sys_role.name': re.compile(data)}]}
            match = {'status': {'$in': [0, 1]},
                     'sys_org.org_code': re.compile(r'^{}'.format(org_code)),
                     'sys_org.status': {'$in': [0, 1]}
                     }
            match.update(search_match)
            search = [
                {
                    '$lookup': {
                        'from': 'sys_org',
                        'localField': 'org_role.org_code',
                        'foreignField': 'org_code',
                        'as': 'sys_org'
                    }
                },
                {
                    '$lookup': {
                        'from': 'sys_role',
                        'localField': 'org_role.role_code',
                        'foreignField': 'role_code',
                        'as': 'sys_role'
                    }
                },
                {'$match': match},
                {'$sort': {sort: sortOrder}},
                {'$skip': skip_nums},
                {'$limit': int(per_page)},
                {'$project': {'username': 1,
                              'user_code': 1,
                              'desc': 1,
                              'status': 1,
                              'account.email': 1,
                              'account.mobile': 1,
                              'info': 1,
                              'org_role': 1,
                              'sys_org.org_code': 1,
                              'sys_org.org_name': 1,
                              'sys_role.name': 1,
                              'sys_role.role_code': 1,
                              'update_time': 1,
                              'last_login_time': 1
                              }}
            ]
            users = cls.objects.aggregate(*search)
            
            return list(users)
        except Exception as e:
            raise e
    
    @classmethod
    def get_org_users_count(cls, org_code, data=''):
        """
        获取当前机构下用户总数
        :return:
        """
        
        try:
            
            if data == '停用':
                search_match = {'org_role.is_stop': True}
            elif data == '正常':
                search_match = {'org_role.is_stop': False}
            else:
                search_match = {'$or': [{'username': re.compile(data)},
                                        {'account.mobile': re.compile(data)},
                                        {'account.email': re.compile(data)},
                                        {'info.name': re.compile(data)},
                                        {'sys_org.org_name': re.compile(data)},
                                        {'sys_role.name': re.compile(data)}]}
            match = {'status': {'$in': [0, 1]},
                     'sys_org.status': {'$in': [0, 1]},
                     'sys_org.org_code': re.compile(r'^{}'.format(org_code))}
            match.update(search_match)
            search = [
                {
                    '$lookup': {
                        'from': 'sys_org',
                        'localField': 'org_role.org_code',
                        'foreignField': 'org_code',
                        'as': 'sys_org'
                    }
                },
                {
                    '$lookup': {
                        'from': 'sys_role',
                        'localField': 'org_role.role_code',
                        'foreignField': 'role_code',
                        'as': 'sys_role'
                    }
                },
                {'$match': match},
                {'$group': {'_id': 0, 'count': {'$sum': 1}}}
            ]
            user_obj = cls.objects.aggregate(*search)
            info = list(user_obj)
            count = info[0].get('count') if info else 0
            return count
        except Exception as e:
            raise e
    
    @classmethod
    def get_user_list_by_current_org(cls, org_code):
        """
        查询当前机构下的用户信息(不包含子机构)
        :param org_code:
        :return:
        """
        try:
            current_org_user_list = cls.objects(org_role__org_code__in=[org_code], org_role__is_stop=False,
                                                status__nin=[cls.get_status("用户删除")]).all()
            return {"current_org_user_list": current_org_user_list, "total_count": len(current_org_user_list)}
        except Exception as e:
            raise e
    
    @classmethod
    def check_user_in_org(cls, user_code, org_code):
        """
        验证用户是否在当前机构
        :param user_code: 用户
        :param org_code: 机构
        :return:
        """
        try:
            user = User.objects(user_code=user_code, org_role__org_code=org_code).first()
            if user:
                return True
            else:
                return False
        except Exception as e:
            raise e
    
    @classmethod
    def get_select_users_by_org_id(cls, org_id, search_data='', page=1, per_page=12):
        """
        通过机构id获取用户信息(多数情况可以用于select2框)
        :param org_id:
        :param page:
        :param per_page:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            org = Sys_org.objects(org_id=org_id).first()
            org_code = org.org_code
            search = {
                '__raw__': {
                    'status': {'$in': [0, 1]},
                    'org_role.org_code': re.compile(r'^{}'.format(org_code)),
                    'username': re.compile(search_data),
                }
            }
            
            users = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            count = cls.objects(**search).count()
            user_list = []
            for user in users:
                info = {'user_code': user.user_code,
                        'username': user.username}
                user_list.append(info)
            return dict(user_list=user_list, count=count)
        except Exception as e:
            raise e
    
    @classmethod
    def get_user_dict_by_role_code(cls, role_code, page=1, per_page=12):
        """
        通过角色获取用户
        :param role_code:
        :param page:
        :param per_page:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            users = cls.objects(org_role__role_code__startswith=role_code, status__in=[0, 1]).skip(skip_nums).limit(
                int(per_page))
            data = []
            for user in users:
                info = {'user_code': user.user_code,
                        'username': user.username}
                data.append(info)
            return data
        except Exception as e:
            raise e
    
    def can(self, url_rule, user_roles):
        logging.info(url_rule)
        permission = Permissions.objects(url=url_rule).first()
        if not permission:
            return False
        
        permission_roles = permission.roles  # 可以访问该路由的角色list
        current_role_list = Role.objects(role_code__in=session.get("role_code"),
                                         role_status=0).all()
        result = set(permission_roles) & set(user_roles)  # 取交集，用于判断当前权限是否有当前用户的角色
        if permission.permission_type != 1 and current_role_list and result:
            return True
        elif permission.permission_type == 1:
            return True
        else:
            return False
    
    @classmethod
    def get_user_list_by_data(cls, page, per_page, search_data, department_id_list):
        """
        根据分页信息、查询条件、部门ID查询用户信息(同一部门下)
        :param page:
        :param per_page:
        :param search_data:
        :param department_id_list:
        :return:
        """
        start_index = (int(page) - 1) * int(per_page)
        search = {
            '__raw__': {
                'org_role.department_id': {'$in': department_id_list},
                'status': {'$nin': [int(cls.get_status("用户删除"))]},
                '$or': [
                    {'username': re.compile(search_data)},
                    {'info.name': re.compile(search_data)},
                    {'account.mobile': re.compile(search_data)},
                    {'account.email': re.compile(search_data)}
                ]
            }
        }
        return cls.objects(**search).skip(start_index).limit(int(per_page)).order_by("-create_time").all()
    
    @classmethod
    def get_department_user_total_count(cls, department_id_list, search_data):
        """
        获取部门员工记录总数
        :param department_id_list:
        :param search_data:
        :return:
        """
        search = {
            '__raw__': {
                'org_role.department_id': {'$in': department_id_list},
                'status': {'$nin': [int(cls.get_status("用户删除"))]},
                '$or': [
                    {'username': re.compile(search_data)},
                    {'info.name': re.compile(search_data)},
                    {'account.mobile': re.compile(search_data)},
                    {'account.email': re.compile(search_data)}
                ]
            }
        }
        return cls.objects(**search).count()
    
    @classmethod
    def get_user_list_all_by_data(cls, department_id_list):
        """
        根据部门ID查询用户信息(同一部门下)
        :param department_id_list:
        :return:
        """
        search = {
            '__raw__': {
                'org_role.department_id': {'$in': department_id_list},
                'status': {'$nin': [cls.get_status("用户删除")]}
            }
        }
        return cls.objects(**search).order_by("-create_time").all()
    
    @classmethod
    def get_user_list_by_user_code_list(cls, user_code_list):
        user_obj_list = cls.objects(user_code__in=user_code_list,
                                    status__in=[cls.get_status("正常"), cls.get_status("用户停用")]).all()
        return user_obj_list
    
    @classmethod
    def get_user_by_user_code(cls, user_code):
        """
        根据user_code查询当前用户
        :param user_code: 
        :return: 
        """
        return cls.objects(user_code=user_code, status__in=[cls.get_status("正常")]).first()
    
    @classmethod
    def get_user_info_by_user_code(cls, user_code):
        """
        根据用户编号获取用户具体信息
        :param user_code:
        :return:
        """
        return cls.objects(user_code=user_code, status__in=[cls.get_status("正常")]).first()
    
    @classmethod
    def update_current_department_user_by_data(cls, user_code_list, current_org_code, department_id, operation):
        """
        将当前用户添加进此部门或移出此部门
        :return:
        """
        if operation == "remove":
            # 根据用户编号以及机构编号获取本用户所处机构org_role信息字典，并将org_role中的department_id列表删除指定值
            # org_role.$.department_id 中的$表示当前 用户编号、机构编号符合要求的org_role列表索引
            cls.objects(user_code__in=user_code_list, org_role__org_code=current_org_code).update(
                __raw__={'$pull': {'org_role.$.department_id': department_id}})
        else:
            # 根据用户编号以及机构编号获取本用户所处机构org_role信息字典，并将org_role中的department_id列表添加指定值
            # org_role.$.department_id 中的$表示当前 用户编号、机构编号符合要求的org_role列表索引
            cls.objects(user_code__in=user_code_list, org_role__org_code=current_org_code).update(
                __raw__={'$push': {'org_role.$.department_id': department_id}})
    
    @staticmethod
    def get_status(dict_name):
        status_value = SysDict.get_dict_by_type_and_name(dict_type='sys_user_status', dict_name=dict_name)
        return status_value.dict_id
    
    @classmethod
    def get_users_by_org_id(cls, org_id, search_data='', page=1, per_page=12):
        """
        更具机构id获取用户
        :param org_id:
        :param search_data:
        :param page:
        :param per_page:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            org = Sys_org.objects(org_id=org_id).first()
            org_code = org.org_code
            search = [
                {
                    '$lookup': {
                        'from': 'sys_org',
                        'localField': 'org_role.org_code',
                        'foreignField': 'org_code',
                        'as': 'sys_org'
                    }
                },
                {'$unwind': "$sys_org"},
                {'$match': {
                    '$and': [
                        {'status': {'$in': [0, 1]}},
                        {'sys_org.org_code': re.compile(r'^{}'.format(org_code))}
                    ],
                    '$or': [{'username': re.compile(search_data)},
                            {'account.mobile': re.compile(search_data)},
                            {'account.email': re.compile(search_data)},
                            {'info.name': re.compile(search_data)},
                            {'sys_org.org_name': re.compile(search_data)},
                            ]
                }},
                {'$skip': skip_nums},
                {'$limit': int(per_page)},
                {'$project': {'username': 1,
                              'user_code': 1,
                              'account.email': 1,
                              'account.mobile': 1,
                              'sys_org.org_name': 1,
                              }}
            ]
            users = cls.objects.aggregate(*search)
            return list(users)
        except Exception as e:
            raise e
    
    @classmethod
    def get_user_by_code_list(cls, user_code_list):
        """
        根据用户编号列表 获取用户信息
        :param user_code_list:
        :return:
        """
        user_obj_list = cls.objects(user_code__in=user_code_list,
                                    status__in=[int(cls.get_status("正常")), int(cls.get_status("用户停用"))]).only(
            "user_code", "username").all()
        return user_obj_list
    
    @classmethod
    def get_select_users_by_org_code_list(cls, org_code_list, search_data='', page=1, per_page=12):
        """
        通过机构code列表获取用户信息(多数情况可以用于select2框)
        :param org_code_list:
        :param page:
        :param per_page:
        :return:
        by denghaolin
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            search = {
                '__raw__': {
                    'status': {'$in': [0, 1]},
                    'org_role.org_code': {'$in': org_code_list},
                    'username': re.compile(search_data),
                }
            }
            
            users = cls.objects(**search).skip(skip_nums).limit(int(per_page))
            count = cls.objects(**search).count()
            user_list = []
            for user in users:
                info = {'user_code': user.user_code,
                        'username': user.username}
                user_list.append(info)
            return dict(user_list=user_list, count=count)
        except Exception as e:
            raise e
    
    # 钱包操作
    def update_bank_card_info(self, bank_card_list):
        """
        更新银行卡信息
        :param bank_card_list:
        :return:
        """
        try:
            bank_cards = self.wallet.bank_cards
            bank_cards.clear()
            for card in bank_card_list:
                user_bank_card = UserBankCard(**card)
                bank_cards.append(user_bank_card)
            self.save()
            return True
        except Exception as e:
            logging.debug(e)
            return False
    
    @classmethod
    def change_user_balance(cls, change_type, change_money_count):
        """
        根据余额改变方式（recharge 充值 （消费...）） 改变金额大小, 用户编号对某用户钱包余额进行更新
        :param change_type:
        :param change_money_count:
        :return:
        """
        current_user_obj = User.get_user_info_by_user_code(current_user.user_code)
        old_user_balance = current_user_obj.wallet.balance
        if change_type == "recharge":
            current_user_obj.wallet.balance = old_user_balance + float(change_money_count)
            current_user_obj.save()
    
    @classmethod
    def change_user_point(cls, change_type, user_code, change_point_count, way):
        """
        根据积分改变方式（get 获取 post 消费）改变用户积分数目
        :param change_type:
        :param user_code:
        :param change_point_count:
        :param way:
        :return:
        """
        current_user_obj = User.get_user_info_by_user_code(user_code)
        old_user_point = current_user_obj.wallet.point
        if change_type == "get":
            current_user_obj.wallet.point = old_user_point + int(change_point_count)
            # 添加积分流水记录
            new_point_record = PointRecord(create_time=dt.datetime.now(), get=True, post=False,
                                           amount=change_point_count, org_code=session.get("org_code"),
                                           way=way, point_sum=old_user_point + int(change_point_count))
            current_user_obj.wallet.point_record.append(new_point_record)
            current_user_obj.save()
    
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
    def get_record_by_user_code(cls, user_code=None, start_time=None, end_time=None, page=1, per_page=20):
        """
        根据用户code获取记录对象
        :param user_code:
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
                        {'user_code': user_code},
                        {'wallet.point_record.create_time': {'$lte': start_time}},
                        {'wallet.point_record.create_time': {'$gte': end_time}},
                    ],
                }})
            else:
                search.append({'$match': {
                    '$and': [
                        {'user_code': user_code},
                    ],
                }})
            search.append({'$sort': {'wallet.point_record.create_time': -1}})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append(
                {'$project': {'wallet.point_record.create_time': 1,
                              'wallet.point_record.amount': 1,
                              'wallet.point_record.org_code': 1,
                              'wallet.point_record.way': 1,
                              'wallet.point_record.point_sum': 1,
                              'username': 1,
                              }})
            search.append({'$skip': skip_nums})
            search.append({'$limit': per_page})
            record_list = list(cls.objects.aggregate(*search))
            return record_list, count
        except Exception as e:
            logging.debug(e)
            raise e
    
    @classmethod
    def get_user_avatar_by_name(cls, user_name_list):
        """
        根据用户名获取用户头像
        :param user_name_list:
        :return:
        """
        result = {}
        all_user = cls.objects(username__in=user_name_list).all()
        for user in all_user:
            if user.info['avatar']:
                result[user.username] = user.info['avatar']
            else:
                result[user.username] = 'default.png'
        
        return result
    
    @classmethod
    def get_org_users(cls, org_code, data='', page=1, per_page=20):
        """
        查询有同一机构（及子机构）下的用户(分页)
        :param org_code:
        :param page: 当前页
        :param per_page: 请求数量
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            if data == '停用':
                search_match = {'org_role.is_stop': True}
            elif data == '正常':
                search_match = {'org_role.is_stop': False}
            else:
                search_match = {'$or': [{'username': re.compile(data)}]}
            match = {'status': {'$in': [0, 1]},
                     'sys_org.org_code': re.compile(r'^{}'.format(org_code)),
                     'sys_org.status': {'$in': [0, 1]}
                     }
            match.update(search_match)
            search = []
            search.append({
                '$lookup': {
                    'from': 'sys_org',
                    'localField': 'org_role.org_code',
                    'foreignField': 'org_code',
                    'as': 'sys_org'
                }
            })
            search.append({
                '$lookup': {
                    'from': 'sys_role',
                    'localField': 'org_role.role_code',
                    'foreignField': 'role_code',
                    'as': 'sys_role'
                }
            })
            search.append({'$match': match})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$sort': {'create_time': 1}})
            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})
            search.append({'$project': {'_id': 0,
                                        'username': 1,
                                        'user_code': 1,
                                        }})
            users = cls.objects.aggregate(*search)
            
            return list(users), count
        except Exception as e:
            raise e

    @classmethod
    def get_all_users_count(cls):
        """
        获取所有正常使用的用户总数
        :return:
        """
        return cls.objects().count()

    @classmethod
    def get_month_active_user(cls):
        """
        获得当前月活跃用户数量
        :return:
        """
        first_day = dt.datetime(year=dt.datetime.now().year, month=dt.datetime.now().month, day=1)
        return cls.objects(last_login_at__gt=first_day).count()

    @classmethod
    def get_month_add_user(cls):
        """
        获得当前月新增用户数量
        :return:
        """
        first_day = dt.datetime(year=dt.datetime.now().year, month=dt.datetime.now().month, day=1)
        return cls.objects(create_time__gt=first_day).count()

    @classmethod
    def get_30_days_new_user_list(cls):
        """
        获取前30天新增用户
        :return: 
        """
        try:
            current_time = dt.datetime.fromtimestamp(time.time())
            pre_30day_time = dt.datetime.fromtimestamp(time.time() - 2592000)
            search = [
                {'$match': {
                    'create_time': {
                        '$gt': pre_30day_time,
                        '$lt': current_time
                    }
                }},
                {"$group": {
                    '_id': {
                        'year': {'$year': '$create_time'},
                        'month': {'$month': '$create_time'},
                        'day': {'$dayOfMonth': '$create_time'},
                    },
                    'count': {'$sum': 1}
                }},
                {'$sort': {'_id': 1}}
            ]
            return list(cls.objects.aggregate(*search))
        except Exception as e:
            logging.error(e)

    @classmethod
    def get_12_month_new_user_list(cls):
        """
        获取前12月新增用户
        :return: 
        """
        try:
            current_time = dt.datetime.fromtimestamp(time.time())
            pre_11month_time = current_time - relativedelta(months=11)
            pre_11month_1_day_time = dt.datetime(pre_11month_time.year, pre_11month_time.month, 1)
            search = [
                {'$match': {
                    'create_time': {
                        '$gt': pre_11month_1_day_time,
                        '$lt': current_time
                    }
                }},
                {"$group": {
                    '_id': {
                        'year': {'$year': '$create_time'},
                        'month': {'$month': '$create_time'},
                    },
                    'count': {'$sum': 1}
                }},
                {'$sort': {'_id': 1}}
            ]
            return list(cls.objects.aggregate(*search))
        except Exception as e:
            logging.error(e)

    @classmethod
    def get_all_year_new_user_list(cls):
        """
        获取所有年份新增用户数量
        :return: 
        """
        try:
            search = [
                {"$group": {
                    '_id': {
                        'year': {'$year': '$create_time'},
                    },
                    'count': {'$sum': 1}
                }},
                {'$sort': {'_id': 1}}
            ]
            return list(cls.objects.aggregate(*search))
        except Exception as e:
            logging.error(e)

    def is_status_normal(self):
        """
        判断用户状态是否正常
        :return:
        """
        if int(self.status) == dict_status_normal:
            return True
        else:
            return False
