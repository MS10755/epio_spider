# -*- coding: utf-8 -*-
import scrapy
import json
from ..AES_python.aes import decrypt
from ..items import EpioItem
from scrapy.selector import Selector


class EpioSpiderSpider(scrapy.Spider):
    name = 'epio_spider'
    allowed_domains = ['epio.app']
    # API接口https://girlimg.epio.app/api/articles?lang=en-us&filter={"where":{"tag":"all","search":"","lang":"en-us"},"limit":20,"skip":40}
    start_urls = ['http://epio.app/']

    def __init__(self, keyword='', page_num='1'):
        super(EpioSpiderSpider).__init__()
        self.key_word = keyword
        self.page_num = int(page_num)


    def start_requests(self):
        for url in self.gen_start_urls(self.key_word, self.page_num):
            yield scrapy.Request(url)

    def gen_start_urls(self, keyword, num):
        url_list = list()
        for index in range(1, num + 1):
            url_list.append(
                'https://girlimg.epio.app/api/articles?lang=en-us&filter={"where":{"tag":"all","search":"%s",'
                '"lang":"en-us"},"limit":%d,"skip":%d}' % (
                    keyword, index * 20, (index - 1) * 20)
            )
        return url_list

    def parse(self, response):
        response_info = json.loads(response.text)
        gallery_list_info = decrypt(response_info['string'], 'gefdzfdef').decode()
        gallery_list_info = json.loads(gallery_list_info)
        for gallery in gallery_list_info:
            gallery_url = 'https://girlimg.epio.app/api/articles/%s?lang=en-us' % gallery['_id']
            item = EpioItem()
            item['gallery_title'] = gallery['title']
            item['image_index'] = 0
            yield scrapy.Request(gallery_url, meta=item, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta
        response_info = json.loads(response.text)
        image_list_info = decrypt(response_info['string'], 'gefdzfdef').decode()
        image_list_info = json.loads(image_list_info)['content']
        image_urls = Selector(text=image_list_info).xpath("//img/@src").extract()
        item['image_num'] = len(image_urls)
        for image_url in image_urls:
            item['image_urls'] = [image_url]
            item['image_index'] += 1
            yield item
