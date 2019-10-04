# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
import json
from lagou_scrapy.items import LagouScrapyItem, DetailItem
from bs4 import BeautifulSoup
import scrapy_redis

class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['www.lagou.com']
    # custome_setting可用于自定义每个spider的设置，而setting.py中的都是全局属性的，当你的
    # scrapy工程里有多个spider的时候这个custom_setting就显得很有用了
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
            'user-Agent': str(UserAgent().random)
        }
    }

    def start_requests(self):
        # requests = []
        url = "https://www.lagou.com/jobs/positionAjax.json?city=全国&needAddtionalResult=false"
        for i in range(1, 30):
            data = {
                "first": "True",
                "pn": str(i),
                "kd": "python"
            }
            yield scrapy.FormRequest(
                url, method='POST', callback=self.parse2, formdata=data,  encoding='utf-8')


    def parse2(self, response):
        json_data = json.loads(response.text)
        content = json_data['content']
        showId = content['showId']  # 用与组成detail_url
        positionResult = content['positionResult']
        result = positionResult['result']

        for i in result:
            item = LagouScrapyItem()
            positionId = i['positionId']  # 职位id，用于组成detail_url
            item['positionName'] = i['positionName']  # 职位名
            item['salary'] = i['salary']  # 薪水
            item['workYear'] = i['workYear']  # 工作经验
            item['education'] = i['education']  # 教育经历
            item['createTime'] = i['createTime']  # 发布时间
            item['jobNature'] = i['jobNature']  # 工作类型
            item['companyfullname'] = i['companyFullName']  # 公司名
            # 职位详情url
            item['detail_url'] = f'https://www.lagou.com/jobs/{positionId}.html?show={showId}'
            item['city'] = i['city']

            # url = item['detail_url']
            yield item

            # yield scrapy.Request(url, method="GET", callback=self.parse3)

    # def parse3(self, response):
    #     item = response.meta['item']
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     job_detail = soup.find('div', class_='job-detail').text.strip()
    #     item['job_detail'] = job_detail

    #     yield item
