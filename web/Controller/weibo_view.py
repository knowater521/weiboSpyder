from web import app
from flask import redirect, render_template,session, flash, url_for, abort
from web.Controller import weibo
from flask_wtf import Form
from wtforms import SubmitField,StringField,validators
from functools import wraps
baseurl = ''


class TokenForm(Form):
    access_Code = StringField('Access_Code', [validators.required()], description="你的得到的Token")
    button = SubmitField('提交')


def login_with_known_token(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if not weibo.token:
            token = session.get('token')
            if not token:
                return redirect('/login')
            weibo.set_token(token)
        return func(*args, **kw)
    return wrapper


@app.route(baseurl + '/login', methods=['POST', 'GET'])
def login_weibo():
    history_token = session.get('token')
    if history_token:
        weibo.set_token(history_token)
    if weibo.token:
        return redirect(url_for('get_person_info'))

    form = TokenForm()
    if form.validate_on_submit():
        try:
            weibo.set_code(form.access_Code.data)
        except RuntimeError as err:
            flash('错误' + str(err))
        else:
            session['token'] = weibo.token
            return redirect(url_for('get_person_info'))
    return render_template('login/login.html', form=form, authorize_url=weibo.authorize_url)


@app.route(baseurl + '/person')
@login_with_known_token
def get_person_info():
    try:
        uid = weibo.get('account/get_uid')
        session['uid'] = uid["uid"]
        print(uid)
    except RuntimeError as err:
        return render_template('errors/general.html', code=401, title='授权错误', other=str(err))
    return render_template('login/login_success.html', data=[['uid', uid['uid']]])


@app.route(baseurl + '/friendsbilateral')
@login_with_known_token
def get_friends_bilateral():
    x = weibo.get('friendships/friends/bilateral',uid =3173405774)
    for one in x["users"]:
        try:
            print("{} {} {} {}".format(one['screen_name'],one['description'],one['status']['text'][:5],one['friends_count'] ) )
        except:
            pass
    return str(x)



