from flask import render_template, session, abort, request, redirect, url_for, current_app, flash
from flask_login import login_required

from pyfw.main.models import CommonUserInfo
from . import main
from .forms import NameForm

from flask_sqlalchemy import get_debug_queries



@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                '查询慢的Sql语句为: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NameForm()
    if form.validate_on_submit():

        user=CommonUserInfo()

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        return redirect(url_for('.index'))
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_email(current_app.config['FLASKY_ADMIN'], 'New User',
    #                        'mail/new_user', user=user)
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data

    return render_template('main/index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))



@main.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():

    userlist = CommonUserInfo.query.all()
    # page = request.args.get('page', 1, type=int)
    # pagination = CommonUserInfo.query.order_by(CommonUserInfo.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #     error_out=False)
    #
    # posts = pagination.items

    form = NameForm()

    return render_template('main/userlist.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),userlist=userlist)


@main.route('/test', methods=['GET', 'POST'])
def test():

    return render_template('main/test.html')

@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'