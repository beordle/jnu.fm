#coding:utf-8
from tools import gen_text_response,route,response_text,need_bind, response_news
import requests

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
  for i in text['data']:
    news={}
    news['title']=i['position']
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
    news['picurl']=""
    news['url']=""
    items.append(news)
  return items

@route(u"图书 (?P<book>\w+)")
@route("book (?P<book>\w+)")
@response_news
def book(book,user):
  """
{
author: " 袁小荣编著   ",
checkout: 1,
detail: " 本书依据大量原始材料，包括专列、专机资料，在各地的讲话、谈话和经过考证的回忆，揭示毛泽东的行踪、活动和思想变化过程，剖析抗美援朝、庐山会议、“四清”运动、“九·一三”事件、“文化大革命”、“四人帮”篡权等重大事件的前因后果。",
douban: "http://book.douban.com/isbn/9787511521293/",
image: "http://book.bookday.cn/book/cover?isbn=9787511521293&w=67&h=97",
isbn: "9787511521293",
lookup: 1,
position: [
"本部五楼社科阅览区 A752/20148 馆内阅览 ",
"本部四楼中文图书外借区 A752/20148 到期 14-12-14 ",
"南校区图书馆借阅区 A752/20148 在架上 "
],
publish: "北京 : 人民日报出版社, 2014   ",
size: "3册 (1441页) : 图 ; 24cm",
status: " ",
title: "毛泽东离京巡视纪实",
url: "http://202.116.13.244/search~S1*chx?/X(%E6%AF%9B)&SORT=D/X(%E6%AF%9B)&SORT=D&SUBKEY=(%E6%AF%9B)/1%2C40%2C40%2CB/frameset&FF=X(%E6%AF%9B)&SORT=D&1%2C1%2C",
year: "2014"
},
  """

  text=requests.get("http://125.218.212.151:8081/book/search/engine?query=%s&page=1" %book).json()
  items=[]
  for i in text['data'][:10]:
    try:
      news={}
      news['title']=i['title']
      news['description']='\n'.join(i['position'])
      news['picurl']=i['image']
      news['url']=i['url']
      items.append(news)
    except:
      pass

  return items
