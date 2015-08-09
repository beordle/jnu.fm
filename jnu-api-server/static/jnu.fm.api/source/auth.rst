用户验证及信息同步
===============

注册
----------------

api.jnu.fm/auth?username=beordle&password=27622223&jwcid=2012052690&jwcpw=143217


* username 注册的用户名
* password 注册的密码
* jwcid 学生学号（可选，如不指定 jwcid 默认为 username）
* jwcpw 教务处密码

登陆
----------------

http://api.jnu.fm/auth?username=brdle&password=27622223

参数释义

* username 用户名
* password 密码

同步
----------------
获取服务器当前储存的用户数据

http://api.jnu.fm/sync?token=136249108911153f5bbb2851fc417cf126fdbb888fbrdle


更新服务器数据

http://api.jnu.fm/sync?token=136249108911153f5bbb2851fc417cf126fdbb888fbrdle

>token 登陆即可获得



返回值示例
----------------
{
status: "LoginSuccess",
token: "136249108911153f5bbb2851fc417cf126fdbb888fbrdle",
version: 1,
data: {
username: "brdle",
jwcid: "2012052690",
password: "27622223",
minzu: "汉族",
chushengriqi: "1994-03-14",
jiatingzhuzhi: "南开区渭水道3号",
shengyuan: "天津南开区",
xiaoqu: "校本部",
zhengzhi: "共青团员",
xueyuan: "国际学院",
xingming: "张金栋",
leibie: "内招生",
xingbie: "男",
ruxuenianfen: "2012",
guoji: "中华人民共和国",
peiyang: "本科",
zhuanye: "计算机科学与技术",
kaoshengzheng: "12120104951581",
shenfenzheng: "120104199403143217",
jwcpw: "143217"
}
}