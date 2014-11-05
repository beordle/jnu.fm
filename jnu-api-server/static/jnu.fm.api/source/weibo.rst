上传用户头像
===============

请GET http://api.jnu.fm/uploader/image?token=1363368071c548598745d4b2b6b3dd7ce908e67766beordle
请POST http://api.jnu.fm/uploader/image?token=1363368071c548598745d4b2b6b3dd7ce908e67766beordle
模拟文件上传

查看指定用户发送的微博
----------------
http://api.jnu.fm/weibo/view?username=beordle&limit=20



查看指定频道发送的微博
----------------
http://api.jnu.fm/weibo/view?fm=schoolinfo&limit=20

评论指定id的微博 
----------------
http://api.jnu.fm/weibo/review?id=12&text=测试评论&token=


token无效返回
Token not pass


发送一条微博
----------------
http://api.jnu.fm/weibo/send

参数释义
* token
* text 正文
* ext 额外附加的信息。一般不用于显示 
* [fm] 发送到指定频道

demo http://api.jnu.fm/weibo/send?text=真心需要找到我的ip5 @12345&token=&fm=失物招领&ext=已找到,本部


.. 笑死::

  @index.route('/search/<search_string>', methods=['GET', 'POST'])
  def get_books(search_string):
      s = requests.session()
      search_string = request.args.get('query', search_string)
      page = request.args.get('page', '1')
      #r = s.get("http://202.116.13.244/search*chx/X?SEARCH=%s&SORT=D" % search_string)
      page=1+(int(page)-1)*12
      r = s.get("http://202.116.13.244/search~S1*chx?/X(%s)&SORT=D/X(%s)&SORT=D&SUBKEY=(%s)/%s,999,999,B/browse" % (search_string,search_string,search_string,page))

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

sdf

