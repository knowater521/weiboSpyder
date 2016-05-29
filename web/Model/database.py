from flask.ext.sqlalchemy import SQLAlchemy
from web import app

db = SQLAlchemy(app)


class Public(db.Model):
    __bind_key__ = 'weibo'
    uid = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime)
    wid = db.Column(db.Integer, primary_key=True)

    def __init__(self, uid, text, time):
        self.uid = uid
        self.text = text
        self.time = time


class My(db.Model):
    __bind_key__ = 'weibo'
    uid = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime)
    wid = db.Column(db.Integer, primary_key=True)

    def __init__(self, uid, text, time):
        self.uid = uid
        self.text = text
        self.time = time


class Lab(db.Model):
    __bind_key__ = 'weibo'
    uid = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime)
    wid = db.Column(db.Integer, primary_key=True)

    def __init__(self, uid, text, time):
        self.uid = uid
        self.text = text
        self.time = time