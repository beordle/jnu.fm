import Image,requests,StringIO,hashlib

def get_image(con):
  image_list=[]
  im = Image.open(StringIO.StringIO(con))
  imgry = im.convert('L')

  threshold = 118
  table = []
  for i in range(256):
      if i < threshold:
          table.append(0)
      else:
          table.append(1)

  out = imgry.point(table,'1')
  #image_list.append(out)
  im=out
  sizex,sizey=im.size
  
  list=[]
  for y in range(sizey):
      for x in range(sizex):
           if not im.getpixel((x,y))==1:
             
             break
      else:
          list.append(y)
          
  length=set(range(sizey))-set(list)
  top=min(length)
  bottom=max(length)
  
  #print top,bottom

  list=[]
  for x in range(sizex):   
      for y in range(sizey):
        try:
           assert im.getpixel((x,y))==1
        except:
           break
      else:
           list.append(x)
  #for i in list:
  #  print i
  for index,element in enumerate(list):
    try:
      if element-list[index-1]>2 and list[index-1]>0:
        s=im.crop((list[index-1],top,element,bottom+1))
        #print list[index-1],top,element,bottom
        image_list.append(s)
    except:
      pass
  #im.save("test%s.png" %str(i)) 
  if not len(image_list)==4:
      return []
  return image_list




