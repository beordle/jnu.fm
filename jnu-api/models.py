from flask import Flask
from flask.ext.sqlalchemy import *
import pymysql
app = Flask('begin')
db = SQLAlchemy(app)

class CardUser3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stuid = db.Column(db.String(50))
    fakeid = db.Column(db.String(50))
    userid = db.Column(db.String(50))
    passwordofcard=db.Column(db.String(50))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///core.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/test'
db.create_all()
CardUser=CardUser3
