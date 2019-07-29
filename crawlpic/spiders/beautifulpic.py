# -*- coding: utf-8 -*-
import scrapy


class BeautifulpicSpider(scrapy.Spider):
    name = 'beautifulpic'
    # allowed_domains = ['image.baidu.com']
    # allowed_domains = ['pixabay.com']
    allowed_domains = ['www.85814.com']
    start_urls = ['https://www.85814.com/']

    def parse(self, response):
        pass
