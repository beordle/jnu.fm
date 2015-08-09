#coding:utf-8
import requests
import time
import random

def sendsms(phone,msg):
    s=requests.session()

    headers={'Accept':'*/*',
    'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Host':'202.116.13.7',
    'Pragma':'no-cache',
    'Referer':'http://202.116.13.244/search~S1*chx?/ca5/ca5/1%2C254%2C254%2CE/frameset&FF=ca56+53+20121&1%2C1%2C/indexsort=r',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17',
    }

    json=s.get("http://202.116.13.7/ssms/servlet/SendSMS?jsoncallback=call&mobile=%s&msg=%s" %(phone,msg),headers=headers).text
    
    def call(msg):
       print msg['msg'].decode('utf-8')
       assert msg['msg']==u"短信发送成功。".encode('utf-8')
    eval(json)



def sendsmsex(phone,msg):
  print msg[:70]
  sendsms(phone,msg[:70])
  time.sleep(4)
  if len(msg)<=70:
     return
  else:
     sendsmsex(phone,msg[70:])


#重写
def sendsmsex(phone,msg):
  print msg[:70]
  sendsms(phone,msg[:70])
  time.sleep(4)
  if len(msg)<=70:
     return
  else:
     sendsmsex(phone,msg[70:])



if __name__=='__main__':

  phone="15625128341"
  text=u"""
  SMS模块加载测试
   """

  sendsmsex(phone,text)