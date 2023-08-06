#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 17:24
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : models.py

import datetime, logging, re, time, json
from flask import session
from flask_security import current_user

from rich_base_provider import db
from rich_base_provider.sysadmin.sys_dict.models import SysDict
from rich_base_provider.sysadmin.sys_user.models import User


class Task(db.Document):
    """
    待办表
    """
    meta = {
        'collection': 'task'
    }
    task_id = db.StringField(unique=True, required=False)  # 任务唯一id
    task_code = db.StringField()  # 任务层级
    title = db.StringField()  # 任务主题
    remark = db.StringField()  # 任务备注

    task_type = db.StringField()  # 任务类型
    order_list = db.ListField(default=[])  # 订单号
    is_critical = db.StringField()  # 是否紧急("0",不紧急，"1":紧急)
    limit_time = db.DateTimeField()  # 期限

    source = db.StringField()  # 任务发起人         保存user_code
    worker = db.StringField()  # 指派人             保存user_code
    create_time = db.DateTimeField()  # 任务创建时间
    create_by = db.StringField()  # 创建人
    update_time = db.DateTimeField()  # 任务完成时间
    update_by = db.StringField()  # 更新人
    status = db.StringField()  # 任务状态("0",未完成，"1":已完成,"2":取消)

    @staticmethod
    def create_task_id():
        base_str = str(time.time()).replace('.', '')[:13]
        return '{}{:0<13}'.format('T', base_str)

    @staticmethod
    def get_status(dict_name):
        """
        获取状态
        :param dict_name:
        :return:
        """
        data = SysDict.get_dict_by_type_and_name(dict_type='task_status', dict_name=dict_name)
        return data

    @classmethod
    def create_task_code(cls, task_id):
        """
        创建待办层级      task_id-0001
        :param task_id:
        :return:
        """
        try:
            search = [{'$match': {
                'task_code': re.compile(r"^" + task_id)
            }},
                {'$project': {'task_code': 1,
                              'task_id': 1}}
            ]
            task_levels = list(cls.objects.aggregate(*search))
            task_level = len(task_levels)
            logging.info(task_level)
            task_code = task_id + '-' + task_level * '0001' + '0001'
            return task_code
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def create_task(cls, params):
        """
        新建待办
        :param params:
        :return:
        """
        try:
            limit_time = datetime.datetime.strptime(params.get("limit_time"), '%Y-%m-%d %H:%M:%S')  # 格式化日期
            task_id = cls.create_task_id()
            task_obj = Task(task_id=task_id,
                            task_code=cls.create_task_code(task_id),
                            title=params.get('title'),
                            remark=params.get('remark', ''),
                            source=current_user.user_code,
                            worker=params.get('worker'),

                            task_type=params.get('task_type', '1'),
                            order_list=params.get('order_id_list', []),
                            is_critical=params.get('is_critical'),
                            limit_time=limit_time,

                            create_time=datetime.datetime.now(),
                            create_by=current_user.user_code,
                            status=params.get('status', cls.get_status('未完成').dict_id)
                            )
            task_obj.save()
            req_dict = dict(
                task_id=task_obj.task_id, task_code=task_obj.task_code, title=task_obj.title,
                remark=task_obj.remark, source=User.get_user_info_by_user_code(task_obj.source).username,
                worker_name=User.get_user_info_by_user_code(task_obj.worker).username, worker=task_obj.worker,
                task_type=task_obj.task_type, order_list=task_obj.order_list, is_critical=task_obj.is_critical,
                limit_time=str(task_obj.limit_time), create_time=str(task_obj.create_time),
                create_by=task_obj.create_by, status=task_obj.status)
            # return req_dict
            return json.dumps(req_dict)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def update_task(cls, params):
        """
        更新待办
        :param params:
        :return:
        """
        try:
            limit_time = datetime.datetime.strptime(params.get("limit_time"), '%Y-%m-%d %H:%M:%S')  # 格式化日期
            cls.objects(task_id=params.get('task_id')).update_one(
                set__title=params.get('title'),
                # set__content='',
                set__remark=params.get('remark'),
                set__source=current_user.user_code,
                set__worker=params.get('worker'),

                set__task_type=params.get('task_type'),
                set__order_list=params.get('order_id_list'),
                set__is_critical=params.get('is_critical'),
                set__limit_time=limit_time,

                set__status=params.get('status', cls.get_status('未完成').dict_id),
                update_by=current_user.user_code,
                update_time=datetime.datetime.now()
            )
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def deal_task(cls, params):
        """
        待办已处理
        :param params:
        :return:
        """
        try:
            cls.objects(task_id=params.get('task_id')).update_one(
                set__status=cls.get_status('已完成').dict_id,
                update_by=current_user.user_code,
                update_time=datetime.datetime.now()
            )
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_task_info(cls, worker_code, search_data='', page=1, per_page=12, status_name='未完成'):
        """
        获取未完成待办列表
        :param worker_code: 指派人user_code
        :param search_data:
        :param page:
        :param per_page:
        :return:
        """
        try:
            status = cls.get_status(status_name).dict_id
            skip_nums = (int(page) - 1) * int(per_page)
            search = []
            search.append({
                '$lookup': {'from': 'sys_user',
                            'localField': 'source',
                            'foreignField': 'user_code',
                            'as': 'source_user'}}, )
            search.append({
                '$lookup': {'from': 'sys_user',
                            'localField': 'worker',
                            'foreignField': 'user_code',
                            'as': 'worker_user'}}, )
            search.append({'$match': {'$and': [
                {'status': {'$in': [status]}},
                {'worker': {'$in': [worker_code]}},
            ],
                '$or': [{'title': re.compile(search_data)},
                        {'remark': re.compile(search_data)},
                        {'source_user.username': re.compile(search_data)},
                        {'worker_user.username': re.compile(search_data)},
                        ]
            }})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$sort': {'create_time': -1}})
            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})
            search.append({'$project': {'_id': 0,
                                        'task_id': 1,
                                        'task_code': 1,
                                        'title': 1,
                                        'remark': 1,
                                        'source': 1,
                                        'source_user.username': 1,
                                        'worker': 1,
                                        'worker_user.username': 1,
                                        'create_time': 1,
                                        'status': 1,
                                        'limit_time': 1,
                                        'update_time': 1
                                        }})
            res_list = list(cls.objects.aggregate(*search))
            return res_list, count
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_task_detail_by_id(cls, task_id):
        """
        获取待办对象
        :param task_id:
        :return:
        """
        try:
            task_obj = cls.objects(task_id=task_id).first()
            if task_obj:
                return task_obj
            return None
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_task_detail_by_code(cls, task_code):
        """
        根据task_code获取顶级待办对象
        :param task_code:
        :return:
        """
        try:
            task_id = task_code.split('-')[0]
            task_obj = cls.objects(task_id=task_id).first()
            if task_obj:
                return task_obj
            return None
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_task_by_source(cls, source_code, search_data='', page=1, per_page=12):
        """
        根据发起者获取发起者创建的待办列表
        :param source_code:
        :param search_data:
        :param page:
        :param per_page:
        :return:
        """
        try:
            status = cls.get_status('取消').dict_id
            skip_nums = (int(page) - 1) * int(per_page)
            search = []
            search.append({'$lookup': {'from': 'sys_user',
                                       'localField': 'worker',
                                       'foreignField': 'user_code',
                                       'as': 'worker_user'}})
            search.append({'$lookup': {'from': 'sys_user',
                                       'localField': 'source',
                                       'foreignField': 'user_code',
                                       'as': 'source_user'}})
            search.append({'$lookup': {'from': 'sys_dict',
                                       'localField': 'status',
                                       'foreignField': 'dict_name',
                                       'as': 'status_dict'}})
            search.append({'$match': {'$and': [{'source': source_code},
                                               {'status': {'$nin': [status]}}
                                               ],
                                      '$or': [
                                          {'title': re.compile(search_data)},
                                          {'remark': re.compile(search_data)},
                                          {'worker_user.username': re.compile(search_data)},
                                          {'source_user.username': re.compile(search_data)},
                                      ]}})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            count = list(cls.objects.aggregate(*search))[0]["count"] if list(cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$sort': {'create_time': -1}})
            search.append({'$skip': skip_nums})
            search.append({'$limit': int(per_page)})
            search.append({'$project': {
                'task_id': 1,
                'title': 1,
                'remark': 1,
                'source': 1,
                'source_user.username': 1,
                'worker': 1,
                'worker_user.username': 1,
                'create_time': 1,
                'status': 1,
                'limit_time': 1,
            }})
            res_list = list(cls.objects.aggregate(*search))
            return res_list, count
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def update_sponsor_task(cls, task_id, status='取消'):
        """
        取消我创建的待办
        :param task_id:
        :return:
        """
        try:
            cls.objects(task_id=task_id).update_one(
                set__status=cls.get_status(status).dict_id,
                update_by=current_user.user_code,
                update_time=datetime.datetime.now()
            )
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_task_count(cls):
        """
        获取当前登录用户的待办条数
        :return:
        """
        try:
            user_code = session.get('user_code')
            status = cls.get_status('未完成').dict_id
            task_count = cls.objects(worker=user_code, status=status).all().only('task_id').count()
            if task_count > 0:
                return task_count
            else:
                return None
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def create_level_task(cls, params):
        """
        新建待办
        :param params:
        :return:
        """
        try:
            new_limit_time = datetime.datetime.strptime(params.get("new_limit_time"), '%Y-%m-%d %H:%M:%S')  # 格式化日期
            # old_task_id = params.get('old_task_code').split('-')[0]
            old_task_id = params.get('old_task_id')
            task_id = cls.create_task_id()
            task_obj = Task(task_id=task_id,
                            task_code=cls.create_task_code(old_task_id),  # 根据顶级指派的待办获取该待办层级code
                            title=params.get('title'),  # 顶级待办的待办主题
                            remark=params.get('new_remark', ''),  # 新待办的备注
                            source=current_user.user_code,  # 新的待办发起人
                            worker=params.get('new_worker'),  # 新的指派人

                            task_type=params.get('task_type', '1'),
                            order_list=params.get('order_id_list', []),
                            is_critical=params.get('new_is_critical'),
                            limit_time=new_limit_time,

                            create_time=datetime.datetime.now(),
                            create_by=current_user.user_code,
                            status=params.get('status', cls.get_status('未完成').dict_id)
                            )
            task_obj.save()
            req_dict = dict(
                task_id=task_obj.task_id, task_code=task_obj.task_code, title=task_obj.title,
                remark=task_obj.remark, source=task_obj.source, worker=task_obj.worker, task_type=task_obj.task_type,
                order_list=task_obj.order_list, is_critical=task_obj.is_critical, limit_time=str(task_obj.limit_time),
                create_time=str(task_obj.create_time), create_by=task_obj.create_by, status=task_obj.status)
            return json.dumps(req_dict)
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_unread_task(cls):
        """
        获取当前登陆用户最新未读信息
        :return:
        """
        try:
            user_code = session.get('user_code')
            from rich_base_provider.sysadmin.sys_user_relations.models import User_relations
            has_unread_validate = User_relations.get_validation_list(user_code, session.get('org_id')).get(
                'validate_info')
            status = cls.get_status('未读').dict_id
            search = []
            search.append({'$match': {'$and': [{'status': status}, {'worker': user_code}]}})
            search.append({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            task_count = list(cls.objects.aggregate(*search))[0]["count"] if list(
                cls.objects.aggregate(*search)) else 0
            search.remove({'$group': {'_id': 0, 'count': {'$sum': 1}}})
            search.append({'$sort': {'create_time': -1}})
            if has_unread_validate != []:  # 判断当前是否有好友申请
                search.append({'$limit': 4})
            else:
                search.append({'$limit': 5})
            search.append({'$project': {'task_code': 1, 'title': 1, '_id': 0}})
            task_list = list(cls.objects.aggregate(*search))
            res_list = []
            if has_unread_validate != []:
                if task_list:
                    for task in task_list:
                        task_dict = {'id': task.get('task_code'),
                                     'url': '/task/deal/with/' + task.get('task_code'),
                                     'title': tran_title(task.get('title'))}
                        res_list.append(task_dict)
                    res_list.append('user_has_unread_validate')
                    task_count += 1
                    return res_list, task_count
                return res_list, task_count
            else:
                if task_list:
                    for task in task_list:
                        task_dict = {'id': task.get('task_code'),
                                     'url': '/task/deal/with/' + task.get('task_code'),
                                     'title': tran_title(task.get('title'))}
                        res_list.append(task_dict)
                    return res_list, task_count
                return res_list, task_count
        except Exception as e:
            logging.debug(e)
            raise e


def tran_title(title):
    """
    转换标题，长度超过10位转换为...
    :param title:
    :return:
    """
    try:
        if len(title) > 10:
            small_title = title[:10] + '...'
            return small_title
        else:
            return title
    except Exception as e:
        logging.debug(e)
        raise e