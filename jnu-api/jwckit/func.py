#coding:utf-8
#from user.wraper import need_token,retry
import requests
from bs4 import BeautifulSoup
from det import get_text_from_image
from superprocessor import process_class_text2
from urlparse import urljoin
from pyquery import PyQuery as pq
#保证，一单符合就失败的,次数
#@retry([lambda x: x!="unkwon"],[lambda x: x=='password'],4)

def login(username, password):
        #所有请求均使用本headers 这两个字段对方均会检查
        headers = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                   "Referer": "http://jwc.jnu.edu.cn/web/login.aspx"}
        #创建一个浏览器会话
        s = requests.session()

        #发起GET请求
        html = s.get("http://jwc.jnu.edu.cn/web/login.aspx").text

        #解析页面验证码并完成初始化cookie工作
        soup = BeautifulSoup(html)
        # code = (soup.find('span', id='lblFJM').contents[0])#<span id="lblFJM'的正文为验证码
        dict = {}
        for i in soup.findAll("input"):  # 搜索表单,并填写
            if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'btnLogin'):
                dict[i['name']] = i['value'].encode('utf-8')

        #获取验证码，最多重试3次

        for i in range(10):
            #print i
            con = s.get("http://jwc.jnu.edu.cn/web/ValidateCode.aspx").content
            code = get_text_from_image(con)

            dict['txtFJM'] = code
            dict['txtYHBS'] = username
            dict['txtYHMM'] = password

            #发起POST
            length = s.post(
                "http://jwc.jnu.edu.cn/web/login.aspx",
                data=dict,
            ).headers['Content-Length']
            #print length
            #print 
            if length == "7819":
                return "password"
            if length == "1325":
                return s
            if length == '8792':
                continue
        return "unkwon"

#得到功课表文件
def get_person_teacher(s,xuehao):
    html = s.get("http://jwc.jnu.edu.cn/web/Secure/Xjgl/Xjgl_Zsgl_Xxcx.aspx").text
    soup = BeautifulSoup(html)
    dic = {}
    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'bthSearch'):
            dic[i['name']] = i['value'].encode('utf-8')
    dic['__EVENTTARGET']='lbtnQuery'
    dic['txtXH']=xuehao
    for i in ['txtND','ddListZSJJ','txtXZ','txtKSH','ddListPYCC','ddListSYLB','ddlGATQ','txtXM','ddlXQ','ddlXY','ddlDRFS']:
        dic[i]=""
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/Xjgl/Xjgl_Zsgl_Xxcx.aspx",
        data=dic
    ).text

    soup = BeautifulSoup(html)
    dic = {}
    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'bthSearch'):
            dic[i['name']] = i['value'].encode('utf-8')
    dic['__EVENTARGUMENT']='Select$0'
    dic['__EVENTTARGET']='GVJG'
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/Xjgl/Xjgl_Zsgl_Xxcx.aspx",
        data=dic
    ).text
    xingming= pq(html)('input#txtXM').attr['value']

    zhuangye= pq(html)('#ddlZY>option:selected').text()
    zhengjianleibie= pq(html)('#ddlZJLB>option:selected').text()
    zhengjianhao= pq(html)('input#txtZJH').attr['value']
    niandu= pq(html)('input#txtND').attr['value']
    chushengriqi= pq(html)('input#txtCSRQ').attr['value']
    guoji= pq(html)('input#txtGJ').attr['value']
    xingbie= pq(html)('#ddlXB>option:selected').text()
    
    return xingming,zhuangye,zhengjianleibie,zhengjianhao,chushengriqi,guoji,xingbie,niandu,xuehao

#得到功课表文件
def get_socre_teacher(s):
    html = s.get("http://jwc.jnu.edu.cn/web/Secure/Cjgl/Cjgl_Cjcx_Xscjlbcx.aspx").text
    soup = BeautifulSoup(html)
    dic = {}
    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'bthSearch'):
            dic[i['name']] = i['value'].encode('utf-8')
    dic['__EVENTTARGET']='lbtnQuery'
    dic['txtXH']='2012052690'
    for i in ['ddListZSJJ','txtXM','ddListXY','txtNJ']:
        dic[i]=""

    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/Cjgl/Cjgl_Cjcx_Xscjlbcx.aspx",
        data=dic
    ).text

    soup = BeautifulSoup(html)
    dic = {}
    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'bthSearch'):
            dic[i['name']] = i['value'].encode('utf-8')
    dic['__EVENTARGUMENT']='ZH$0'
    dic['__EVENTTARGET']='GVList'
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/Cjgl/Cjgl_Cjcx_Xscjlbcx.aspx",
        data=dic
    ).text
    html=pq(html)('table#GVListZH').html()
    return '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><table >'+html+'</table>'


