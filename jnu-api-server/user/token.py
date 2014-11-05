# coding:utf-8
import os
import time
import hashlib
import urllib


def get_token(username="beordle"):

    def _get_token(username):
        #不同站点可使用不同密钥
        privatekey = "2324dsf34##4f$43etg4_3t5g?rt)u434"
        timea = str(int(time.time() + 24 * 60 * 60))  # 设置有效期为1天
        token = timea + hashlib.md5(timea + privatekey + username).hexdigest() + username
        return token
    return urllib.quote(_get_token(username))


def auth_token(token):
    def _auth_token(token):
        privatekey = "2324dsf34##4f$43etg4_3t5g?rt)u434"

        #长度验证
        strlen = len("1354975386609d045143db3cb3452aa57d42c9f3c6")
        assert len(token) > strlen  # 有用户名后必然大于只有时间+哈希的长度

        #数据还原并进行有效期验证
        timea = time.time()
        token_time = token[:10]
        token_hash = token[10:10 + 32]
        token_user = token[10 + 32:]
        avaible_time = int(token_time) - timea
        assert 0 < avaible_time < 3600 * 24  # 确保有效期小于一天这样才说明是本程序所生成并不过期
        assert token_hash == hashlib.md5(token_time + privatekey + token_user).hexdigest()
    try:
        _auth_token(token)
        return True
    except:
        return False


def get_username_from_authed_token(token):
    def _auth_token(token):
        privatekey = "2324dsf34##4f$43etg4_3t5g?rt)u434"

        #长度验证
        strlen = len("1354975386609d045143db3cb3452aa57d42c9f3c6")
        assert len(token) > strlen  # 有用户名后必然大于只有时间+哈希的长度

        #数据还原并进行有效期验证
        timea = time.time()
        token_time = token[:10]
        token_hash = token[10:10 + 32]
        token_user = token[10 + 32:]
        avaible_time = int(token_time) - timea
        assert 0 < avaible_time < 3600 * 24  # 确保有效期小于一天这样才说明是本程序所生成并不过期
        assert token_hash == hashlib.md5(token_time + privatekey + token_user).hexdigest()
        return token_user
    try:
        token_user = _auth_token(token)
        return token_user
    except:
        return False

get = get_token
auth = auth_token
getUsernameFromToken = get_username_from_authed_token
if __name__ == '__main__':
    token = get_token("rr")
    print auth_token(token)
