#coding:utf-8 
import requests
import urlparse
from sendemail import sendemail
from pyquery import PyQuery as pq
from detective import mix_password,normal_data
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from sms import sendsmsex
import time
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
  'inputEndDate':'20130531',
  'inputStartDate':'20130501',
  }
  data.update(idata)


  text=func(url,data=data).text
  func,url,data=auto_form(url,text,r)
  text=func(url,data=data).text
  func,url,data= auto_form("http://card.jnu.edu.cn:8080",text,r)
  months_list=[]
  for i in pq(text)(".listbg , .listbg2 "):
    colums=[pq(j).text() for j in pq(i)("td")]
    months_list.append([colums[1],colums[2],colums[3],colums[4],parse(colums[0])])#+relativedelta(minutes=+55)])
  return months_list




def today_data(r):
  text=r.get("http://card.jnu.edu.cn:8080/accounttodayTrjn.action").text
  func,url,data= auto_form("http://card.jnu.edu.cn:8080",text,r)
  text=func(url,data=normal_data(data)).text
  today_list=[]
  for i in pq(text)(".listbg , .listbg2 "):
    colums=[pq(j).text() for j in pq(i)("td")]
    today_list.append([colums[1],colums[2],colums[3],colums[4],parse(colums[0])    ])#    +relativedelta(minutes=+55)])
  return today_list

def person_data(r):
  text=r.get('http://card.jnu.edu.cn:8080/accountcardUser.action').text
  s=[]
  for i in pq(text)("td.neiwen"):
     s.append( pq(i).text().replace(u'\xa0', u' ')  )
  return s


def rest_data(r):
  s=person_data(r)
  for i in s:
    if i.find(u'余额')>=0:
      return i.split(u'元')[0]
"""
for stui in range(2012050168,2012059999):
  stuid=str(stui)
  print stuid
  f=open(stuid + '.txt',"w")
  try:
    r=login(stuid)
    dd=person_data(r)
    for k in dd:
       print >>f, k.encode('gbk')

  except:
    pass
  f.close()
exit()
"""

last_num=0
stuid="2012050167"
phone="15625128341"



r=login(stuid)
l=months_data(r)
for k in person_data(r):
   print k

for i in l:
  for j in i:
    print j,
  print 
while not time.sleep(1):
  try:

    r=login(stuid)
    
    l=today_data(r)
    #print 'local times',last_num,',live times',len(l),
    print l
    if not last_num==len(l):
      #print
      for i in l:
          for k in i:
            print k,
          print 
      last_num=len(l)
      print l[-1:]
      text=l[-1:][0][1]+", "+l[-1:][0][2]+', '+str(l[-1:][0][4])
      #sendsmsex(phone,text)
      sendemail(text)
  except:
    pass

for i in months_data(r):
  print i



