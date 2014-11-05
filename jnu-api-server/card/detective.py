import Image
import requests,StringIO,hashlib
def get_image(s):
  image_list=[]
  con=s.get("http://card.jnu.edu.cn:8080/getpasswdPhoto.action").content
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
  #out.save('full.jpg')
  l=[]
  for n in range(4):
    for m in range(3):
      t=out.crop((10+36*m,36+36*n,10+23+36*m,36+23+36*n))
      #print n,m
      #t.save(str(n)+str(m)+".png")
      l.append(hashlib.md5(t.tostring()).hexdigest())
  return l

def mix_password(s,password):
  l=get_image(s)
  #print l
  k={'a22bcf7d39d13ca59f3c8396e7eb89db': '4', '60d6fa3d848c9fc74347c3d7c9e86d5c': '0', '3c80aa2efb76384843ce7828ee08a318': 'C', '61e5b4a8285973cb33be84ac78f5b530': '8', '790f3dc990ffc97e56a73771d16528f7': 'X', 'e8fd364d0205838ed1600c5a6b23dbb5': '1', '9421f03c799a7ae78f73726b52df1d36': '5', '0a3ba0c5b9586e8cf5ef848746ee587b': '6', '12c0e7d2f6a6a3f7d8de8cb8f9072112': '7', '2e5103732bd2fa2f86498da3d655e1cc': '2', '53b333cb4bd0960591b696fb2cce5d44': '9', 'f46fac15712d87d3409ae0ffd7acd81d': '3'}

  new_l=['0','1','2','3','4','5','6','7','8','9','C','X']

  l=map(lambda x: k[x],l)

  #{'C': 'C', 'X': 'X', '1': '2', '0': '7', '3': '0', '2': '6', '5': '1', '4': '4', '7': '8', '6': '9', '9': '5', '8': '3'}
  keys_map=dict(zip(l,new_l))
  keys_map_function=lambda x:keys_map[x]
  return  "".join  ( map(keys_map_function,password)  )

def normal_data(data):
  new_data={}
  for k,v in data.items():
     if type(v) is type([]):
         new_data[k]=v[0]
     else:
         new_data[k]=v
  return new_data