# coding:utf-8

import json
import re
import urllib
import urllib2
import cookielib
import base64
import hashlib
import StringIO
import time
import hashlib
import urlparse
import json

from urlparse import *
from urlparse import urljoin
from functools import wraps


import chardet
import requests
from bs4 import BeautifulSoup

from models import *

from flask import Blueprint, render_template, abort, Flask
from flask import *
from jinja2 import TemplateNotFound
from functools import wraps
from flask.ext.sqlalchemy import *
from user.token import get, auth, getUsernameFromToken
from jnulib import book
from jnulib import getimg
from jnulib import getimg
from jwckit.func import get_xls, login, get_kaoshi

app = Flask('begin')

from web import web_book_callback
from web import youku
from card import webapi
app.register_blueprint(web_book_callback.web, url_prefix='/web')
app.register_blueprint(book.index, url_prefix='/book')
app.register_blueprint(getimg.index, url_prefix='/isbn')
app.register_blueprint(youku.web, url_prefix='/youku')
app.register_blueprint(webapi.web, url_prefix='/card')


app.config['HEADER_FOLDER'] = 'static/avatar'
app.config['BACKGROUND_FOLDER'] = 'static/background'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join
                              (app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def get_class_table2(user="2012052690", password="143217", year=2012, term=1):
    ret = login(user, password)
    return get_xls(ret, year, term)


def get_kaoshi_table2(user="2012052690", password="143217", year=2012, term=1):
    ret = login(user, password)
    return get_kaoshi(ret, year, term)



@app.route('/auth_jwc', methods=['GET', 'POST'])
def jwc():
    args=request.args
    token = args['token']
    jwc_username = args['jwc_username']
    jwc_password = args['jwc_password']
    s=type(login(jwc_username,jwc_password))
    if not s==type('string'):
        username=getUsernameFromToken(token)
        #token不通过
        if not username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)
        user = User.query.filter_by(username=username).one()
        data = json.loads(user.json)
        data['jwc_username']=jwc_username
        data['jwc_password']=jwc_password
        user.json = json.dumps(args)
        db.session.add(user)
        db.session.commit()
        ret={
             'version': 1.0,
             'status': 0,
             }
        return jsonify(ret)
    else:
        ret={
             'version': 1.0,
             'status': 1,
             }
        return jsonify(ret)

@app.route('/get_info', methods=['GET', 'POST'])
def get_info():
    args=request.args
    token = args['token']
    username = args['username']

    self_username=getUsernameFromToken(token)
    #token不通过
    if not self_username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)

    q = User.query.filter_by(username=username).all()
    #用户不存在
    if len(q)==0:
            ret={
             'version': 1.0,
             'status': 4,
             }
            return jsonify(ret)
    
    user=q[0]
    data = json.loads(user.json) 
    ret_data={}
    ret_list=["nickname","realname","sex","signature","avatar","background"]
    for key,value in data.items():
        if key in ret_list:
            ret_data[key]=value
    if data.has_key('tid'):
        ret_data['avatar']='/static/avatar/'+username+'-'+data['tid']+'.png'
        ret_data['background']='/static/background/'+username+'-'+data['tid']+'.png'
    ret_data['version']=1.0
    ret_data['status']=0    
    return jsonify(ret_data)


@app.route('/set_info', methods=['GET', 'POST'])
def set_info():
    args=request.args
    token = args['token']
    username=getUsernameFromToken(token)
    #token不通过
    if not username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)

    user = User.query.filter_by(username=username).one()
    data = json.loads(user.json)

    set_data={}
    set_list=["nickname","realname","sex","signature"]
    for key,value in args.items():
        if key in set_list:
            print (key)
            set_data[key]=value
    data.update(set_data)
    user.json=json.dumps(data)
    db.session.add(user)
    db.session.commit()

    ret_data={}
    ret_data['version']=1.0
    ret_data['status']=0    
    return jsonify(ret_data)


@app.route('/get_username', methods=['GET', 'POST'])
def get_username():
    args=request.args
    token = args['token']
    username=getUsernameFromToken(token)
    #token不通过
    if not username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)
    ret={
             'version': 1.0,
             'username':username,
             'status': 0,
    }

    return jsonify(ret)


@app.route('/set_avatar', methods=['POST'])
def set_avatar():
    args=request.args
    print (args)
    token = args['token']
    import time
    tid=str(time.time())
    username=getUsernameFromToken(token)
    #token不通过
    if not username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)

    user = User.query.filter_by(username=username).one()
    data = json.loads(user.json)
    data['tid']=tid
    user.json=json.dumps(data)
    db.session.add(user)
    db.session.commit()

    file = request.files['file']
    if file:
            filename = username+'-'+tid+'.png'
            filepath=os.path.join(app.config['HEADER_FOLDER'], filename)
            file.save(os.path.join(app.config['HEADER_FOLDER'], filename))

            ret={
             'version': 1.0,
             'status': 0,
             'url': "/static/avatar/"+filename,
             }
            return jsonify(ret)



    return jsonify(ret_data)

