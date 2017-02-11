# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from .. import items
from datetime import datetime
import json


class NewsSpider(scrapy.Spider):
    name = "news1"
    allowed_domains = ["news1.kr"]

    def start_requests(self):
        return [FormRequest("http://news1.kr/ajax/ajax.php",
                            formdata={'cmd': 'categories', 'op': 'categories_list', 'slimit': '1', 'elimit': '20',
                                      'orderby': 'pubdate_tsm',
                                      'date': datetime.now().strftime('%Y-%m-%d'), 'sort': 'desc',
                                      'categories_sec': 'parent', 'categories_id': '1', 'upper_categories_id': '1'},
                            callback=self.parse)]

    def parse(self, response):
        json_obj = json.loads(response.body)
        data_list = json_obj.get('data', [])
        result_list = []

        for data in data_list:
            title = data.get('title', None)
            link = data.get('id', None)

            if title is not None and link is not None:
                item = items.NewsScraperItem()
                item['title'] = title
                item['link'] = 'http://news1.kr/articles/?' + link
                item['cp'] = 'news1'

                result_list.append(item)

        return result_list
