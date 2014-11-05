#coding:utf-8

import requests
#http://127.0.0.1/auth_jwc?token=1375102913887b5d2d70a86ca07cb58fb410f6a7dcbeordle2&jwc_password=143217&jwc_username=2012052691

url="http://127.0.0.1:8081/login?username=beordle2&password=27622223"
r = requests.get(url)
print r.text
token=r.json()['token']

files = {'file': open('favicon.ico', 'rb')}
url="http://127.0.0.1:8081/set_avatar?token=%s" %token
r = requests.post(url, files=files)
print r.text

url=u"http://127.0.0.1:8081/set_info?token=%s&nickname=栋栋&realname=张金栋&sex=1&signature=试试看" %token
r = requests.post(url)
print r.text

url="http://127.0.0.1:8081/get_info?token=%s&username=beordle2"
r = requests.post(url)
print r.text


"http://127.0.0.1/static/avatar/beordle2.png"
