# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "asiae"
    allowed_domains = ["www.asiae.co.kr"]
    start_urls = ['http://www.asiae.co.kr/news/pol/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "idxno")]')
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
                link = links[0].replace('&sec=pol2', '').replace('&sec=pol5', '')

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = link
                    item['cp'] = 'asiae'
                    result_list.append(item)

        return result_list
