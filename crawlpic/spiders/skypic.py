# -*- coding: utf-8 -*-
import os

import w3lib

import scrapy
from scrapy.http import Request, Response

from crawlpic.items import CrawlpicItem
# from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urlparse


class SkyPicSpider(scrapy.Spider):
    name = 'skypic'
    allowed_domains = ['ivsky.com']
    start_urls = ['https://www.ivsky.com/']

    def __init__(self, *args, **kargs):
        self.save_root_dir = "skypic_files/"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse_home_url)

    def parse_home_url(self, response=Response("")):
        # self.logger.debug(response.headers)
        self.logger.debug('')

        save_file = self.save_root_dir + 'home.html'
        with open(save_file, 'wb') as tfile:
            tfile.write(response.text.encode(encoding="utf8"))

        hrefs = response.xpath("//ul[@class='sy_list']//a/@href")
        # self.logger.debug(hrefs)
        for link in hrefs:
            # self.logger.debug(link.get())
            yield response.follow(link, self.parse_cat_url)

    def parse_cat_url(self, response=Response("")):
        # self.logger.debug("============ begin parse cat url ===============")
        # split_path = response.url.split("/")

        # new_flag = "default"
        # if split_path[-1] == "":
        #     new_flag = split_path[-2]
        # else:
        #     new_flag = split_path[-1]

        # new_subdir = os.path.join(self.save_root_dir, new_flag)
        # os.mkdir(new_subdir)

        # save_file = self.save_root_dir + new_flag + '.html'
        # with open(save_file, 'wb') as tfile:
        #     tfile.write(response.text.encode(encoding="utf8"))

        urlitem = CrawlpicItem()
        base_url = get_base_url(response)

        allimgs = response.xpath("//ul[@class='pli']//img/@src")
        tmp_urls = []
        for url in allimgs:
            # urlitem.pic_url = url.get()
            # urlitem["image_urls"] = 'https:' + url.get()
            tmp_urls.append(urlparse(base_url, )[0] + ":" + url.get())
            # self.logger.debug(urlitem["image_urls"])
            # yield response.follow(url, self.down_img)

        urlitem["image_urls"] = tmp_urls
        # return urlitem
        yield urlitem

        # self.logger.debug("============ end parse cat url ================")

    def down_img(self, response=Response("")):
        # self.logger.debug("================= downing img ===================")
        self.logger.debug(response.url)
        split_path = response.url.split("/")
        save_file = self.save_root_dir + split_path[-1]
        self.logger.debug(save_file)
        with open(save_file, 'wb') as tfile:
            tfile.write(response.body)

        # urlitem = CrawlpicItem()
        # urlitem.pic_url = response.url
        # yield urlitem

    def parse(self, response):
        pass

    def closed(self, reason):
        pass
