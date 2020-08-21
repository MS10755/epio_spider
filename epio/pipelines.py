# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import re


class EpioPipeline(object):
    def process_item(self, item, spider):
        return item


class DownloaderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['image_urls'][0], meta=item)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        gallery_title = item['gallery_title']
        gallery_title = re.sub(r'[/\\:*"<>|？]', '', gallery_title)
        image_index = item['image_index']
        key_word = self.spiderinfo.spider.key_word
        if key_word is '':
            key_word = '随机'
        path = '/'.join([key_word,'[%dP] ' % item['image_num'] + gallery_title, str(image_index)]) + '.jpg'
        return path
