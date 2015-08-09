#coding:utf-8
import Image,requests,StringIO,hashlib,glob,gc
#性能优化版
#!!!!性能提升5倍!!!
['_Image__transformer', '__doc__', '__getattr__', '__init__', '__module__',
   '__repr__', '_copy', '_dump', '_expand', '_makeself', '_new', 'category', 'convert',
 'copy', 'crop', 'draft', 'filter', 'format', 'format_description', 'fromstring',
  'getbands', 'getbbox', 'getcolors', 'getdata', 'getextrema', 'getim', 'getpalette', 
  'getpixel', 'getprojection', 'histogram', 'im', 'info', 'load', 'mode', 'offset', 
  'palette', 'paste', 'point', 'putalpha', 'putdata', 'putpalette', 'putpixel', 
  'quantize', 'readonly', 'resize', 'rotate', 'save', 'seek', 'show', 'size'
, 'split', 'tell', 'thumbnail', 'tobitmap', 'tostring', 'transform', 'transpose'
, 'verify']


def cacl_like(char_image,each_row_image):
  
  each_row_image2 = each_row_image.load()
  char_image2=char_image.temp
  #计算图片的匹配度
  total=0.00

  white_point=0
  for x in range(char_image.size[0]):  

      black_line=0
      for y in range(char_image.size[1]): 
                #if char_image.getpixel((x,y))==0:
                if char_image2[x,y]==0:
                  black_line+=1

                if char_image.size[1]-black_line==0:
                  return 1

                if char_image2[x,y]==255:
                #if char_image.getpixel((x,y))==255:
                    white_point+=1
                #total += char_image.getpixel((x,y)) ^ each_row_image.getpixel((x,y))
                total += char_image2[x,y] ^ each_row_image2[x,y]
                # temp.putpixel( (x,y),  mask.getpixel((x,y)) ^ im.getpixel((x,y)))

  return (total/255) / white_point


def get_char_map():
  #读取字模
  mask_map={}
  for i in glob.glob("*.png"):
   if not i=='raw.png':


    mask= Image.open(i).convert('1')

    mask=mask.crop((0, 3, mask.size[0], 19)) #性能优化
    char_name=i.split(".")[0][:1]
    #print char_name
    mask2 = mask.load()
    mask.temp=mask2
    mask_map[char_name]=mask

  return mask_map
 
def get_image(png,mask_map):
  source_image = Image.open(png)
  source_image.save('raw.png')
  source_image_gray = source_image.convert('L')
  source_image2=source_image.load()
  source_image_gray2=source_image_gray.load()
  #将红色更换为黑色，其他颜色均为白色
  for y in range(source_image.size[1]):  
      for x in range(source_image.size[0]): 

        """
        if source_image.getpixel((x,y))[0] >210 and source_image.getpixel((x,y))[1] <140:
             source_image_gray.putpixel((x,y),255)
        else:
             source_image_gray.putpixel((x,y),0)
  """
        if source_image2[x,y][0] >210 and source_image2[x,y][1] <140:
             source_image_gray2[x,y]=255
        else:
             source_image_gray2[x,y]=0
  source_image_gray.save("processed.png")

  #转化为黑白图片
  blackwhite_image = source_image_gray.convert('1')



  total_char_match_list=[]
  #一直记录当前最most 的匹配的 位置，字符，匹配度,但是只保留4个
  
  for char_name,char_image in mask_map.items():
      char_width=char_image.size[0]
      blackwhite_image_width=blackwhite_image.size[0]
      #each_char_match_list=[]
      for x in range(blackwhite_image_width):
          if x>0 and x + char_width< blackwhite_image_width: #性能优化
            each_row_image=blackwhite_image.crop((x, 3, x + char_width, 19)) 
            num=cacl_like(char_image,each_row_image)
            total_char_match_list.append ( [num,x,char_name])
  total_char_match_list.sort()

  four_char_match_list=total_char_match_list
  four_char_match_list=[ (num,x,char_name) for  num,x,char_name in  four_char_match_list if num<0.6]


  dic={}
  for num,x,char_name in  four_char_match_list:
      if dic.has_key(x):

        if dic[x][0]>num:
          dic[x]=[num,x,char_name]
      else:
        dic[x]=[num,x,char_name]
  four_char_match_list=dic.values()
  #print u'经过除重处理'
  #m 和n 靠得 很近。 那么肯定只有m的
  #print four_char_match_list
  four_char_match_list.sort()
  four_char_match_list=four_char_match_list[:4]
  four_char_match_list=[ (x,num,char_name) for  num,x,char_name in  four_char_match_list if num<0.48]
  

  four_char_match_list.sort()
  char_list=[char_name for num,x,char_name in four_char_match_list]

  char_string="".join(char_list)
  return char_string


import time



#con=requests.get("http://jwc.jnu.edu.cn/web/ValidateCode.aspx").content
#source_image = StringIO.StringIO(con)


source_image='raw.png'

mask_map=get_char_map()
gc.disable()
t=time.time()
print get_image(source_image,mask_map)
print time.time()-t
gc.enable()
