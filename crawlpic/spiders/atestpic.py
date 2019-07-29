# -*- coding: utf-8 -*-
import scrapy
import logging


class AtestpicSpider(scrapy.Spider):
    name = 'atestpic'
    allowed_domains = ['85814.com']
    start_urls = ['https://www.85814.com/']

    def __init__(self, *args, **kwargs):
        pass

    def start_requests(self):
        '''self defined, it must be iterable'''
        tmp_url = 'https://www.85814.com/meinv/yizhoujingxuanmeinv/'
        yield scrapy.http.Request(tmp_url, self.parse_tmp_url)
        # for url in AtestpicSpider.start_urls:
        #     yield scrapy.http.Request(url, self.parse)

    def parse(self, response):
        response.cookie
        pass

    def parse_tmp_url(self, response):
        # if isinstance(response, scrapy.http.TextResponse):
        #     response.text
        self.log('=========== begin parse =============')
        # self.log(type(response.text))

        # save_file = 'clawl_files/clawl_file.html'
        # with open(save_file, 'wb') as tfile:
        #     tfile.write(response.text.encode(encoding="utf8"))

        # allimgs = response.xpath('//dd/p//img/@src').extract()
        # for img in allimgs:
        #     self.log(img)
        #     yield response.follow(img, self.down_img)
        allimgs = response.xpath('//dd/p//img/@src')
        for img in allimgs:
            self.log(img.get())
            yield response.follow(img, self.down_img)

        self.log("============ end parse ==============")

    # def parse_body(self, response):
    #     # response = scrapy.http.TextResponse

    #     # alllist = response.xpath('//dd/p[@id="1"]').extract()
    #     allimgs = response.xpath('//dd/p//img/@src').extract()
    #     for img in allimgs:
    #         # print(img)
    #         # self.log(img, logging.DEBUG)
    #         yield response.follow(allimgs, self.down_img)

    #     # self.log(alllist)

    def down_img(self, response):
        self.log("===down img===")
        # self.log('saving img: %(s)', logging.DEBUG, response.url)
        url = response.url
        theimgname = url.split('/')[-1]

        file_path = 'clawl_files/' + theimgname
        with open(file_path, "bw") as alias:
            alias.write(response.body)

        # self.log(asss, logging.DEBUG)

        # save_file = 'clawl_files/clawl_file.html'
        # with open(save_file, 'wb') as tfile:
        #     tfile.write(response.body)
