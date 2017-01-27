# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "hani"
    allowed_domains = ["www.hani.co.kr"]
    start_urls = ['http://www.hani.co.kr']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "society")]')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            titles = select.xpath('text()').extract()
            links = select.xpath('@href').extract()
            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '')

                if len(title) > 10:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'hani'
                    result_list.append(item)

        return result_list
