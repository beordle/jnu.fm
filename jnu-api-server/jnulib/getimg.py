import requests
import Image
import StringIO
from flask import Flask, jsonify, render_template, request,Blueprint
index = Blueprint(__name__, __name__,template_folder='templates',static_folder='static')

def getimage(isbn):
  import requests
  import Image
  import StringIO
  outfile=StringIO.StringIO()
  x=requests.get("http://202.112.150.126/index.php?client=libcode&isbn=%s/cover" %isbn).content
  f=StringIO.StringIO(x)
  im = Image.open(f)

  im = im.resize((im.size[0]/4 ,im.size[1]/4) , Image.BILINEAR)
  im.save(outfile, "JPEG")
  s=outfile.getvalue()
  return s


@index.route('/image/<isbn>', methods=['GET', 'POST'])
def get_books(isbn):
    f=getimage(isbn)
    return f