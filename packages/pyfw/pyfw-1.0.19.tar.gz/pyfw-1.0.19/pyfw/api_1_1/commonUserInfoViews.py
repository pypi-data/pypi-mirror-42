from flask import render_template, session, abort, request, redirect, url_for, current_app, flash, jsonify
from flask_login import login_required

from pyfw.main.models import CommonUserInfo
from . import api_1_1





@api_1_1.route('/commonuserinfos', methods=['GET'])
def getList():
    """
    获取数据列表
    :return:
    """

    # 查询字符串
    filters = set()

    # 构建查询条件
    user_name = request.args.get('name')

    if user_name: filters.add(CommonUserInfo.login_account.contains(user_name))

    # 获取查询页
    page = request.args.get('page', 1, type=int)

    pagination = CommonUserInfo.query.filter(*filters).order_by(CommonUserInfo.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)

    return jsonify({
        'items': [user.to_json() for user in pagination.items],
        'page': pagination.page,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num,
        'has_next': pagination.has_next,  # 如果有下一页，返回True
        'has_prev': pagination.has_prev,  # 如果有上一页，返回True
        'pages': pagination.pages,  # 查询得到的总页数
        'per_page': pagination.per_page,  # 每页显示的记录数量
        'total': pagination.total,
        'iter_pages': [pages for pages in
                       pagination.iter_pages(left_edge=2, left_current=2, right_current=3, right_edge=2)]

    })




@api_1_1.route('/commonuserinfo', methods=['post'])
def post():
    """
    新增对象
    :param self:
    :return:
    """

    #构建查询条件
    login_account = request.form['login_account']



    return jsonify({
            'result': login_account,
            'msg':'新增成功'
     })



@api_1_1.route('/commonuserinfo/<int:id>', methods=['get'])
def get(id):
        """
        获得单对象
        :param id:
        :return:
        """



        #查询字符串
        filters=set()

        #构建查询条件
        user_name = request.args.get('name')

        if user_name :filters.add(CommonUserInfo.login_account.contains(user_name))


        #获取查询页
        page = request.args.get('page', 1, type=int)





        pagination = CommonUserInfo.query.filter(*filters).order_by(CommonUserInfo.id.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)





        return jsonify({
            'items': [user.to_json() for user in pagination.items],
            'page': pagination.page,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num,
            'has_next' :pagination.has_next, #如果有下一页，返回True
            'has_prev': pagination.has_prev, #如果有上一页，返回True
            'pages': pagination.pages, #查询得到的总页数
            'per_page': pagination.per_page, #每页显示的记录数量
            'total': pagination.total,
            'iter_pages':[pages for pages in pagination.iter_pages(left_edge = 2 ,left_current=2,right_current=3,right_edge=2)]

        })


@api_1_1.route('/commonuserinfo/<int:id>', methods=['put'])
def put( id):
        """
        更新对象
        :param id:
        :return:
        """

        login_account = request.form['login_account']


        return jsonify({
            'result': id,
            'login_account':login_account,
            'msg': '修改成功'
        })



@api_1_1.route('/commonuserinfo/<int:id>', methods=['delete'])
def delete( id):
        """
        删除对象
        :param id:
        :return:
        """




        return jsonify({
            'result': id,
            'msg': '删除成功'
        })