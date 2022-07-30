import redis
def download():
    r= redis.Redis(host="81.70.18.48",port =6379 ,db=0,password='1A958.e41693')
    result= r.smembers("all-magnet")
    print(result)
    return result

def upload(bad_magnet):
    r = redis.Redis(host="81.70.18.48", port=6379, db=0, password='1A958.e41693')
    bad_hash=bad_magnet[-20:]
    r.sadd("badhash", bad_hash)



