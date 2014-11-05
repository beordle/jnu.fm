from flask import Flask
from flask.ext.sqlalchemy import *
import pymysql
app = Flask('begin')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json = db.Column(db.Binary)
    username = db.Column(db.String(50))
"""
class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    pool= db.Column(db.String)
    own= db.Column(db.String)
    reviews=db.relationship('Review',backref='tweets',lazy=False)
    ownrealname= db.Column(db.String)
    ext=db.Column(db.UnicodeText)
    hasimage=db.Column(db.Boolean)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText)
    own= db.Column(db.String)
    tweets_id=db.Column(db.Integer,db.ForeignKey('tweets.id'))
    ownrealname=db.Column(db.String)
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/test'
app.secret_key = 'ilovehsy'
db.create_all()
