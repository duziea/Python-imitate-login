import redis


class urlDB():
    '''
    使用redis缓存构造urlDB，存放4种状态
    1.爬取成功url，2.永久失效的url，3.正在下载url,4.下载失败要再次下载url
    set_suc(url) 存储url状态为1
    set_fail(url) 存储url状态为2
    set_downing(url) 存储url状态为3
    set_down_again(url) 存储url状态为4
    check(url) 查看某url的状态
    '''

    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,decode_responses=True)
        self.pool2 = redis.ConnectionPool(host='127.0.0.1',port=6379,db=1,decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)
        self.r2 = redis.Redis(connection_pool=self.pool2)
        self.status_suc = 1
        self.status_fail = 2
        self.status_downing = 3
        self.status_down_again = 4

    def set_suc(self,url):
        url = url.encode('utf-8')
        try:
            self.r.set(url,self.status_suc)
            s = True
        except:
            s = False

        return s

    def set_fail(self,url):
        url = url.encode('utf-8')
        try:
            self.r.set(url,self.status_fail)
            s = True
        except:
            s = False

        return s

    

    def check(self,url):
        url = url.encode('utf-8')
        try:
            status = self.r2.get(url)
            return status
        except:
            pass
        return False
            


if __name__ == "__main__":
    db = urlDB()
    url = 'http://baidu.com'
    db.set_suc(url)
    print(db.check(url))
