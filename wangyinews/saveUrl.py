import redis
import json


class urlDB():
    '''
    使用redis缓存构造urlDB，存放5种状态
    1.待爬取url,存入db1
    1.爬取成功url，2.永久失效的url，3.正在下载url,4.下载失败要再次下载url
    其中1,2两种状态要存入数据库，
    set_suc(url) 存储url状态为1
    set_fail(url) 存储url状态为2
    set_downing(url) 存储url状态为3
    set_down_again(url) 存储url状态为4
    check(url) 查看某url的状态
    '''

    def __init__(self):
        self.pool0 = redis.ConnectionPool(
            host='127.0.0.1', port=6379, db=0, decode_responses=True)
        self.r0 = redis.Redis(connection_pool=self.pool0)
        self.key = '网易新闻urls'
        self.item_key = '详细新闻'

        self.status_suc = 1
        self.status_fail = 2
        self.status_downing = 3
        self.status_down_again = 4

    def len_(self,key):
        return self.r0.llen(key)


    def set_wait(self, url):
        try:
            url = json.dumps(url)
            self.r0.lpush(self.key, url)
            s = True
        except:
            s = False
        return s

    
    def get_wait(self):
        l = self.len_(self.key)
        if l != 0:
            try:
                url = self.r0.rpop(self.key)
                url = json.loads(url)
                return url
            except:
                return 'error'
        else:
            print('待爬取url为空')
            return False

    def save_item(self,data):
        try:
            data = json.dumps(data)
            self.r0.lpush(self.item_key, data)
            s = True
        except:
            s = False
        return s


    def set_suc(self, url):
        url = url.encode('utf-8')
        try:
            self.r0.set(url, self.status_suc)
            s = True
        except:
            s = False

        return s

    def set_fail(self, url):
        url = url.encode('utf-8')
        try:
            self.r0.set(url, self.status_fail)
            s = True
        except:
            s = False

        return s

    def check(self, url):
        url = url.encode('utf-8')
        try:
            status = self.r0.get(url)
            return status
        except:
            pass
        return False


if __name__ == "__main__":
    db = urlDB()
    url = 'http://baidu.com'
    db.set_suc(url)
    print(db.check(url))
