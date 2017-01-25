# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class MbcSpider(scrapy.Spider):
    name = "mbc"
    allowed_domains = ["http://imnews.imbc.com"]
    start_urls = ['http://imnews.imbc.com/news/2017/politic/index.html']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//li')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            title = select.xpath('a/div/text()').extract()
            if len(title) < 1:
                title = select.xpath('div/a/text()').extract()
            item['title'] = title
            item['link'] = select.xpath('a/@href').extract()
            item['cp'] = 'mbc'

            result_list.append(item)

        return result_list
