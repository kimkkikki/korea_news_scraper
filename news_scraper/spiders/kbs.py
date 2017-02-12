# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from .. import items
from datetime import datetime
import json


class NewsSpider(scrapy.Spider):
    name = "kbs"
    allowed_domains = ["news.kbs.co.kr"]

    def start_requests(self):
        return [FormRequest("http://news.kbs.co.kr/news/getContentsNewsList.do",
                            formdata={'CURRENT_PAGE_NO': '1', 'ROW_PER_PAGE': '20', 'SEARCH_DATE': datetime.now().strftime('%Y%m%d'),
                                      'SEARCH_CONTENTS_CODE': '0003', 'LAST_DATE': datetime.now().strftime('%Y%m%d')},
                            callback=self.parse)]

    def parse(self, response):
        json_obj = json.loads(response.body)
        data_list = json_obj.get('page_list', [])
        result_list = []

        for data in data_list:
            title = data.get('NEWS_TITLE', None)
            link = data.get('NEWS_CODE', None)

            if title is not None and link is not None:
                item = items.NewsScraperItem()
                item['title'] = title
                item['link'] = 'http://news.kbs.co.kr/news/view.do?ncd=' + str(link)
                item['cp'] = 'kbs'

                result_list.append(item)

        return result_list
