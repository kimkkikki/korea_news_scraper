# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class JtbcSpider(scrapy.Spider):
    name = "jtbc"
    allowed_domains = ["http://news.jtbc.joins.com"]
    start_urls = ['http://news.jtbc.joins.com/section/index.aspx?scode=10/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//dt')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            item['title'] = select.xpath('a/text()').extract()
            item['link'] = select.xpath('a/@href').extract()
            item['cp'] = 'jtbc'

            result_list.append(item)

        return result_list
