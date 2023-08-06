#!/usr/bin/env python
# -*- coding: utf-8 -*-

' json序列化工具对象'
import datetime
import json



class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

__author__ = 'Andrew Wen'

def ObjToJson(obj):
    """
    对象转换为字典，排除数据库属性
    :param obj:
    :return:
    """
    ctdict = obj.__dict__

    # 去掉数据库对象
    ctdict.pop('_sa_instance_state')
    ctdict["key"]=ctdict["id"]

    return ctdict


def JsonStrToObj(jsonStr,targetObj):
    """
    json转换到数据库对象
    :param obj:
    :return:
    """
    ctdict = json.loads(jsonStr)

    method = ctdict["method"]



    for key in ctdict:
        if hasattr(targetObj, key):
            setattr(targetObj, key, ctdict[key])



    return method,targetObj




def CopyObj(source,target):
    """
    拷贝对象属性，排除数据库相关特性
    :param source:
    :param target:
    :return: 负责完成属性的对象
    """
    sourcedict = source.__dict__

    # 去掉数据库对象
    sourcedict.pop('_sa_instance_state')

    for key in sourcedict:
        if hasattr(target, key):
            setattr(target, key, sourcedict[key])



    return target



def ObjToJsonStr(obj):
    ctdict = obj.__dict__

    # 去掉数据库对象
    ctdict.pop('_sa_instance_state')

    return json.dumps(ctdict,cls=CJsonEncoder)



def GetResult(pagination,result=None):
    """
    获得返回结果对象
    :param pagination:
    :return:
    """
    if result== None:
       result={"code":"0000","msg":"操作成功"}

    page= {
            'result':{"code":result["code"],"msg":result["msg"]},
            'list': [user.to_json() for user in pagination.items],
            'pagination':{'total': pagination.total, 'pageSize': pagination.per_page, 'current': pagination.page}
        }

    # {
    #     'list': [user.to_json() for user in pagination.items],
    #     'page': pagination.page,
    #     'prev_num': pagination.prev_num,
    #     'next_num': pagination.next_num,
    #     'has_next': pagination.has_next,  # 如果有下一页，返回True
    #     'has_prev': pagination.has_prev,  # 如果有上一页，返回True
    #     'pages': pagination.pages,  # 查询得到的总页数
    #     'per_page': pagination.per_page,  # 每页显示的记录数量
    #     'total': pagination.total,
    #     'iter_pages': [pages for pages in
    #                    pagination.iter_pages(left_edge=2, left_current=2, right_current=3, right_edge=2)]
    #
    # }

    return page;