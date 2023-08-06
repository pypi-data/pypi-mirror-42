#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/14 13:50
# @Author  : chenwanyue
# @Site    : www.rich-f.com
# @File    : models.py
# @Software: Rich Web Platform
# @Function: 权限管理数据模型

import re
import datetime as dt

import logging

from rich_base_provider import db
from flask_security import current_user
from rich_base_provider import response
from rich_base_provider.sysadmin.sys_dict.models import SysDict

permission_status_normal = 0
permission_status_block_up = 1
permission_status_delete = 2

permission_normal = "正常"
permission_block_up = "停用"
permission_delete = "删除"

permission_type_limit = 0
permission_type_default = 1
permission_type_menu = 2
permission_type_menu_default = 3
permission_type_protal_default = 4

permission_limit = "限制操作权限"
permission_default = "默认操作权限"
permission_menu = "限制菜单权限"
permission_menu_default = "默认菜单权限"
permission_protal_default = '默认门户权限'


class Permissions(db.Document):
    """权限表"""

    meta = {
        'collection': 'sys_permissions'
    }

    permission_id = db.StringField()  # 权限id
    permission_name = db.StringField()  # 权限名
    url = db.StringField()  # url地址
    icon = db.StringField()  # 图标
    permission_type = db.IntField(
        choices=[permission_type_limit, permission_type_default,
                 permission_type_menu, permission_type_menu_default,
                 permission_type_protal_default])  # 权限类型, 0：限制操作权限 1：默认操作权限  2:限制菜单权限 3:默认菜单权限，4:默认门户权限
    sort = db.IntField(default=0)  # 同级排序
    parent_id = db.StringField()  # 父类id
    desc = db.StringField()  # 权限描述
    status = db.IntField(choices=[permission_status_normal, permission_status_block_up, permission_status_delete],
                         default=permission_status_normal)  # 权限状态("0",正常，"1":停用 "2":删除)
    create_by = db.StringField()  # 创建人
    update_by = db.StringField()  # 修改人
    create_time = db.DateTimeField(default=dt.datetime.utcnow)  # 创建时间
    update_time = db.DateTimeField()  # 修改时间
    roles = db.ListField(db.StringField(), default=[])  # 名权限对应的角色（存储角色编号 角色编号唯一）
    # roles = db.ListField(db.ReferenceField(Role), default=[])  # 名权限对应的角色（存储角色对象）

    # 权限类型字典表
    permission_type_dict = {permission_type_limit: permission_limit, permission_type_default: permission_default,
                            permission_type_menu: permission_menu,
                            permission_type_menu_default: permission_menu_default,
                            permission_type_protal_default: permission_protal_default}
    # 权限状态字典表
    status_dict = {permission_status_normal: permission_normal, permission_status_block_up: permission_block_up,
                   permission_status_delete: permission_delete}

    @classmethod
    def find_perm_list(cls, role_code_list, page=1, per_page=20, search_data="", sort='create_time', sortOrder=-1):

        """
        根据角色对象此角色拥有的权限
        :param role_code_list
        :param page
        :param per_page
        :param search_data
        :return:
        """
        # 根据角色信息获取本角色在此机构所有操作权限 包括默认权限
        start_index = (int(page) - 1) * int(per_page)  # 起始索引

        search = {
            '__raw__': {
                'status': {'$in': [permission_status_normal, permission_status_block_up]},
                # 'roles': {'$in': role_code_list}
            }
        }

        search_status_list = [k for k, v in cls.status_dict.items() if v == search_data and v is not permission_delete]
        search_type_list = [k for k, v in cls.permission_type_dict.items() if v == search_data]
        if search_status_list:
            search['__raw__']['status'] = {'$in': search_status_list}
            search_list = [
                {'permission_type': {'$in': [permission_type_limit, permission_type_menu]},
                 'roles': {'$in': role_code_list}},
                {'permission_type': {
                    '$in': [permission_type_default, permission_type_menu_default, permission_type_protal_default]}}
            ]
            search['__raw__']['$or'] = search_list
        elif search_type_list:
            search['__raw__']['permission_type'] = {'$in': search_type_list}
            # search['__raw__']['roles'] = {'$in': role_code_list}
        else:
            search_list = [

                {'permission_type': {'$in': [permission_type_limit, permission_type_menu]},
                 'roles': {'$in': role_code_list},
                 '$or': [{'permission_name': re.compile(r'{}'.format(search_data))},
                         {'url': re.compile(r'{}'.format(search_data))},
                         {'desc': re.compile(r'{}'.format(search_data))}]
                 },

                {'permission_type': {
                    '$in': [permission_type_default, permission_type_menu_default, permission_type_protal_default]},
                 '$or': [{'permission_name': re.compile(r'{}'.format(search_data))},
                         {'url': re.compile(r'{}'.format(search_data))},
                         {'desc': re.compile(r'{}'.format(search_data))}]
                 }
            ]

            search['__raw__']['$or'] = search_list
        data_list = cls.objects(**search).skip(start_index).limit(int(per_page)).order_by(sortOrder + sort).all()
        data_count = cls.objects(**search).count()
        return data_list, data_count

    @classmethod
    def get_perm_total_count(cls):
        """
        获取权限管理记录总数
        :return:
        """
        search = {
            '__raw__': {
                'status': {'$in': [permission_status_normal, permission_status_block_up]},
            }
        }
        return cls.objects(**search).count()

    @classmethod
    def get_un_default_perm_list(cls, role_code_list):
        """
        获取所有本角色可分配的非默认权限
        :param role_code_list:
        :return:
        """
        un_default_permission = cls.objects(roles__in=role_code_list,
                                            status__in=[permission_status_normal, permission_status_block_up],
                                            permission_type__in=[permission_type_limit, permission_type_menu,
                                                                 permission_type_menu_default]).only(
            "permission_id", "permission_name", "url",
            "permission_type", "parent_id",
            "desc").order_by("+permission_id").all()
        return un_default_permission

    @classmethod
    def get_perm_id_new(cls, parent_id):
        """
        获取本层级最新权限编号
        :param parent_id:
        :return:
        """
        # 根据父ID获取所有指定权限的ID(只获取permission_id字段) 根据排序获取最新的perm_id 已删除权限权限编号不复用
        new_perm = cls.objects(parent_id=parent_id).only("permission_id").order_by(
            "-permission_id").first()
        if new_perm:
            return new_perm.permission_id
        else:
            return "0"

    @classmethod
    def get_perm_info(cls, permission_id):
        """
        根据权限编号获取本权限具体信息
        :param permission_id:
        :return:
        """
        perm_info = cls.objects(permission_id=permission_id,
                                status__in=[permission_status_normal, permission_status_block_up]).first()
        return perm_info

    @classmethod
    def delete_perm(cls, permission_id, update_time):
        """
        删除权限
        :param permission_id
        :param update_time
        :return:
        """
        # 根据权限编号获取本权限具体信息
        perm_obj = cls.get_perm_info(permission_id)
        if not perm_obj:
            # 本权限不存在
            return response.ERROR
        else:
            user = current_user.user_code
            perm_obj.update(status=permission_status_delete, update_time=update_time, update_by=user)

    @classmethod
    def get_child_perm(cls, login_user_role_code, parent_id):
        """
        根据当前登录用户角色编号以及权限父ID查询本角色所有权限父ID的此的权限信息
        :param login_user_role_code:
        :param parent_id:
        :return:
        """
        perm_child_list = cls.objects(roles__in=login_user_role_code, parent_id=parent_id,
                                      status__in=[permission_status_normal, permission_status_block_up],
                                      permission_type__in=[permission_type_limit, permission_type_menu,
                                                           permission_type_menu_default]
                                      ).order_by(
            "+permission_id").all()
        return perm_child_list

    @classmethod
    def get_child_perm_id(cls, parent_id):
        perm_child_list = cls.objects(parent_id=parent_id,
                                      status__in=[permission_status_normal, permission_status_block_up]).only(
            "permission_id").all()
        return perm_child_list

    @classmethod
    def insert_perm(cls, create_dict):
        """
        创建新权限
        :param create_dict:
        :return:
        """
        """
            权限一开始创建
                默认权限 所有角色都拥有 roles保存[]列表 
                非默认权限 只有顶级admin拥有此权限 后续顶级admin可以将此权限进行分配
        """
        user = current_user.user_code
        if int(create_dict["permission_type"]) != permission_type_default or int(
                create_dict["permission_type"]) != permission_type_menu_default:
            # 限制权限 菜单权限
            # 获取顶级机构的顶级admin角色（默认设定顶级机构机构编号为0001，admin角色编号为0001-0001）
            # 获取系统首位机构编号（根据dict_type + dict_id 唯一获取）
            org_dict = SysDict.get_dict_info_by_type_and_id("org_code", "1")
            org_dict_data = org_dict.description
            # 获取系统首位角色编号（根据dict_type + dict_id 唯一获取）
            role_dict = SysDict.get_dict_info_by_type_and_id("role_code", "1")
            role_dict_data = role_dict.description
            # 角色编号构成（机构编号-角色编号）
            role_code = org_dict_data + "-" + role_dict_data
            create_dict["roles"].append(role_code)
        # 添加权限对象
        perm = Permissions(permission_id=create_dict["permission_id"],
                           permission_name=create_dict["permission_name"],
                           url=create_dict["url"], permission_type=int(create_dict["permission_type"]),
                           parent_id=create_dict["parent_id"], desc=create_dict["desc"],
                           status=int(create_dict["status"]), icon=create_dict["icon"], sort=create_dict["sort"],
                           create_by=user, update_by=user, create_time=dt.datetime.now(),
                           update_time=dt.datetime.now(), roles=create_dict["roles"])
        perm.save()

    @classmethod
    def update_perm(cls, update_dict):
        """
        更新权限基本信息
        :param update_dict:
        :return:
        """
        # 更新权限对象
        old_perm = Permissions.objects(permission_id=update_dict["permission_id"]).first()
        if old_perm.permission_name != update_dict["permission_name"]:
            old_perm.permission_name = update_dict["permission_name"]
        if old_perm.url != update_dict["url"]:
            old_perm.url = update_dict["url"]
        if str(old_perm.permission_type) != str(update_dict["permission_type"]):
            # 如果将权限类型修改为默认权限 则将此权限的roles列表清空
            if int(update_dict["permission_type"]) == permission_type_default:
                # 将此权限的角色编号列表清空
                old_perm.roles = []
            else:
                # 判断本权限之前的权限类型 为默认权限（roles只添加admin角色）非默认权限（保留roles的值）
                if old_perm.permission_type == permission_type_default:
                    # 默认权限 只添加admin
                    # 获取系统首位机构编号（根据dict_type + dict_id 唯一获取）
                    org_dict = SysDict.get_dict_info_by_type_and_id("org_code", "1")
                    org_dict_data = org_dict.description
                    # 获取系统首位角色编号（根据dict_type + dict_id 唯一获取）
                    role_dict = SysDict.get_dict_info_by_type_and_id("role_code", "1")
                    role_dict_data = role_dict.description
                    old_perm.roles = [org_dict_data + "-" + role_dict_data]
            old_perm.permission_type = int(update_dict["permission_type"])
        if old_perm.desc != update_dict["desc"]:
            old_perm.desc = update_dict["desc"]
        if str(old_perm.status) != str(update_dict["status"]):
            old_perm.status = int(update_dict["status"])
        if old_perm.icon != update_dict["icon"]:
            old_perm.icon = update_dict["icon"]
        if str(old_perm.sort) != str(update_dict["sort"]):
            old_perm.sort = int(update_dict["sort"])
        if old_perm.parent_id != update_dict["parent_id"]:
            # 判断用户是否想把父权限ID设置为自身ID
            if old_perm.permission_id != update_dict["parent_id"]:
                old_perm.parent_id = update_dict["parent_id"]
        old_perm.update_time = dt.datetime.now()
        old_perm.update_by = current_user.user_code
        old_perm.save()
        return response.SUCCESS

    @classmethod
    def get_perm_sub_info(cls, url, permission_name):
        """
        根据权限路径、权限名称获取权限信息
        :param url:
        :param permission_name:
        :return:
        """
        search = {
            '__raw__': {
                'status': {'$in': [permission_status_normal, permission_status_block_up]},
                '$or': [
                    {'permission_name': permission_name},
                    {'url': url}
                ]
            }
        }
        return cls.objects(**search).first()

    @classmethod
    def allot_perm_to_roles(cls, permission_id, role_code_list, update_time):
        """
        将指定权限分配给指定角色
        :param permission_id:
        :param role_code_list:
        :param update_time
        :return:
        """
        # 获取本权限对象
        perm_obj = cls.objects(permission_id=permission_id,
                               status__in=[permission_status_normal, permission_status_block_up]).first()
        if not perm_obj:
            return response.ERROR
        else:
            for role_code in role_code_list:
                perm_obj.roles.append(role_code)
            perm_obj.update_time = update_time
            perm_obj.update_by = current_user.user_code
        perm_obj.save()

    @classmethod
    def delete_permission_roles(cls, role_code):
        """
        将此角色从原先的权限引用中删除
        :param role_code:
        :return:
        """
        # 获取含有本角色编号的所有权限对象
        perm_obj_list = Permissions.objects(roles__in=[role_code],
                                            status__in=[permission_status_normal, permission_status_block_up]).all()
        for perm_obj in perm_obj_list:
            perm_obj.roles.remove(str(role_code))
            perm_obj.update_time = dt.datetime.now()
            perm_obj.update_by = current_user.user_code
            perm_obj.save()

    @classmethod
    def get_permissions_by_role_code(cls, role_code):
        """
        根据角色类型获取菜单权限
        :param role_code:
        :return:
        """
        permission_list = Permissions.objects(roles__in=role_code,
                                              status__in=[permission_status_normal]).only(
            "permission_id",
            "permission_name",
            "url", "icon", "sort",
            "parent_id",
            "permission_type",
            "desc").order_by(
            'sort').all()
        return permission_list

    @classmethod
    def get_menu_permissions_by_role_code(cls, role_code):
        """
        根据角色类型获取菜单权限
        :param role_code:
        :return:
        """

        search = {
            '__raw__': {
                'status': {'$in': [permission_status_normal]},
                '$or': [
                    {'roles': {'$in': role_code}, 'permission_type': permission_type_menu},
                    {'permission_type': permission_type_menu_default}
                ]
            }
        }

        permission_list = Permissions.objects(**search).only(
            "permission_id",
            "permission_name",
            "url", "icon", "sort",
            "parent_id",
            "permission_type",
            "desc").order_by(
            'sort').all()
        return permission_list

    @classmethod
    def update_permission_roles_info(cls, old_role_code, new_role_code):
        """
        角色id更改是 同步权限表中角色id信息
        :param old_role_code:
        :param new_role_code:
        :return:
        """
        permission_obj_list = Permissions.objects(roles__in=[old_role_code], status__in=[0, 1, 2]).only('roles').all()
        for roles_obj in permission_obj_list:
            for role_code in roles_obj.roles:
                if role_code == old_role_code:
                    roles_obj.roles.remove(old_role_code)
                    roles_obj.roles.append(new_role_code)
                    roles_obj.update_time = dt.datetime.now()
                    roles_obj.update_by = current_user.user_code
                    roles_obj.save()

    @classmethod
    def get_perm_sub_info_by_name(cls, login_user_role_code, parent_perm_name_list):
        """
        根据当前登录用户角色编号以及权限名称获取权限ID 以及其他信息
        :param login_user_role_code
        :param parent_perm_name_list
        :return:
        """
        permission_obj_list = cls.objects(roles__in=login_user_role_code,
                                          status__in=[permission_status_normal, permission_status_block_up],
                                          permission_name__in=parent_perm_name_list).only("permission_id",
                                                                                          "permission_name",
                                                                                          "parent_id").all()
        return permission_obj_list

    @classmethod
    def ger_permissions_by_role_code(cls, role_code):
        """
        根据角色id 获取全部权限信息
        :param role_code:
        :return:
        """
        permission_obj_list = cls.objects(roles__in=[role_code]).only("permission_id", "permission_name").all()
        return permission_obj_list

    @classmethod
    def get_permission_by_url(cls, url):
        """
        根据URL获取权限
        :param url:
        :return:
        """
        return cls.objects(url=url).first()

    @classmethod
    def get_permissions_all(cls):
        """
        获取全部非默认权限
        :return:
        """
        permission_obj_all_list = cls.objects(
            permission_type__in=[permission_type_limit, permission_type_menu, permission_type_menu_default],
            status__in=[permission_status_normal]).only(
            "permission_id", "permission_name", 'parent_id').order_by("+sort").all()
        return permission_obj_all_list

    @classmethod
    def delete_role_by_permission_id(cls, permission_list, role_code, update_by):
        """
        根据权限列表 删除指定角色
        :param permission_list:
        :param role_code:
        :return:
        """
        permission_obj_list = cls.objects(permission_id__in=permission_list,
                                          permission_type__in=[permission_type_limit, permission_type_menu,
                                                               permission_type_menu_default]).all()

        for perm_obj in permission_obj_list:
            perm_obj.roles.remove(str(role_code))
            perm_obj.update_by = update_by
            perm_obj.update_time = dt.datetime.now()
            perm_obj.save()

    @classmethod
    def add_role_by_permission_id(cls, permission_list, role_code, update_by):
        """
        根据权限列表 添加指定角色
        :param permission_list:
        :param role_code:
        :param update_by:
        :return:
        """
        permission_obj_list = cls.objects(permission_id__in=permission_list,
                                          permission_type__in=[permission_type_limit, permission_type_menu,
                                                               permission_type_menu_default]).all()

        for perm_obj in permission_obj_list:
            perm_obj.roles.append(str(role_code))
            perm_obj.update_by = update_by
            perm_obj.update_time = dt.datetime.now()
            perm_obj.save()

    @classmethod
    def get_permissions_by_role(cls, role_code):
        """
        获取角色非默认权限
        :param role_code:
        :return:
        """
        permission_list = Permissions.objects(roles__in=[role_code],
                                              permission_type__in=[permission_type_menu, permission_type_limit,
                                                                   permission_type_menu_default],
                                              status__in=[permission_status_normal]).only(
            "permission_id",
            "permission_name",
            'parent_id').order_by("+sort").all()
        return permission_list

    @classmethod
    def get_permission_type_protal_default_list(cls):
        return cls.objects(permission_type__in=[permission_type_protal_default],
                           status__in=[permission_status_normal]).order_by("+sort").all()

    @classmethod
    def get_child_permission_by_code(cls, role_code, parent_id, url):
        """
        根据权限编码获取相关子菜单
        :return:
        """
        try:
            search = {
                '__raw__': {
                    'status': {'$in': [permission_status_normal]},
                    'parent_id': parent_id,
                    'url': {'$ne': url},
                    '$or': [
                        {'permission_type': permission_type_menu_default},
                        {'roles': {'$in': role_code}, 'permission_type': permission_type_menu},
                    ]
                }
            }
            return Permissions.objects(**search).order_by("+sort").all()

        except Exception as e:
            logging.debug(e)
            return None

    @classmethod
    def get_first_menu_permissions_by_role_code(cls, role_code):
        """
        根据角色类型获取菜单权限
        :param role_code:
        :return:
        """

        search = {
            '__raw__': {
                'status': {'$in': [permission_status_normal]},
                'permission_id': {'$regex': '^\d{0,6}$'},
                'permission_type': 2,
                'roles': {'$in': role_code},
            }
        }

        permission_list = Permissions.objects(**search).only(
            "permission_id",
            "permission_name",
            "url", "icon", "sort",
            "parent_id",
            "permission_type",
            "desc").order_by(
            'sort').all()
        return permission_list
