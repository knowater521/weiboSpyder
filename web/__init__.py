from flask_bootstrap import Bootstrap
# import redis
from flask import Flask, session
from datetime import timedelta

from web.Model import Environment

app=Flask(__name__)
app.permanent_session_lifetime = timedelta(days=31)
# BootStarp init
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['BOOTSTRAP_QUERYSTRING_REVVING'] = False
Bootstrap(app)

# Redis
# r = redis.Redis(host='localhost',port=6379,db=0,password=Environment.redis_passwd)

# Database Setting

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
# app.config['SQLALCHEMY_ECHO']=True
mysql_url = 'mysql+mysqlconnector://{0}:{1}@localhost:{2}/'.format(Environment.mysql_user, Environment.mysql_passwd,
                                                                   Environment.mysql_port)
app.config['SQLALCHEMY_BINDS'] = {"project": mysql_url + 'weibo'}


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=31)


import web.Controller
