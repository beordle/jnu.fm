jnu.fm
======

暨南FM 是一個暨南大學校內微信公眾平台,這個 github 項目是JNU.FM 運營期間所衍生的項目

目前這個項目分為兩個獨立的部份

1.API伺服器. 一套針對學校教務處,校園卡中心,圖書館緊湊的API封裝
2.微信服務器. 與微信通信的 Server,會調用 API 伺服器

#對 API 伺服器的說明

jnu-api-server 下即是全部 api 伺服器的代碼.通過 server.py 啟動.啟動后將監聽8081端口.
##api 說明
>>搜索图书

http://server/book/search/engine?query=三国&page=2
参数释义
* query 搜索关键字 AND OR 等图书馆自带高级搜索功能
* page 页码


=====


>>使用学号及教务处密码直接获取课表

http://server/class/get?user=2012052690&password=143217&year=2012&term=2
参数释义
* user 学生学号
* password 教务处密码
* year=2012 课表年份  教务处对应 2012-2013
* term 学期 可选值 1:上学期 2:下学期


====

>>使用学号及教务处密码直接获取考试信息  

http://server/kaoshi/get?user=2012052690&password=143217&year=2012&term=2  
参数释义  
* user 学生学号  
* password 教务处密码    
* year=2012 课表年份  教务处对应 2012-2013  
* term 学期 可选值 1:上学期 2:下学期  



====

>>使用学号及校园卡密码获取今天消费记录(时间可能会有出入,未修复)

http://server/card/today?stuid=2012052691&password=052691
参数释义  
* studi 学生学号  
* password  校园卡密码    

====

>>使用学号及校园卡密码获取饭卡余额

http://server/card/rest?stuid=2012052691&password=052691
参数释义  
* stuid 学生学号  
* password  校园卡密码    



====

##設計
 test

##簡單測試 API
要测试 api 请使用 demo 服务器
将  http://server/ 替换为http://125.218.212.151:8081/ 即可

