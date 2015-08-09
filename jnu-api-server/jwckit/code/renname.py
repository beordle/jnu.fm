import os,glob
l=list(glob.glob("*~*.png"))
for i in l:
  os.rename(i,i.split("~")[0]+".png")