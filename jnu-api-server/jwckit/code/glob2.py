import glob
import Image,hashlib

l=list(glob.glob("*.png"))
lite={}
for i in l:
  name=i.split(".")[0].split(" ")[0]
  i = Image.open(open(i,"rb"))
  key=hashlib.md5(i.tostring()).hexdigest()
  lite[key]=name
print lite