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
            titles = select.xpath('a/text()').extract()
            links = select.xpath('a/@href').extract()

            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text

                item['title'] = title
                item['link'] = links[0]
                item['cp'] = 'chosun'

                result_list.append(item)

        return result_list
