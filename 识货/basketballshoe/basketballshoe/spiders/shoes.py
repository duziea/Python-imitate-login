# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from basketballshoe.items import shoeItem


class ShoesSpider(scrapy.Spider):
    name = 'shoes'
    allowed_domains = ['shihuo.cn']
    start_urls = ['http://shihuo.cn/']
    
    def __init__(self):
        self.info = {}

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        ul = soup.select(
            'body > div.shihuo-content-wrap > div > div.top-block.clearfix > div.left-menu > ul')
        a_list = ul[0].find_all('a')
        for a in a_list[2:3]:
            link = 'http:' + a['href']
            category = a.string
            self.info['category'] = category
            self.info['category_link'] = link

            yield scrapy.Request(link,
                                 meta={
                                     'link': link
                                 },
                                 callback=self.get_info
                                 )

    def get_info(self, response):
        link = response.meta['link']
        total = int(response.xpath(
            '/html/body/div[2]/div/div[1]/div[3]/div/span/text()').get())
        pagesize = 60
        if total <= pagesize:
            totalpage = 1
        else:
            totalpage = total//pagesize + 1
        
        res = urlparse(link)
        scheme = res.scheme
        netloc = res.netloc
        path = res.path
        query = res.query

        for i in range(totalpage+1):
            page = f'page={i}'
            link = scheme + '://' + netloc + path+'?'+query+'&'+page

            yield scrapy.Request(link,callback=self.get_detail)


    def get_detail(self,response):
        shoe_list = response.xpath('//*[@id="js_hover"]/li')
        for i in shoe_list:
            detail_link ='http:'+ i.xpath('./div[1]/div/a/@href').get()
            img_link = i.xpath('./div[1]/div/a/img/@src').get()
            name = i.xpath('./div[3]/a/text()').get()
            price = i.xpath('./div[4]/span/b/text()').get()
            item = shoeItem()
            item['category'] = self.info['category']
            item['detail_link'] = detail_link
            item['img_link'] = img_link
            item['name'] = name
            item['price'] = price

            print(item)
            yield item
            

            



