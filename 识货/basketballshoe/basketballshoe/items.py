# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class shoeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    detail_link = scrapy.Field()
    img_link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()

