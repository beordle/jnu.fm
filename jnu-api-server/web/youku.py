#coding:utf-8
import requests
import urlparse
import os
import base64
from flask import Flask, request, redirect, url_for,jsonify,Blueprint,render_template
from pyquery import PyQuery as pq
print 'loading ',__name__
web = Blueprint( __name__, __name__,template_folder='templates',static_folder='static')
r=requests.session()
@web.route('/preview', methods=['GET', 'POST'])
def video_img_handler3():
   url=request.args['url']
   url=base64.urlsafe_b64decode(str(url))
   return get_video_image(url)

@web.route('/view', methods=['GET', 'POST'])
def video_url_handler():

   url=request.args['url']
   url=base64.urlsafe_b64decode(str(url))
   return redirect (get_video_url(url))

@web.route('/video', methods=['GET', 'POST'])
def video_img_handler():
   query_string=request.args['query']
   return jsonify(data=youku_json(query_string))


def youku_json(query_string=u'钢铁侠'):
  try:
    a=r.get(u"http://m.youku.com/wap/searchlist?keyword=%s&pg=1" %query_string).text
  except:
    try:
      a=r.get(u"http://m.youku.com/wap/searchlist?keyword=%s&pg=1" %query_string).text
    except:
      pass
    a=r.get(u"http://m.youku.com/wap/searchlist?keyword=%s&pg=1" %query_string).text

  video_list=[]
  for i in pq(a)("li a"):
    url= urlparse.urljoin('http://m.youku.com/wap/searchlist?keyword=钢铁侠&pg=1',pq(i)[0].attrib['href'])
    name= pq(i)[0].text
    video_list.append({'url':url,'name':name})
  print video_list
  return video_list
  #break


def get_video_img(url):
  a=r.get(url).text

  #print pq(a)("div.playlink a").text

  try:
    img=pq(a)("img.imgdetail")[0].attrib['src']
    return img
  except:
    pass
  #  break
def get_video_image(url):
  url=get_video_img(url)
  img=requests.get(url).content
  return img



def get_video_url(url):
  a=r.get(url).text

  #print pq(a)("div.playlink a").text

  try:
    url=pq(a)("div.playlink a")[0].attrib['href']

    video_url=urlparse.urljoin('http://m.youku.com/wap/searchlist?keyword=钢铁侠&pg=1',url)
  except:
    pass
  return video_url

#url=video_list[1]['url']
#get_video_image(url)
#print get_video_url(url)
  #  break
