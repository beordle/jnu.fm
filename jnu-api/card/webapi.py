#coding:utf-8 
import requests
import urlparse
import urlparse
import os
import base64

from flask import Flask, request, redirect, url_for,jsonify,Blueprint,render_template
web = Blueprint( __name__, __name__,template_folder='templates',static_folder='static')

from pyquery import PyQuery as pq
from detective import mix_password,normal_data
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import time
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *


def auto_form(url,text,r):
  action=pq(text)("form").attr['action']
  url=urlparse.urljoin(url,action)
  data={}
  for i in pq(text)("form select"):
    data[pq(i).attr['name']] = [pq(j).attr['value'] for j in pq(i)("option")]

  for i in pq(text)("form input"):
    data [ pq(i).attr['name'] ]=pq(i).attr['value']
  methods={'get':r.get,'post':r.post}
  method_name=pq(text)("form").attr['method']
  func=methods[method_name]
  return func,url,data


def login(stuid,password=None):
    if not password: password=stuid[-6:]
    r=requests.session()
    r.headers={'Host':'card.jnu.edu.cn:8080','Referer':'http://card.jnu.edu.cn/platform/cc/index',}
    r.get("http://card.jnu.edu.cn").text
    r.get("http://card.jnu.edu.cn:8080/getCheckpic.action?rand=8000.")

    data={
    'loginType':'2',
    'name':stuid,
    'passwd': mix_password(r,password),
    'rand':'8000',
    'userType':'1'
    }

    r.post("http://card.jnu.edu.cn:8080/loginstudent.action",data=data).text
    # login sucessful on here!!
    return r


def months_data(r):
  text=r.get("http://card.jnu.edu.cn:8080/accounthisTrjn.action").text

  func,url,data= auto_form("http://card.jnu.edu.cn:8080",text,r)
  text=func(url,data=normal_data(data)).text
  func,url,data=auto_form(url,text,r)

  idata={
  'inputEndDate': (date.today()+relativedelta(days=0)).strftime('%Y%m%d'),
  'inputStartDate':(date.today()+relativedelta(days=-7)).strftime('%Y%m%d'),
  }
  data.update(idata)


  text=func(url,data=data).text
  func,url,data=auto_form(url,text,r)
  text=func(url,data=data).text
  func,url,data= auto_form("http://card.jnu.edu.cn:8080",text,r)
  months_list=[]
  for i in pq(text)(".listbg , .listbg2 "):
    colums=[pq(j).text() for j in pq(i)("td")]
    months_list.append(
                      {
                       'way':colums[1],
                       'position':colums[2],
                       'price':colums[3],
                       'rest':colums[4], 
                       'time':(parse(colums[0])+relativedelta(minutes=+55)).isoformat(' ') , 
 })
  return months_list



def person_data(r):
  text=r.get('http://card.jnu.edu.cn:8080/accountcardUser.action').text
  s=[]
  for i in pq(text)("td.neiwen"):
     text=pq(i).text().replace(u'\xa0', u' ')
     if  not u'：'  in text:
         s.append(  text  )
  return s


def rest_data(r):
  s=person_data(r)
  for i in s:
    if i.find(u'余额')>=0:
      return i.split(u'元')[0]

def today_data(r):
  text=r.get("http://card.jnu.edu.cn:8080/accounttodayTrjn.action").text
  func,url,data= auto_form("http://card.jnu.edu.cn:8080",text,r)
  text=func(url,data=normal_data(data)).text
  today_list=[]
  for i in pq(text)(".listbg , .listbg2 "):
    colums=[pq(j).text() for j in pq(i)("td")]
    today_list.append(
                      {
                       'way':colums[1],
                       'position':colums[2],
                       'price':colums[3],
                       'rest':colums[4], 
                       'time':(parse(colums[0])+relativedelta(minutes=+55)).isoformat(' ') , 
 })
  return today_list




#ff
#app=Flask('ssddd')

#app.register_blueprint(web, url_prefix='/web')


@web.route('/today', methods=['GET'])
def ftoday_data_json():
   stuid=request.args['stuid']
   password=request.args['password']
   r=login(stuid,password)
   return jsonify(data=today_data(r))

@web.route('/personalinfo', methods=['GET'])
def d12data_json():
   stuid=request.args['stuid']
   password=request.args['password']
   r=login(stuid,password)
   return jsonify(data=person_data(r))

@web.route('/rest', methods=['GET', 'POST'])
def today_data_json():
   stuid=request.args['stuid']
   password=request.args['password']
   r=login(stuid,password)
   return jsonify(data=rest_data(r) )

@web.route('/month', methods=['GET', 'POST'])
def month_data_json():
   stuid=request.args['stuid']
   password=request.args['password']
   r=login(stuid,password)
   return jsonify(data=months_data(r) )

#app.run(port=80)