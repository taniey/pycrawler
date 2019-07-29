# -*- coding: utf-8 -*-
import datetime
import json
import traceback

import scrapy


class BaiDuPicSpider(scrapy.Spider):
    name = 'badupic'
    allowed_domains = ['baidu.com']
    start_urls = ['http://image.baidu.com/']

    def __init__(self, *args, **kwargs):
        self.save_dir = 'baidu_crawl_files/'
        pass

    def start_requests(self):
        '''self defined, it must be iterable'''
        tmp_url = 'http://image.baidu.com/'
        yield scrapy.http.Request(tmp_url, self.parse_img_home_url)
        # for url in AtestpicSpider.start_urls:
        #     yield scrapy.http.Request(url, self.parse)

    def parse(self, response):
        response.cookie
        pass

    def parse_img_home_url(self, response=scrapy.http.Response('')):
        # if isinstance(response, scrapy.http.TextResponse):
        #     response.text
        self.logger.debug('=========== begin parse =============')
        # self.log(type(response.text))

        self.logger.debug(response.headers)
        # response.headers

        save_file = self.save_dir + 'baidu_img_home.html'
        with open(save_file, 'wb') as tfile:
            tfile.write(response.text.encode(encoding="utf8"))

        # https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=picture&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=picture&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&1564235409512=

        now = datetime.datetime.now()
        now_ms = now.timestamp() * 1000

        qurey_url = (
            'https://image.baidu.com/search/acjson?'
            'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord='
            'picture&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&'
            'latest=&copyright=&word=picture&s=&se=&tab=&width=&height=&face=0&'
            'istype=2&qc=&nc=1&fr=&expermode=&force=&pn=30&'
            'rn={rn}&gsm={gsm}&{now}=').format(rn=30,
                                               gsm='1e',
                                               now=int(now_ms))

        self.logger.debug(qurey_url)
        yield response.follow(qurey_url, self.query_pic_index)

        # # allimgs = response.xpath('//dd/p//img/@src').extract()
        # # for img in allimgs:
        # #     self.log(img)
        # #     yield response.follow(img, self.down_img)
        # allimgs = response.xpath('//dd/p//img/@src')
        # for img in allimgs:
        #     self.log(img.get())
        #     # yield response.follow(img, self.down_img)

        self.logger.debug("============ end parse ==============")

    # def parse_body(self, response):
    #     # response = scrapy.http.TextResponse

    #     # alllist = response.xpath('//dd/p[@id="1"]').extract()
    #     allimgs = response.xpath('//dd/p//img/@src').extract()
    #     for img in allimgs:
    #         # print(img)
    #         # self.log(img, logging.DEBUG)
    #         yield response.follow(allimgs, self.down_img)

    #     # self.log(alllist)

    def query_pic_index(self, response=scrapy.http.Response("")):
        try:
            self.logger.debug("======= in qrey pic index ============")
            save_file = self.save_dir + 'baidu_pic_indx.json'
            with open(save_file, 'wb') as tfile:
                tfile.write(response.text.encode(encoding="utf8"))

            root = json.loads(response.text)

            imglst = None
            if isinstance(root, dict):
                if "data" in root:
                    imglst = root['data']

            if imglst is None or not isinstance(imglst, list):
                return

            for one in imglst:
                # self.logger.debug(one)
                objURL = one["objURL"] if "objURL" in one else None

                if objURL is not None:
                    real_url = self._decode_img_url(objURL)
                    yield response.follow(real_url, self.down_img)

                # fromURL = one["fromURL"] if "objURL" in one else None
                # if fromURL is not None:
                #     real_url = self._decode_img_url(fromURL)
                #     yield scrapy.http.Request(real_url, None)
        except Exception:
            traceback.print_exc()

    def _decode_img_url(self, encode_url=""):
        '''decode img url'''
        # self.logger.debug(encode_url)

        tmp_enc_url = encode_url
        # tmp_enc_url = tmp_enc_url.replace("ippr", "http")
        tmp_enc_url = tmp_enc_url.replace("_z2C$q", ":")
        tmp_enc_url = tmp_enc_url.replace("AzdH3F", "/")
        tmp_enc_url = tmp_enc_url.replace("_z&e3B", ".")
        tmp_enc_url = tmp_enc_url.lower()
        # tmp_enc_url = tmp_enc_url[4:]

        table = {
            "w": "a",
            "k": "b",
            "v": "c",
            "1": "d",
            "j": "e",
            "u": "f",
            "2": "g",
            "i": "h",
            "t": "i",
            "3": "j",
            "h": "k",
            "s": "l",
            "4": "m",
            "g": "n",
            "5": "o",
            "r": "p",
            "q": "q",
            "6": "r",
            "f": "s",
            "p": "t",
            "7": "u",
            "e": "v",
            "o": "w",
            "x": "x",
            "y": "y",
            "z": "z",
            "8": "1",
            "d": "2",
            "n": "3",
            "9": "4",
            "c": "5",
            "m": "6",
            "0": "7",
            "b": "8",
            "l": "9",
            "a": "0",
        }

        decode_url = ""
        for c in tmp_enc_url:
            if c in table:
                decode_url += table[c]
            else:
                decode_url += c

        self.logger.debug(decode_url)
        return decode_url

    def down_img(self, response=scrapy.http.Response("")):
        self.logger.debug("============= downing img ============")
        url = response.url
        theimgname = url.split('/')[-1]

        file_path = self.save_dir + theimgname
        with open(file_path, "bw") as alias:
            alias.write(response.body)

        # save_file = self.save_dir + 'clawl_file.html'
        # with open(save_file, 'wb') as tfile:
        #     tfile.write(response.body)
