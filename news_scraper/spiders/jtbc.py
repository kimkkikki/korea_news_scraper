# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "jtbc"
    allowed_domains = ["news.jtbc.joins.com"]
    start_urls = ['http://news.jtbc.joins.com/section/index.aspx?scode=10/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//dt')
        result_list = []
        for select in selects:
            titles = select.xpath('a/text()').extract()
            links = select.xpath('a/@href').extract()

            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item = items.NewsScraperItem()
                    item['title'] = title
                    item['link'] = 'http://news.jtbc.joins.com' + links[0]
                    item['cp'] = 'jtbc'
                    result_list.append(item)

        return result_list
