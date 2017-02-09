# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "joins"
    allowed_domains = ["news.joins.com"]
    start_urls = ['http://news.joins.com/politics/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains(@href, "article")]')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            titles = select.xpath('text()').extract()
            links = select.xpath('@href').extract()
            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = 'http://news.joins.com' + links[0]
                    item['cp'] = 'joins'
                    result_list.append(item)

        return result_list
