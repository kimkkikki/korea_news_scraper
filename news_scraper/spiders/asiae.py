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

                if 10 < len(title) < 100 and '영업익' not in title and '영업손' not in title and '영업이익' not in title and '영업손실' not in title and '&sec=pol5' not in links[0]:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'asiae'
                    result_list.append(item)

        return result_list
