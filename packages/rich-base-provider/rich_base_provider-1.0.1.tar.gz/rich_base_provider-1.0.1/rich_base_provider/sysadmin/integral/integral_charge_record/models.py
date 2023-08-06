#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 17:24
# @Author  : denghaolin
# @Site    : www.rich-f.com
# @File    : models.py

import datetime, time
from rich_base_provider import db
from flask_security import current_user
import logging


def create_record_id():
    """
    创建积分兑换记录唯一id
    :return:
    """
    base_str = str(time.time()).replace('.', '')[:13]
    return 'R{:0<13}'.format(base_str)


class IntegralChargeRecord(db.Document):
    """
    积分兑换记录
    """
    record_id = db.StringField()  # 唯一id
    user_code = db.StringField()  # 兑换的用户的唯一id
    org_id = db.StringField()  # 兑换的机构的唯一id
    present_id = db.StringField()  # 兑换的礼物唯一id
    present_name = db.StringField()  # 兑换的礼物名称
    count = db.StringField()  # 兑换的数量
    deduct_integral = db.StringField()  # 扣除积分
    create_by = db.StringField()  # 创建人
    create_time = db.DateTimeField()  # 创建时间
    update_by = db.StringField()  # 更新人
    update_time = db.DateTimeField()  # 更新时间

    @classmethod
    def get_record_list_by_data(cls, present_id, page=1, per_page=20):
        """
        根据礼品id获取记录对象列表
        :param present_id:
        :param page:
        :param per_page:
        :return:
        """
        start_index = (int(page) - 1) * int(per_page)
        search = {
            '__raw__': {
                'present_id': present_id,
                # '$or': [
                #     {'present_name': re.compile(search_data)}
                # ]
            }
        }
        return cls.objects(**search).skip(start_index).limit(int(per_page)).order_by("-create_time").all()

    @classmethod
    def add_record(cls, params):
        """
        新增积分兑换记录
        :param params:
        :return:
        """
        try:
            record_id = create_record_id()
            user_code = params.get('user_code')
            org_id = params.get('org_id')
            present_id = params.get('present_id')
            present_name = params.get('present_name')
            count = params.get('count')
            deduct_integral = params.get('deduct_integral')
            create_by = current_user.user_code
            create_time = datetime.datetime.now()
            record = IntegralChargeRecord(record_id=record_id, user_code=user_code if user_code else '',
                                          present_id=present_id, org_id=org_id if org_id else '',
                                          present_name=present_name, count=str(count),
                                          deduct_integral=deduct_integral, create_by=create_by, create_time=create_time
                                          )
            record.save()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_record_by_present_id(cls, present_id):
        """
        根据礼品id查询记录
        :param present_id:
        :return:
        """
        try:
            return cls.objects(present_id=present_id).first()
        except Exception as e:
            logging.debug(e)
            raise e

    @classmethod
    def get_record_by_user_code_or_org_id(cls, page=1, per_page=20, user_code=None, org_id=None, start_time=None,
                                          end_time=None, ):
        """
        根据用户code或机构id获取兑换记录对象
        :param user_code:
        :param org_id:
        :return:
        """
        try:
            skip_nums = (int(page) - 1) * int(per_page)  # 偏移量
            if user_code:
                search = {
                    '__raw__': {
                        'user_code': user_code,
                    }
                }
                if start_time and end_time:
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                    count = cls.objects(create_time__gte=start_time, create_time__lte=end_time, **search).count()
                    res = cls.objects(create_time__gte=start_time, create_time__lte=end_time, **search).skip(
                        skip_nums).limit(int(per_page)).order_by('-create_time')
                    return res, count
                else:
                    record = cls.objects(**search).skip(skip_nums).limit(int(per_page)).order_by('-create_time')
                    count = cls.objects(**search).count()
                    return record, count
            if org_id:
                search = {
                    '__raw__': {
                        'org_id': org_id,
                    }
                }
                if start_time and end_time:
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                    count = cls.objects(create_time__gte=start_time, create_time__lte=end_time, **search).count()
                    res = cls.objects(create_time__gte=start_time, create_time__lte=end_time, **search).skip(
                        skip_nums).limit(int(per_page)).order_by('-create_time')
                    return res, count
                else:
                    res = cls.objects(**search).skip(skip_nums).limit(int(per_page)).order_by(
                        "-create_time").all()
                    count = cls.objects(**search).count()
                    return res, count
        except Exception as e:
            logging.debug(e)
            raise e
