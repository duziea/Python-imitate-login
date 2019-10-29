# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import redis

class BasketballshoePipeline(object):
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class redisPipeline(object):
    def process_item(self,item,spider):
        '''
        连接池：
        当程序创建数据源实例时，系统会一次性创建多个数据库连接，并把这些数据库连接保存在连接池中，当程序需要进行数据库访问时，
        无需重新新建数据库连接，而是从连接池中取出一个空闲的数据库连接
        '''
        pool = redis.ConnectionPool(host='127.0.0.1',port=6379)   #实现一个连接池

        r = redis.Redis(connection_pool=pool)
        r.lpush('basketball',json.dumps(dict(item),ensure_ascii=False))
    