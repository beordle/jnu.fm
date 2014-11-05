import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def add_bind(wxid,stuid,cardpw,jwcpw):
    r.hdel(wxid,'stuid')
    r.hdel(wxid,'cardpw')
    r.hdel(wxid,'jwcpw')
    r.hset(wxid,'stuid',stuid)
    r.hset(wxid,'cardpw',cardpw)
    r.hset(wxid,'jwcpw',jwcpw)

def get_info(wxid):
    return r.hgetall(wxid)