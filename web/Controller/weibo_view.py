from web import app
from flask import redirect, render_template, session, flash, url_for
from flask_wtf import Form
from wtforms import SubmitField, StringField, validators
from functools import wraps
from web.Controller.function.weiboApi import Client
from ..Model.database import Public,db,My

import re
import jieba
import datetime

baseurl = ''


class TokenForm(Form):
    access_Code = StringField('Access_Code', [validators.required()], description="你的得到的Token")
    button = SubmitField('提交')


def login_with_known_token(func):
    @wraps(func)
    def wrapper(*args, **kw):
        token = session.get('token')
        if not token:
            return redirect('/login')
        weibo = Client(token=token)
        # try:
        return func(weibo=weibo, *args, **kw)
        # except RuntimeError:
        #     return redirect(url_for('login_weibo'))

    return wrapper


@app.route(baseurl + '/login', methods=['POST', 'GET'])
def login_weibo():
    weibo = Client()
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
def get_person_info(weibo):
    try:
        uid = weibo.get('account/get_uid')
        session['uid'] = uid["uid"]
        print(uid)
    except RuntimeError as err:
        return render_template('errors/general.html', code=401, title='授权错误', other=str(err))
    return render_template('login/login_success.html', data=[['uid', uid['uid']]])


@app.route(baseurl + '/publictimeline')
@login_with_known_token
def get_public_weibo(weibo):
    x = weibo.get('statuses/public_timeline', count=50)
    for one in x["statuses"]:
        time = datetime.datetime.strptime(one["created_at"], '%a %b %d %H:%M:%S %z %Y')
        uid = one["id"]
        text = one["text"]
        db.session.add(Public(uid, text, time))

    db.session.commit()

    return str(x)


@app.route(baseurl + '/mytimeline')
@login_with_known_token
def get_my_weibo(weibo):
    for page in range(6,10):
        x = weibo.get('statuses/home_timeline', count=100, trim_user=1,page=page)
        for one in x["statuses"]:
            time = datetime.datetime.strptime(one["created_at"], '%a %b %d %H:%M:%S %z %Y')
            uid = one["id"]
            text = one["text"]
            db.session.add(My(uid, text, time))

    db.session.commit()

    return 'done'


@app.route(baseurl + '/weibo/<name>')
@login_with_known_token
def get_weibo_by_name(weibo, name):
    STOPWORDS = ['的', '地', '得', '而', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到',
                 '说', '要', '去', '你', '会', '着', '看', '好', '这', " ", "啊"]

    r = re.compile(r'[\u4e00-\u9fa5]+')

    x = weibo.get('statuses/user_timeline', screen_name=name, count=100)
    lists = x["statuses"]
    dicts = {}
    for one in lists:
        content = one['text']
        clear_content = re.sub(r"\[(.+?)\]", "", content)
        clear_content = re.sub(r" @(.+?) |(HTTP|http)s?://[^,， ]+", "", clear_content)
        clear_content = " ".join(r.findall(clear_content))
        seg_list = jieba.cut(clear_content)
        segs = list(seg_list)
        # print('内容:{}\n关键词:{}\n\n'.format(content, " ".join(segs)))

        for seg in segs:
            if seg not in STOPWORDS:
                if seg in dicts:
                    dicts[seg] += 1
                else:
                    dicts[seg] = 1

    dict_sorted = sorted(dicts.items(), key=lambda d: d[1], reverse=True)

    return render_template('highfreq.html', dict=dict_sorted)


