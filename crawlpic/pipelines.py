# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlpicPipeline(object):
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    @classmethod
    def from_spider(self, crawler):
        pass
