#coding:utf-8
from flask import Flask, jsonify, render_template, request,Blueprint
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin

import time
import urlparse
from pyquery.pyquery import PyQuery as pq
import requests


def getzhlib(value):

  a={
  'v_index':'TITLE',
  'v_value':'python',
  'v_pagenum':'10',
  }
  a['v_value']=value.encode('gbk')
  text= requests.post("http://202.116.24.97/cgi-bin/IlaswebBib",data=a).content

  text=text.decode('gbk')
  book_list=[]
  aa=pq(text)
  img_count=0
  for i in aa('div>table>tr'):
     line=[pq(i).html() for i in pq(i)("td")]
     title=pq(line[0]).html()
     if title==u"题名":
        continue
     author=pq(line[1]).html()
     publish=pq(line[2]).html()
     page=pq(line[3]).html()
     rate=pq(line[4]).html()
     bookid=pq(line[5]).html()

     url=pq(line[6])('a').attr('href')

     if url!=None and img_count<5 :

       u=url= urlparse.urljoin("http://202.116.24.97/cgi-bin/IlaswebBib?",url)

       text=requests.get(u).content.decode('gbk')
       for i in pq(text)('div>table>tr'):
            #print pq(i).html().replace(u'\xa0','')
            if 'isbn' not in locals() and pq(i)('input[name=ISBN]').attr('value')!=None:
               img_count+=1
               isbn= pq(i)('input[name=ISBN]').attr('value')
               img= "http://book.bookday.cn/book/cover?isbn=%s&w=67&h=97" %isbn

     d={}
     if 'isbn' in locals():
      d['isbn']=isbn
      d['image']=img
     else:
      d['isbn']=""
      d['image']=""
     d['url']=url
     d['title']=title
     d['publish']=publish
     d['position']=[bookid]
     book_list.append(d)
     try:
      del isbn
     except:
      pass
  return book_list

#print getzhlib(u'三国')

import re
import gc
index = Blueprint('book', __name__,template_folder='templates',static_folder='static')
@index.route('/search/<search_string>', methods=['GET', 'POST'])
def get_books(search_string):
    gc.disable()
    s = requests.session()
    search_string = request.args.get('query', search_string)
    page = request.args.get('page', '1')
    need_limit= request.args.get('available', '0')
    need_limit = int(need_limit)
    iszh = request.args.get('iszh', '0')

    if iszh=="1":
       book_list=getzhlib(search_string)
       return jsonify(version=1.0, data=book_list)

    #r = s.get("http://202.116.13.244/search*chx/X?SEARCH=%s&SORT=D" % search_string)
    page=1+(int(page)-1)*12

    availble_limit=["","availlim/"]
    r = s.get("http://202.116.13.244/%ssearch~S1*chx?/X(%s)&SORT=D/X(%s)&SORT=D&SUBKEY=(%s)/%s,40,40,B/browse" % (availble_limit[need_limit],search_string,search_string,search_string,page))
    import time
    t=time.time()
    # print r.text
    # print chardet.detect(r.text) ascii
    soup = BeautifulSoup(unicode(r.text))
    total_list = []
    for tot in soup.findAll('td', {'class': "briefCitRow"}):
        dic = {}
        # print i.encode("gbk")
        left = tot.find("td", {'align': "left", 'class': "briefcitDetail"})
        dic['position'] = []
        can=0
        exist=0

        s="""<td align="left" class="briefcitDetail">
<!--{nohitmsg}-->
<span class="briefcitTitle">
<a href="/search~S1*chx?/X(df)&SORT=D/X(df)&SORT=D&SUBKEY=(df)/1%2C11%2C11%2CB/frameset&FF=X(df)&SORT=D&11%2C11%2C">狼のブルース
<br/>
 / 五木寛之著&nbsp; &nbsp;
東京 : 講談社, 1970.4&nbsp; &nbsp;
268p ; 19cm<!--
<div>
1970</div>
-->
<br/>
"""     

        try:
            text=re.findall('<span class="briefcitTitle">(.*?)<br/>(.*?)-->',unicode(left),re.S)[0][1]
        except:
            text=""

        for i in left.findAll("tr", {'class': "bibItemsEntry"}):
            str = ""
            for tr in i.findAll('td'):
                if tr.find('a') != None:
                    str += tr.find('a').text + " "
                else:
                    str += tr.text.split('-->')[0].split(u'\xa0')[1]
                    if str.find(u"在架上")>=0:
                        can=1
                    if str.find(u"在架上") or str.find(u"馆内阅览") >=0:
                        exist=1
            dic['position'].append(str)
        dic['detail'] = left.findAll("div", {'class': "briefcitItems"})[1].text
        dic['checkout']=can
        dic['lookup']=exist

        temp=text.split('\n')


        ["",    
" / 于雷等编著   ",
"北京 : 机械工业出版社, 2012.01   ",
"197页 : 图 ; 21cm<!--",
"<div>",
"2012</div>",
""]
        try:
            author=temp[1].replace(r"/ ","")
            publish=temp[2].replace("\u00a0","")
            size=temp[3].replace("<!--","")
            year=temp[5].split("<")[0]
            dic['author']=author
            dic['publish']=publish
            dic['size']=size
            dic['year']=year
        except:
            pass
        dic['url'] = left.find("span", {'class': "briefcitTitle"}).find("a")['href']
        dic['url'] = urljoin("http://202.116.13.244/search*chx/", dic['url'])
        dic['title'] = left.find("span", {'class': "briefcitTitle"}).find("a").text
        dic['status'] = left.find("span", {'class': "briefcitStatus"}).text
        # print dic['intro']
        try:
            dic['image'] = tot.findAll("td", {'align': "center"})[1].find("img")['src']
            isbn=dic['image'].split("=")[1].split("&")[0]
            dic['isbn']=isbn
            dic['image']= "http://book.bookday.cn/book/cover?isbn=%s&w=67&h=97" %(isbn)
            dic['douban']="http://book.douban.com/isbn/%s/" %(isbn)

        except:
            pass
        total_list.append(dic)
    #print time.time()-t
    gc.enable()
    return jsonify(version=1.0, data=total_list)
