# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "chosun"
    allowed_domains = ["news.chosun.com"]
    start_urls = ['http://news.chosun.com/politics/index.html/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//p')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            item['title'] = select.xpath('a/text()').extract()
            item['link'] = select.xpath('a/@href').extract()
            item['cp'] = 'chosun'

            result_list.append(item)

        return result_list
