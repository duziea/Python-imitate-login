# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class LagouScrapyPipeline(object):
    def __init__(self):
        self.file = open(r'C:\Users\Administrator\Desktop\Python-imitate-login\lagou_scrapy\info.json','a+', encoding='utf-8')
    def process_item(self, item, spider):
        data = dict(item)
        json.dump(data,self.file,ensure_ascii=False)
        
        return item
    def close_spider(self,spider):
        self.file.close()