@app.route('/set_background', methods=['POST'])
def set_background():
    args=request.args
    print (args)
    token = args['token']

    username=getUsernameFromToken(token)
    #token不通过
    if not username:
            ret={
             'version': 1.0,
             'status': 2,
             }
            return jsonify(ret)

    file = request.files['file']
    if file:
            filename = username+'.png'
            filepath=os.path.join(app.config['BACKGROUND_FOLDER'], filename)
            file.save(os.path.join(app.config['BACKGROUND_FOLDER'], filename))

            ret={
             'version': 1.0,
             'status': 0,
             'url': '/static/background/'+filename,
             }
            return jsonify(ret)



    return jsonify(ret_data)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    args=request.args
    username = args['username']
    password = args['password']
    q = User.query.filter_by(username=username).all()

    #用户已存在
    if len(q)== 1:
        ret={
             'version': 1.0,
             'status': 1,
             'token': 'none',
             }
        return jsonify(ret)

    #用户不存在
    if len(q) == 0:
        #在数据库中添加用户
        user = User(username=username)
        args={}
        args['password']=password
        user.json = json.dumps(args)
        db.session.add(user)
        db.session.commit()
        #生成token
        token = get(username)
        ret={
             'version': 1.0,
             'status': 0,
             'token': token,
             }
        return jsonify(ret)




@app.route('/login', methods=['GET', 'POST'])
def login2():
    args=request.args
    username = args['username']
    password = args['password']

    q = User.query.filter_by(username=username).all()

    #用户不存在
    if len(q) == 0:
        ret={
             'version': 1.0,
             'status': 1,
             'token': 'none',
             }
        return jsonify(ret)
    
    #用户已存在
    if len(q)== 1:
        user=q[0]
        data = json.loads(user.json)

        #如果密码不符
        if not data['password']==password:
            ret={
                 'version': 1.0,
                 'status': 2,
                 'token': 'none',
                 }
            return jsonify(ret)

        else:
           token=get(username)
           ret={
             'version': 1.0,
             'status': 0,
             'token': token,
             }
           return jsonify(ret)

@app.route('/version')
def version():
    return jsonify(version=1)

@app.route('/password/reset', methods=['GET', 'POST'])
def password_reset():

    if 'oldpassword' in request.args:
        oldpassword = request.args['oldpassword']
        username = request.args['username']
        newpassword = request.args['password']

    q = User.query.filter_by(username=username).all()
    user = q[0]
    dic = json.loads(user.json)
    if oldpassword == dic['password']:
        dic['password'] = newpassword
    else:
        return jsonify(status="Password not match")
    user.json = json.dumps(dic)
    db.session.add(user)
    db.session.commit()
    return jsonify(status="Password reset success")


@app.route('/sync', methods=['GET', 'POST'])
def sync():

    args = hebing(request.form, request.args)
    token = args.get('token')
    username = getUsernameFromToken(token)

    dic = delete(dic)
    return_val = dict(
        version=1.0,
        data=None
    )
    q = User.query.filter_by(username=username).all()
    user = q[0]
    dic = json.loads(user.json)

    user.json = json.dumps(dic)
    db.session.add(user)
    db.session.commit()
    return_val['data'] = delete(dic)
    return jsonify(return_val)


@app.route('/kaoshi/get', methods=['GET', 'POST'])
def get_kaoshi_table123():

    user = request.args['user']
    password = request.args['password']
    year = request.args['year']
    term = request.args['term']
    year, term = int(year), int(term)

    return jsonify(version=1.0, data=get_kaoshi_table2(user, password, year, term))


@app.route('/class/get', methods=['GET', 'POST'])
def get_class_table123():

    user = request.args['user']
    password = request.args['password']
    year = request.args['year']
    term = request.args['term']
    year, term = int(year), int(term)

    data = get_class_table2(user, password, year, term)
    return jsonify(version=1.0, data=data)


@app.route('/kaoshi/auth', methods=['GET', 'POST'])
def get_kaoshi_by_auth():

    jwcpw = request.args['jwcpw']
    token = request.args['token']
    year = request.args['year']
    term = request.args['term']
    year, term = int(year), int(term)
    username = getUsernameFromToken(token)

    if not username:
        return jsonify(version=1.0, status='AuthNotPass')
    else:
        user = User.query.filter_by(username=username).one()
        data = json.loads(user.json)
        id, pw = data['jwcid'], jwcpw
    return jsonify(version=1.0, data=get_kaoshi_table2(id, pw, year, term))


@app.route('/class/auth', methods=['GET', 'POST'])
def get_class_by_auth():

    jwcpw = request.args['jwcpw']
    token = request.args['token']
    year = request.args['year']
    term = request.args['term']
    year, term = int(year), int(term)
    username = getUsernameFromToken(token)

    if not username:
        return jsonify(version=1.0, status='AuthNotPass')
    else:
        user = User.query.filter_by(username=username).one()
        data = json.loads(user.json)
        id, pw = data['jwcid'], jwcpw
    return jsonify(version=1.0, data=get_class_table2(id, pw, year, term))
app.secret_key="dsfsdfsdfijf3qre3829urfd89hscf893whfdr378w23gherhde"

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8081)
