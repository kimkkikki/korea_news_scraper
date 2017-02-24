# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "donga"
    allowed_domains = ["news.donga.com"]
    start_urls = ['http://news.donga.com/Politics/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains(@href, "2017")]')
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
                link = links[0].replace('East/3/all', 'Politics/3/00').replace('BestClick/3/all', 'Politics/3/00')\
                    .replace('Politics/3/000028', 'Politics/3/00')

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = link
                    item['cp'] = 'donga'
                    result_list.append(item)

        return result_list
