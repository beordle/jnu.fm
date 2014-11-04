# -*- coding:utf-8 -*-
import time
from flask import Flask, g, request, make_response,render_template
import hashlib
import re
from functools import wraps
import xml.etree.ElementTree as ET
#from ooredis import *
#from models import *
from controller import *
app = Flask(__name__)

def need(*list):
    def _inline(func):
        @wraps(func)
        def wrap_func(**wrap):
            for i in list:
                func.func_globals[i]=request.args.get(i)
            return func(**wrap)
        return wrap_func
    return _inline

def gen_signature(timestamp, nonce, token):
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    return hashlib.sha1(s).hexdigest()

@app.route('/<string:content>', methods = ['GET', 'POST'] )
def WX_Response_test(content):
  to_user=from_user="test"
  process_func,reply_content=command_process(content,from_user)
  return process_func(from_user,to_user,reply_content)


@app.route('/bind', methods = ['GET', 'POST'] )
@need('wxid','stuid','jwcpw','cardpw')
def WX_Bind_Response():
  if stuid and jwcpw and cardpw and wxid:
     pass
     return render_template('success.html')
  else:
     return render_template('bind.html',wxid=wxid)

@app.route('/', methods = ['GET', 'POST'] )
@need('signature','timestamp','nonce','echostr')
def WX_Response():

  token=get_token()
  if gen_signature (timestamp, nonce, token) == signature:  
      return make_response(echostr)

  xml_recv = ET.fromstring(request.data)
  to_user = xml_recv.find("ToUserName").text
  from_user = xml_recv.find("FromUserName").text
  content=xml_recv.find("Content").text

  if xml_recv.find("MsgType").text=='event' and xml_recv.find("Event").text=='subscribe':
          return subscribe_welcome(to_user,from_user)
 
  process_func,reply_content=command_process(content,from_user)
  return process_func(from_user,to_user,reply_content)


if __name__=="__main__":
     app.run(host="0.0.0.0",port=8000,debug=True)
"""
t=time.time()
for i in range(100):
  func,content=command_process("kebiao hello world",'dd')
print time.time()-t"""
