import Image,requests,StringIO,hashlib
def get_image():
  ['_Image__transformer', '__doc__', '__getattr__', '__init__', '__module__',
   '__repr__', '_copy', '_dump', '_expand', '_makeself', '_new', 'category', 'convert',
 'copy', 'crop', 'draft', 'filter', 'format', 'format_description', 'fromstring',
  'getbands', 'getbbox', 'getcolors', 'getdata', 'getextrema', 'getim', 'getpalette', 
  'getpixel', 'getprojection', 'histogram', 'im', 'info', 'load', 'mode', 'offset', 
  'palette', 'paste', 'point', 'putalpha', 'putdata', 'putpalette', 'putpixel', 
  'quantize', 'readonly', 'resize', 'rotate', 'save', 'seek', 'show', 'size'
, 'split', 'tell', 'thumbnail', 'tobitmap', 'tostring', 'transform', 'transpose'
, 'verify']

  image_list=[]
  con=requests.get("http://jwc.jnu.edu.cn/web/ValidateCode.aspx").content
  im = Image.open(StringIO.StringIO(con))
  im.save('raw.png')
  imgry = im.convert('L')
  imgry.save("dd.png")
  im3=im2=im
  sizeh,sizew=im.size  
  for y in range(sizew):  
      for x in range(sizeh): 
        im3=im.crop((x, y, x+10, y+10)) 
       # im3.save(str(x)+str(y)+".png")
        if im.getpixel((x,y)) == (105, 105, 105, 255):

            imgry.putpixel((x,y),255)
        else:
            imgry.putpixel((x,y),0)
            #imgry.putpixel(   (x,y),  im.getpixel((x,y)) ^ im.getpixel((x,y))  )
  imgry.save("dd2.png")

  for y in range(sizew):  
      for x in range(sizeh): 
        #if im.getpixel((x,y)) == (249, 31, 31, 255):
        if im.getpixel((x,y))[0] >210 and im.getpixel((x,y))[1] <140:
            imgry.putpixel((x,y),255)
        else:
            imgry.putpixel((x,y),0)
            #imgry.putpixel(   (x,y),  im.getpixel((x,y)) ^ im.getpixel((x,y))  )
  imgry.save("dd3.png")




get_image()
print "ss"
