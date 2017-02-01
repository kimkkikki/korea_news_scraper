# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "mbc"
    allowed_domains = ["imnews.imbc.com"]
    start_urls = ['http://imnews.imbc.com/news/2017/politic/index.html']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//li')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            titles = select.xpath('a/div/text()').extract()
            links = select.xpath('a/@href').extract()
            if len(titles) < 1:
                titles = select.xpath('div/a/text()').extract()

            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'mbc'

                    result_list.append(item)

        return result_list
