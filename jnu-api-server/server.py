#!/usr/bin/python

import os
import sys



port=8081
if len(sys.argv)>1:
 port=  int ( sys.argv[1]  )
os.system("title jnu.fm on %s" %port)

print "loading moudule..."
from gevent import monkey
monkey.patch_all()
from app import app
from gevent.pywsgi import WSGIServer
import gevent
from werkzeug.serving import run_with_reloader

from werkzeug.debug import DebuggedApplication

print "starting server..."
app.debug=True

#app=DebuggedApplication(app)
http_server = WSGIServer(( '0.0.0.0', port ), app)
http_server.serve_forever()
