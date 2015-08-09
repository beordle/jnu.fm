#coding:utf-8
from tools import gen_text_response,route,response_text,need_bind, response_news
import requests
import base64

@route("kebiao (?P<stuid>\w+) (?P<jwcpw>\w+)")
@response_text
def kebiao(stuid,jwcpw,user):
  #提供函数处理方法
  content=u"你好1"
  print stuid,jwcpw
  #print first,'d',secode
  return content

@route(u"version")
@route(u"版本")
@response_text
def version(user):
  return u" JNU.FM v2.0 高内聚的内核,更高级的抽象,更快更稳定 现已开源 http://github.com/beordle/jnu.fm"

@route(u"饭卡余额$")
@route(u"余额$")
@route("rest$")
@route("yue$")
@need_bind
@response_text
def rest(user):
  #提供函数处理方法
  print user
  stuid="2012052690"
  cardpw="052690"
  text=requests.get("http://125.218.212.151:8081/card/rest?stuid={stuid}&password={cardpw}".format(**{'stuid':stuid,'cardpw':cardpw})).json()
  content=u"您的校园卡余额为%s" %text['data']
  return content

@route(u"今日消费记录$")
@route("card$")
@route("饭卡$")
@need_bind
@response_news
def today(user):
  stuid="2012052691"
  cardpw="052691"
  text=requests.get("http://125.218.212.151:8081/card/today?stuid={stuid}&password={cardpw}".format(**{'stuid':stuid,'cardpw':cardpw})).json()
  items=[]
  news={}
  news['title']= " "*5 +u"今日消费记录"
  news['description']=""
  news['picurl']=""
  news['url']=""
  items.append(news)
  for i in text['data']:
    news={}
    news['title']= "%s %s %s" %(i['time'].split(' ')[1],i['position'],i['price'])
    news['description']=i['price']
    news['picurl']=""
    news['url']=""
    items.append(news)
  return items

@route(u"课表$")
@route("kebiao$")
@need_bind
@response_news
def kebiao(user):
  stuid="2012052691"
  cardpw="052691"
  text=requests.get("http://125.218.212.151:8081/card/today?stuid={stuid}&password={cardpw}".format(**{'stuid':stuid,'cardpw':cardpw})).json()
  items=[]
  for i in text['data']:
    news={}
    news['title']=i['position']
    news['description']=i['price']
    news['picurl']="http://technologyplusblog.com/wp-content/uploads/2012/07/180px-SD_card_icon.svg_-150x150.png"
    news['url']=""
    items.append(news)
  return items

@route(u"图书 (?P<book>[^\s]*)")
@route("book (?P<book>[^\s]*)")
@response_news
def book(book,user):

  text=requests.get("http://125.218.212.151:8081/book/search/engine?query=%s&page=1" %book).json()
  items=[]
  for i in text['data'][:10]:
    try:
      news={}
      news['title']=i['title']
      news['description']='\n'.join(i['position'])
      news['picurl']=i['image']
      news['url']="http://beordle.com:8081/web/book?url="+base64.urlsafe_b64decode(i['url'] )
      items.append(news)
    except:
      pass

  return items
