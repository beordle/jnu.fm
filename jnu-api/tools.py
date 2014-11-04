#controller
#coding:utf-8
import re
from flask import Flask, g, request, make_response
import time
from functools import wraps
import jinja2
import __builtin__

__builtin__.word_command_map={
}

def route(re_str):
  def _inline(func):
      @wraps(func)
      def wrap_func(**wrap):

                return func(**wrap)
      __builtin__.word_command_map[re_str]=func
      return wrap_func
  return _inline

def need_bind(func):
      @wraps(func)
      def wrap_func(**wrap):
                if wrap['user']=='need':
                    return gen_text_response,u'need bind'
                else:
                    return func(**wrap)
      return wrap_func

def response_text(func):
      @wraps(func)
      def wrap_func(**wrap):
                    return gen_text_response,func(**wrap)
      return wrap_func

def response_news(func):
      @wraps(func)
      def wrap_func(**wrap):
                    return gen_news_response,func(**wrap)
      return wrap_func

def get_token():
  return "jnufmwx123"

def helpinfo(content):
  content=u"你输入的{content}是无效指令,要查看帮助请回复help".format(**{'content':content})
  return gen_text_response,content


def subscribe_welcome(from_user,to_user):
      content=u"欢迎使用"
      return gen_response(from_user,to_user,content)


def gen_news_response(FromUserName,ToUserName,items):
  reply = """<xml>
<ToUserName><![CDATA[{{toUser}}]]></ToUserName>
<FromUserName><![CDATA[{{fromUser}}]]></FromUserName>
<CreateTime>{{time}}</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>{{count}}</ArticleCount>
<Articles>
{%for item in items%}
<item>
<Title><![CDATA[{{item.title}}]]></Title>
<Description><![CDATA[{{item.description}}]]></Description>
<PicUrl><![CDATA[{{item.picurl}}]]></PicUrl>
<Url><![CDATA[{{item.url}}]]></Url>
</item>
{%end for%}
</Articles>
</xml> 
"""

  template = jj.Template(reply)
  text=template.render(toUser = ToUserName,
    fromUser=FromUserName,
    time=str(int(time.time())),
    count=len(items),
    items=items)
  response = make_response( text )
  response.content_type = 'application/xml'
  return response

def gen_text_response(FromUserName,ToUserName,Content):
  reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
  response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content ) )
  response.content_type = 'application/xml'
  return response

from controller import *

def command_process(content,from_user):
   word_command_map=__builtin__.word_command_map
   for re_str in word_command_map.keys():
            find=re.match(re_str,content)
            if find:
               args=find.groupdict(False)
               if all(args):
                  args['user']=from_user
                  return word_command_map[re_str](**args)
   else:
      return helpinfo(content)

if __name__=="__main__":
  print command_process(u'kebiao 43 34','need')
  print command_process(u'kebiao','need')
  print command_process(u'余额','nee')
  print command_process(u'记录','nee')
  print command_process(u'book 方法','nee')