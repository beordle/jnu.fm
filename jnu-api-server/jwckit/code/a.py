import Image,requests,StringIO,hashlib
def get_image():
  image_list=[]
  con=requests.get("http://jwc.jnu.edu.cn/web/ValidateCode.aspx").content
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



tot=[]
for i in range(10000):
    print i
    l=get_image()
    tot.extend(l)
lite={}
for index,i in enumerate(tot):
  key=hashlib.md5(i.tostring()).hexdigest()
  lite[key]=i
  #i.save(str(index)+".png")
print len(lite.keys()),len(tot)
for index,(key,i) in enumerate(lite.items()):
  i.save(str(index)+".png")
exit()

sizex,sizey=im.size
for y in range(sizey):  
      for x in range(sizex):  
          im2.putpixel((x,y), im1.getpixel((x,y)) ^ im2.getpixel((x,y)))  
      im2.show()  
print "ss"