def get_text_from_image(con):
  lite={'271568e99d4248cec0912d31df7762b9': 'n', '1eadf3ed9e55d684e155020a669086aa': '7', '361ce7a35dab27ab8cacdbe2a49bd26a': 'u', '9efda163c6aaaec7d106ca5491e315d6': 'P', 'fcf1181754f3cf9a02705c846d3603f8': 'f', '1cda899da1f492ee80e8a8a803ca0b82': '5', 'dbfa84d3844bcffa5ec0aee37ba5306f': 'd', '5db8d608be66d4e060fd728c4e5c52aa': 'b', '6d02f63ef5e1d0091b0bbfd451fa872f': 'q', '6f3ca663fbf9651f995e1cefae7e21f2': 'w', '1d144c0beac5d25040714e5948bbd221': 'Z', '6352f1fb8303bf9e26f688f1c1fa6b46': 'A', '4d2e3b217105c9837dc8e77dfdfc8fc4': 'P', '170ecef18e782c7a1113dbc0e4470eb4': '0', '56f5b76c7efe9a268045a7d87ba82cb3': 'm', 'daf0b086bd6f18215d5f9ffc416fb252': 'g', '424a5acc758a012838ecc024871876f6': 'W', '1714c0e2f9a891effefe3105c7ee7cdf': 'z', '71e2c56ace093ae6f149b6a37f7833d9': 'M', 'ff3d18f33e9bcad62bffd92f6b144a65': 'C', 'a848813f92bff6ed8dcabcd713f87676': '3', '4d148d273c1d5b046ce0e0ac89bd0664': 'J', 'baf3e708792d81073fb2e046b8181b71': 'T', '55effec9b9f177a6488383392e2ed433': '8', 'ded396a8321f8000e8425fe2718458bf': 'R', '6241a6da2822d70d7e38de8d0d577baf': 'a', 'dd122f98c9998b83d74033e22b2f73dd': 'd', '3fdbeeb9a52d02414b0dd2e29637443d': 'n', '0361cf387f11685d58b329b03660bfd3': 'z', '9dcf8bc973418ae9e7c37c39b3ad466e': 'v', '9afd9a49cc3d9d7b7217c3e314424609': 'f', '560050ba9fa9ba2804092d64949fe60d': 'c', '0edee66fdf98b849901971a2900ed7e2': 'a', '17198a034996e08e50f9c44f9323132f': 'c', '3e053fd86bede41e5319502710d86c0c': 'a', '971d50ab368807ac32fc889009425eb4': 'j', '12a5d3bee253c037399011515bf07cbe': 'O', '4c849351c740cceb27bd954fd112b50b': 's', '80b1ded18daad3bc7121e41d4bab6b67': 'o', 'b8010d2290a6e55085d4e830ee51f89c': 'r', '0ee84f0e87c9bb17c0fefdb4dcb10258': 'w', 'b4b7759addffee95ec149b2b55c5553e': '1', 'bdcd6c8b3013c2811127bb8ebf92addc': 'b', '1e5ef98dba9224d9796dde2f10eecd3e': 'F', '3273d100cc96a2cd81cb181383cd55bf': 'w', 'c1bc959ac698c9d5de44ce9c1cb33c7b': 'S', '6cade99d8c658d60bf30ed32b74b2d67': 'Q', '7d83d012e0669e6577a654d39635e1a9': 's', 'd242195be334161ebdcf42a3801efa8b': 'D', '86d9d013bb418361e5c9122268663bdb': 'U', '9f9d9380b0a8dae06eec1452dae205e5': '5', '486dd2f1d28f8436fd2bc384c666e03a': 'x', '97e2f8696a4f6287866c32cc4ba8fdfd': '1', 'a517a77a39b9c14f1c0fdba4a7a16aa9': '4', '693d0124630365e54925db57527907f3': 'a', 'caba55decbbea51311810db7191c84ec': 'i', 'a0c96732f98e5ecc90055f0f3e63b751': 'a', 'aad0fa30f2b339abb954f1c533dd32a0': 'U', 'fd5504ccd8cb46cc78e72465d597c552': 'u', 'f603e02567b5c8fd3f4c027c3ce61b1f': 'x', 'b91332f5cc6c89f861c6ac3b76687a2d': 't', 'f7ece65bf906beea10baf84032b64068': 'r', '4718d48ec4bc8102af03141d76396d7f': 'g', '444fb1a86e99bf4f3f420efc6bea3fb4': 'K', 'f8a99d2308a3f70972eb408765dbc7a3': 'Y', '3d68293b762f878c5e3b47d5649622e2': 'V', '10add3a52433a5cafb8074b5df6d9c5b': 'z', 'f4afcd5b04b0203b409fb77e7d5516a0': 'a', 'e0166494916fe87c588018ffb2c0c082': '4', 'd052750bba4c1942a7bcd67a8a856d94': 'o', '2697a4e8ff36e59b7d272c2722ae799e': 'Y', '2cc2b33a3e77c64df860ef6ef6f3e522': 'N', '0768632125f7aaa3d8109d052d673336': 'v', '40b20fca678353db2c6e4a5993039b75': 'I', 'e4ae4f1d70647a007d358f4a92112be6': '9', 'c403633b9c3107913e2c6ecc42ee4f47': 'g', '7edba1b958cee88f425eb0eb4d061931': 'e', 'cbf6350c7a64ab135b027a0c606b907b': 'k', '8a2e2bb72b4848df9d058dbbfa36a530': 't', 'bd419291aa955c7c85298dfdbeb38784': '5', '3fb66b5b109f9cb1bfb13988391e207b': 'c', '8baca34a686d5075fff2998ac22d6129': 'h', '4a103a24e434597a233ca04291cbed4e': 'R', '58791d6ae93968965b7b622ce14412ea': 'S', 'c867ce173b0557b9c839e37d65abd194': '5', '9dcfdce61ee46351da8436722db2a843': 'J', '67563595d94cee45b83ec3a5bcc21661': 'O', '1b5da47ece6171c0123645cea1011828': 'e', '296597ce35d796e8d7a11efe4ba850f6': 'G', 'b7ae301faf03e6c222d69ce4956ffad3': 'I', '796cb110eaff92b559879a55ded05438': 'e', '393c3c642f8c9e86fe31d314c38e2cd0': 'e', '4e0fc23e2de4a57a8376874987c7bddc': '9', '22a03b3beb5858400ed91faef0a78eb8': 'Q', '757e42b093d1852528055f3265b6a25d': 'z', 'da33f4a42be934428948c965668a1e8f': 'v', '163fb6e6789f74c9832590c76767375c': 'V', '0a292db8008d2e086066589ffbb6d009': 'i', 'e652714e46370086c9a7c3868d86fa04': 'C', 'a1a41b293d52899dde0ecae7684f6455': 'w', '55053fa2bd3d77dcf265bcd1e99e3054': 'b', '44e1422d926af7a6cfdc822d696115b5': 's', 'a883ebb42b1dd73daed25a63736a00af': '1', '1a6852df89ae918633d50b4581318ab1': 'T', '7817982404fb181effc9f912b045c78d': 'H', 'ad564152eaa1c00ff029298824e671cd': 'K', '138c736e9048a6dde61d381df397875e': 'A', '70b8a80f00cc848077d5bab56f9c17e9': 'F', 'bac75ad97c8b6e4aeebe95d3f065151b': 'c', 'ab7d10c225cd39e0a247313be0144163': 'T', '2bbc8901a9ba01174f7b8448c6a4d1fa': 'G', '0ce15e872e1f2286a58c018dff71d27d': 'u', 'addaf98584e4b63bf0963d17e6157b9d': 'y', 'a27ee17051df2706f8f6d6028988f2fc': 'M', '2eb33020e0bbadde79a269bf3b2efe19': 'X', '911a18b3f6d6312c26042d8098a8d707': 'm', '45bd7756172fd7fd745429136aa24700': 'x', '2794052c5e9e97a65a6cf88ccca2c0dd': 'S', '65d0807a88df76d5b303db1126bc521e': 'r', '82f539da6280ad73f7520e0150d5d219': 'h', 'fd86a536384ccb17c338299a22c48cd5': 'B', '0e3aade06f21c71cc4e73a89d9131adc': 'm', '821464764f1dd39eb4d17691bb419c22': 't', '274ae567f51f1a0d0bdb2e6911b9eb83': 'N', 'e3a9868e7a1d9515d3454f625c512102': 'x', '01e8c3e79b367cd462d7fda1ed74318d': 'Y', 'c95cac89fcdb768ecd94dc887881d4b2': 'o', 'af2608530e4f72150dfa445094d6a877': '7', 'a0be1fbdfb4ad797f0ee8cecc81aa107': 'A', 'ad8efdbd4110e7f8d1739cdf10125dee': '2', 'e1c61e7c13d8df13a5c2a63a1b18cc02': 'v', '78ef8e25a2ea185e5bfe53a58ca73633': 'I', 'dfd0083f3933dbc8ea2547ebae4cb9d1': 'N', '492241f1f59aca6f44ced74addc23fe9': 'u', '9115576984cf5941cfa21b54b53d6452': 'W', 'fce09b10f975e9b3f895d3edf78535ec': 'e', '05200dc7a149ad17096649f64cfbcab7': '3', '6f81ce148c8295aca8385f42dd4e43a9': 'M', 'a1bb9db8c9b142038c6ee466db8320f6': 'Z', '2aab413a9a84195b8752c2cd50d711ea': '7', 'c111f905fee931de301da12b93c3e411': '6', '1420ea5a6306faf8a67d0492895a04b3': 'v', '2e876d1bfbe0aef834c4f17b4d2313cb': 'q', 'eec719f68c81cf49fedeb731fc2879d2': 'Z', '79d8348e9303d813d0366f8585bcdb67': 'E', '7a036ea5db0821441c6882d0dbc841a7': 'e', '872d5c96bd9501a9ca8916587d2c2aa3': 'h', '6c03ad64f5c9637edac401b4b2b4c426': '2', 'afbc8cb22420ff4006242b2cf846eeeb': 'O', '01cc0c0b02b20f1fcd969868d4a65798': 'k', 'bfab5a22c25577e44f3350550420943b': 'd', '894a715425581f186939ec2d0c0a16b7': 'K', '7e17df3bdb6ed3040fa71557e2fe83d0': '6', '161635c96368c62771b5eacb9c9a65aa': 'r', 'f9eaf3933d3ccb74c858747effa50ca4': 'w', '17979615bb6c3411f754459573c0bd3f': 'H', '72ae4168e7a44f51d38dc0310547325b': 'c', '77e773573e4b9c5dab1fe356c63cf6fe': 'n', '0fb6f17712c89172541e4a43b8f4e4eb': '0', 'f896793c5d76b8e0f30f194a99450c5e': 'B', '8c4697ccb0ccd823a29f997d8f0b5cec': '4', 'd50625fa827bc9d8881eaad8924ed758': 'U', 'a503f50631891d29f8a6eebe44d86f93': 't', '65071b4a664a4edca01996e4430b4f56': 'L', '82ccafcbf3f35c3a04c2b778483991d7': 'x', '0cd35a0500ccfaa6d31ea36b51871fd7': 'E', '457602316383869d5266bbfd913d0e75': 'B', '75c4d2298c62d0c8378113ad76a1a928': 'n', '0941678aa5f2a096267cd32fb08e1b69': 'V', '0bc3421229fce048677eebbc06c6075c': 'z', '59a28a8ce666711b18eae59489029abc': '2', 'cb749f0e3b7801901e0058a15ec19d77': 'z', 'd191b7c2eb9043a7f59f4c117a20444d': '9', 'a0c707823a5b12a9f19e577649ba98cb': '6', '27dd50cdb7e57a1eb4cee0487e98bcdb': 'o', '8c3916dbd409482d2e2138674958382a': 'H', '98220d373a6f30deffcf7d6d097373fb': '8', '52733908e9cbf5c3c0ddad1c50447203': 'X', '600ef160e726708d48e3b1ca33d2e765': 'k', '18ff339a624e27844c52875885ce7835': 'L', '03c9d2db96c6c41114cf7c9512779fbe': 'f', '2ea0197b1476135dd6780658d64602ae': 'J', 'd5acbc83354e8074efff659ad87c5a3d': 'i', '82da256b98fda989a266c50c850e6ba4': 'q', 'a93f74e3f93adc29a0b154238cf64c70': 'C', '2adc8d0e8a3c5c436a7b9f4fd7aca310': 'x', 'dd0c3af8a9912abead5944aaf8b1a893': 'm', '72ff91dbfef4b2c4dd681a419ea70cdf': '0', 'ad3f2c046bd2f8b6832ba3241dd8d23d': 'D', '7cb5c0d7b77c100416d22ff5fa5c5310': 'E', 'c42cb9648b62a8160ac5564568e5a3ca': 'r', '6aa804c5458f46405e62e2c4dd298cb1': 'o', 'c952a869bd795e35ce310f015d624f1e': 'v', '6bb6bc2c562a65ed3eaeaf159d0cc695': 'u', 'c7f169a6289e8c0e8ec4635a39de829e': 'y', '947c01234a9ba8edbeb4b71c476cc031': 'G', '3ce725ec44526cecca55d10fec7206e6': 'W', '67e12554156126378aab62c9946d27c4': '3', '1e28a1da8b8813bcc1dd4614a4c951d2': '8', '6096265bd96c1cb0e2515a68bab9fd59': 'x', '7c26fd2b67aa654d5a11da5cbdfc9722': 's', 'c5f6bde90b0deaf6eecf972caf849e51': 'P', '41f1e875b5467124fca6b69381fb5d18': 'u', 'a2dba95a6ce2f55a8795d9418f80c33b': 'r', 'd7762231599720ed1db6cba387fdcff6': 'm', 'bb6226ca77d30d14a0715f871aba10b2': 'P', '99ade5c8b3c6689561a5a636c6e5914d': 'n', 'd8e04f817e968e77f8d4de766810ea37': 'R', '0019b3e5688ce96fbe9c5168fe63a9ef': 't', 'cebbb5e747f563556f84356fbbcd7c15': 'n', '5272ab4df97d8b51cbfd67c3d553a53c': 'P', '04ebe2ee94d64dc457b06111f21ff601': 'o', '50d0c25e71fc36ae4d2d61cd31c90e85': 'F', 'cf90554a8d428852aebfc33a176ccae8': 'X', 'cdc540b02f94d0c71647e4d0a46e27d2': 'm', 'ead0df32e1cd41f041b12fc5a5149e0f': 's', '6d227deb45115938cfd83d2adbacb19b': 'D', '45a394a5493aee79a4df494109b8ade4': 'u', 'cff43d8dacec00656c4a75ca79450b11': 'L'}
  string=""
  l=get_image(con)
  for index,i in enumerate(l):
    key=hashlib.md5(i.tostring()).hexdigest()
    string+=lite[key]
  return string

con=requests.get("http://jwc.jnu.edu.cn/web/ValidateCode.aspx").content
print get_text_from_image(con)
