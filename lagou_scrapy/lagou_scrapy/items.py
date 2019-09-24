# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    createTime = scrapy.Field()
    jobNature = scrapy.Field()
    companyfullname = scrapy.Field()
    city = scrapy.Field()
    detail_url = scrapy.Field()
    job_detail = scrapy.Field()


class DetailItem(scrapy.Item):

    work_description = scrapy.Field()
    work_duty = scrapy.Field()
    work_area = scrapy.Field()
    work_provide = scrapy.Field()
