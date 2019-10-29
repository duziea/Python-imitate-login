# -*- coding: utf-8 -*-
import scrapy
import json
from jdbook.items import JdbookItem
from scrapy_redis.spiders import RedisSpider



class BookSpider(RedisSpider):
    name = 'book'
    allowed_domains = ['jd.com','p.3.cn']

    redis_key = 'book'

    def parse(self, response):
        #get first_category xpath selector list
        # fc_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        fc_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt[1]/a')
        for i in fc_list:
            # traverse first_category list ,get each first_category's name , url
            # and second_category list
            fc = i.xpath('./text()').get()
            sc_list = i.xpath('../following-sibling::dd[1]/em/a')
            # print(sub_list)
            for n in sc_list:
                # traverse second_category list,get each second_category's name,url
                info = {}
                info['first_category'] = fc
                info['second_category'] = n.xpath('./text()').get()
                info['second_category_url'] = 'https:' + n.xpath('./@href').get()
                # print(info)
            
                # yield request second_category_url, callback=self.parse_bookinfo ,
                # get each second_category's books info
                yield scrapy.Request(
                    info['second_category_url'],
                    callback = self.parse_bookpage,
                    meta = {'meta':info}
                )

    def parse_bookpage(self, response):
        info = response.meta['meta']
        lastpage = response.xpath('//*[@id="J_bottomPage"]/span[1]/a[9]/text()').get()
        
        for i in range(1,int(lastpage)+1):
            url ='https://list.jd.com' + response.xpath('//*[@id="J_bottomPage"]/span[1]/a[2]/@href').get()
            url = url.replace('page=1','page='+str(i))
            
            yield scrapy.Request(
                url, 
                callback = self.parse_bookinfo,
                meta={'meta':info}
            ) 

    # parse_bookinfo
    def parse_bookinfo(self,response):
        # get response.meta
        info = response.meta['meta']
        # get book xpath selector list
        book_list = response.xpath('//*[@id="plist"]/ul/li/div')
        for i in book_list:
            item = JdbookItem()
            item['first_category'] = info['first_category']
            item['second_category'] = info['second_category']
            item['second_category_url'] = info['second_category_url']
            item['name'] = i.xpath('./div[3]/a/em/text()').get().strip()
            item['detail_url'] ='https:'+ i.xpath('./div[1]/a/@href').get()
            item['author'] = i.xpath('./div[4]/span[1]/span/a/text()').get()
            item['publisher'] =i.xpath('./div[4]/span[2]/a/text()').get()
            item['pub_date'] = i.xpath('./div[4]/span[3]/text()').get().strip()
            skuid = i.xpath('./@data-sku').get()
            
            url = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuid

            yield scrapy.Request(
                url, 
                callback = self.parse_bookprice,
                meta = {'meta':item}
                )


    def parse_bookprice(self, response):
        # get price
        item = response.meta['meta']
        data = json.loads(response.text)
        item['price'] = data['0']['op']
        yield item