#得到功课表文件
def get_xls(s, age, qx):
    #提供简单的第一学期第二学期的包装，可以将POST的string数据 像这样qxl(1) qxl(2)调用
    qxl = ['', '', '']
    qxl[1] = u"第一学期".encode('gbk')
    qxl[2] = u"第二学期".encode('gbk')

    html = s.get("http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_XK_MainCX.aspx").text
    soup = BeautifulSoup(html)
    dic = {}

    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION', 'bthSearch'):
            dic[i['name']] = i['value'].encode('utf-8')
    dic['dlstXndZ0'] = dic['dlstXndZ'] = str(age) + "-" + str(age + 1)
    dic['dlstNdxq'] = dic['dlstNdxq0'] = qxl[qx]
    #发起POST请求
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_XK_MainCX.aspx",
        data=dic
    ).text
    #原页面为多级iframe嵌套，所以这里可能难于理解
    a=BeautifulSoup(html).find('table').findAll("tr",{"class":"DGItemStyle"})
    b=BeautifulSoup(html).find('table').findAll("tr",{"class":"DGAlternatingItemStyle"})
    a=a+b
    ret={}
    for i in a:
        key=['class','id','name','score','???','type','时间安排','teacher','position','more','阶段','考试时间']
        value=["".join([i for i in j.contents[0] if i!=u'\xa0']) for j in  i.findAll("td")]
        imap=dict(zip(key,value))
        ret[imap['id']]=imap
    for key in ret.keys():
        string=ret[key]['时间安排']
        string2=ret[key]['position']
        del ret[key]['时间安排']
        del ret[key]['阶段']
        del ret[key]['考试时间']
        del ret[key]['???']

        ret[key]['time']=process_class_text2(string,string2)
    return ret




def get_kaoshi(s, age, qx):
    #提供简单的第一学期第二学期的包装，可以将POST的string数据 像这样qxl(1) qxl(2)调用
    qxl = ['', '', '']
    qxl[1] = u"第一学期".encode('gbk')
    qxl[2] = u"第二学期".encode('gbk')

    html = s.get("http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx").text
    soup = BeautifulSoup(html)
    dict1 = {}

    #搜索表单并填写
    for i in soup.findAll("input"):
        if  i['name'] in ('__VIEWSTATE', '__EVENTVALIDATION'):
            dict1[i['name']] = i['value'].encode('utf-8')
    dict1["btnExpKsb"] = u"导出或打印考试安排表".encode('gbk')
    dict1['dlstXndZ0'] = dict1['dlstXndZ'] = str(age) + "-" + str(age + 1)
    dict1['dlstNdxq'] = dict1['dlstNdxq0'] = qxl[qx]
    #发起POST请求
    html = s.post(
        "http://jwc.jnu.edu.cn/web/Secure/PaiKeXuanKe/wfrm_xk_StudentKcb.aspx",
        data=dict1
    ).text
    #原页面为多级iframe嵌套，所以这里可能难于理解

    nexturl = urljoin("http://jwc.jnu.edu.cn", BeautifulSoup(html).find('iframe')['src'])
    soup = BeautifulSoup(s.get(nexturl).text)
    #其中第二个iframe是我们需要的，但是他不是iframe标签，没有i
    nexturl = urljoin("http://jwc.jnu.edu.cn", soup.findAll('frame')[1]['src'])
    html = s.get(nexturl).text
    sum = ""
    dic = {}
    import re
    ff = re.findall(r'<DIV class="r11">(.*?)</DIV>', html, re.S)
    data = []
    for i in ff:
        sum = ""

        for j in i:
            if ord(j) != 13:
                sum += j

        if sum.find(u'课程') > 0:
            for temp in [i for index, i in enumerate(sum.split(u'考试'))][1:]:
                l = [i for i in temp.split(' ')]
                
                def ss(aspx):
                    try:
                        aspx = aspx.split(u"：")[1]
                    except:
                        aspx=aspx
                    return aspx

                l=[ss(aspx)for aspx in l]
                try:
                    date, time, place, name = l
                except:
                    pass
                r = {}
                r['date'], r['time'], r['place'], r['name'],r['socre'] = date, time, place, name, 0
                r['name'],r['id']= '('.join( name.rsplit("(")[:-1] ),name.rsplit("(")[-1][:-1]
                start,end=time.split("-")
                r['time-start'],r['time-end']=start,end
                data.append(r)
    return data

def get_info(s):
    html = s.get('http://jwc.jnu.edu.cn/web/Secure/Xjgl/Xjgl_Xsxxgl_Xjxxxg_XS.aspx').text
    soup = BeautifulSoup(html)
    str = ""
    data={}
    for i in soup.findAll("input"):
        if  i.has_key('id'):
            id=i['id']
            mapping=dict(
                txtXM_X='xingming',
                txtXQ='xiaoqu',
                txtKSH_X='kaoshengzheng',
                txtXY_X='xueyuan',
                txtPYCC_X='peiyang',
                txtSYLB_X='leibie',
                txtNJ_X='ruxuenianfen',
                txtMZ_X='minzu',
                txtZZMM_X='zhengzhi',
                txtCSRQ='chushengriqi',
                txtSYSZD_X='shengyuan',
                txtZY_X='zhuanye',
                txtJTZZ_X='jiatingzhuzhi',
                txtSFZH_X='shenfenzheng',
                txtGJ_X='guoji',
                txtXB_X='xingbie',
                txtCSRQ_X='chushengriqi',
                )

            j=i.get('value', '').replace(" ", "")
            try:
                if j!="" and id in mapping.keys() and not id in ['__VIEWSTATE','__EVENTVALIDATION']:
                    data[ mapping[id] ] = j
            except:
                pass
    return data
#login('2012052690','143217')