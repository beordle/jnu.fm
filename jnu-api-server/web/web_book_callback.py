
#coding:utf-8
import os
import base64

from flask import Flask, request, redirect, url_for,jsonify,Blueprint,render_template
from werkzeug import secure_filename

web = Blueprint('web', __name__,template_folder='templates',static_folder='static')
import requests
from bs4 import BeautifulSoup


def GenImageURL(data):
    return "data:image/gif;base64," + data.encode("base64")

mapd={
u'标准号':'isbn',
u'出版资料':'detail',
u'载体形态':'size',
}
def getbyurl(u="http://202.116.13.244/search~S1*chx?/Xd&searchscope=1&SORT=DZ/Xd&searchscope=1&SORT=DZ&SUBKEY=d/1%2C18445%2C18445%2CB/frameset&FF=Xd&searchscope=1&SORT=DZ&1%2C1%2C"):
  a={}
  k=False
  t=requests.get(u).text
  s=BeautifulSoup(t)
  tables=s.find('div',{'class':"pageContentColumn"}).findAll('table')
  qw=s.findAll('tr',{'class':"bibItemsEntry"})
  a['position']=""

  ss=s.find('span',id='douban').findAll('img')
  for i in ss:
    print i

  for j in qw:
    stri=""
    for i in j.findAll("td"):
         if i.find("a")!=None:
            stri+= i.find("a").contents[0]+"   "
         else:
            stri+= i.text.split('-->')[0].split(u'\xa0')[1]
    a['position']=stri+'<br>'+a['position']

  for table in tables:

    t=table.find('td',{'class':"bibInfoLabel"})
    if t!=None:
        a[t.contents[0]]=""
        f=table.findAll('td',{'class':"bibInfoData"})

        if t.contents[0]==u'出版资料':
            a[u'出版社']=f[0].text.replace("\n","")
        for i in f:
            if t.contents[0]==u'主要责任者':
                a[u'作者']=i.find('a').text.replace(",","")

            if i.find("strong")!=None and t.contents[0]==u'题名':
                print i.find("strong").text
                a['title']= i.find("strong").text
            if len(i.contents[0].replace(" ","")) > len(a[t.contents[0]]):
              a[t.contents[0]]=i.contents[0].replace("\n","")
  isbn=a[u'标准号'].split(" ")[0]

  url= "http://book.bookday.cn/book/cover?isbn=%s&w=100&h=150" %(isbn)
  a['img']=url
  #a['img']=GenImageURL(requests.get(url).content)
  return a

def getbyurl_zh(url):
  map_data={}
  import requests
  a=requests.get(url).content.decode('gbk')
  from pyquery.pyquery import PyQuery as pq
  rr={u"题　名":'title',
  u"页　码":u'载体形态',
  u"作　者":u'作者',
  u"出版项":u'出版社',
  "ISB":u'标准号',
  u"索取号":'position',
  u"附注信":u'载体形态'}
  for i in pq(a)("tr td"):
   print pq(i).text()[:3]
   if pq(i).text()[:3] in rr:
       map_data[   rr[ pq(i).text()[:3] ]  ]=  pq(i).text()[pq(i).text().index(":")+1:]
  map_data['img']= "http://book.bookday.cn/book/cover?isbn=%s&w=100&h=150"  %map_data[u'标准号']
  return map_data

def getbyurl2(url):
  if url.startswith("http://202.116.13.244"):
    return getbyurl(url)
  else:
    return getbyurl_zh(url)

@web.route('/book', methods=['GET', 'POST'])
def web2():

   url=request.args['url']
   url=base64.urlsafe_b64decode(str(url))
   dic=getbyurl2(url)
   return render_template("index2.html",**locals())

#dic=getbyurl()
#for i,j in dic.items():
#   print i,j

if __name__=='__main__':
   web.run(port=8080,debug=True)

