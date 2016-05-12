from web import app
from flask import redirect, render_template,session, flash, url_for, abort
from web.Controller import weibo
from flask_wtf import Form
from wtforms import SubmitField,StringField,validators
from functools import wraps
baseurl = ''
import re
import jieba


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
    x = weibo.get('comments/timeline',uid =3173405774)
    # for one in x["users"]:
    #     try:
    #         print("{} {} {} {}".format(one['screen_name'],one['description'],one['status']['text'][:5],one['friends_count'] ) )
    #     except:
    #         pass
    return str(x)


@app.route(baseurl + '/weibo/<name>')
@login_with_known_token
def get_weibo_by_name(name):
    STOPWORDS=[u'的',u'地',u'得',u'而',u'了',u'在',u'是',u'我',u'有',u'和',u'就',u'不',u'人',u'都',u'一',u'一个',u'上',u'也',u'很',u'到',
               u'说',u'要',u'去',u'你',u'会',u'着',u'没有',u'看',u'好',u'自己',u'这'," "]

    r = re.compile(r'[\u4e00-\u9fa5]+')

    x = weibo.get('statuses/user_timeline', screen_name=name,count=100)
    lists = x["statuses"]
    dict = {}
    for one in lists:
        content = one['text']
        clear_content = re.sub(r"\[(.+?)\]", "", content)
        clear_content = re.sub(r" @(.+?) |(HTTP|http)s?://[^,， ]+", "", clear_content)
        clear_content = " ".join(r.findall(clear_content))
        seg_list = jieba.cut(clear_content)
        segs = list(seg_list)
        print('内容:{}\n关键词:{}\n\n'.format(clear_content," ".join(segs)))

        for seg in segs:
            if seg not in STOPWORDS:
                if seg in dict:
                    dict[seg] += 1
                else:
                    dict[seg] = 1

    dict_sorted = sorted(dict.items(), key=lambda d: d[1], reverse=True)
    for a,b in dict_sorted:
        if b > 0:
            print(a + ',' + str(b) + '\n')
    return render_template('highfreq.html',dict = dict_sorted)

