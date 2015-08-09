#coding:utf-8
from flask import Flask, jsonify, render_template, request,Blueprint

from token import getUsernameFromToken
from functools import wraps
from random import random
from random import random

from functools import wraps
def retry(lamada_and,error,max_retry_times):

   def try_inline(func):
        @wraps (func)
        def wrap_func(*wrap):

           retry_times=0
           while retry_times<max_retry_times:
                retry_times+=1
                return_value = func(*wrap)

                for i in error:
                    if i(return_value)==True:
                       assert False,u"密码不正确"

                for i in lamada_and:
                  if i(return_value)==False:
                       break
                else:
                      #print "ok",retry_times
                      return return_value


           else:
             #print "fail",retry_times
             assert False,u"多次重试无果"

        return wrap_func
   return try_inline


def need_token(func):
        @wraps(func)
        def wrap_func(**wrap):
           token=request.args['token']
           username=getUsernameFromToken(token)
           if username:
                return func(username=username,**wrap)
           else:
                return "Token not pass"

        return wrap_func



