# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "ytn"
    allowed_domains = ["www.ytn.co.kr"]
    start_urls = ['http://www.ytn.co.kr/news/news_list_0101.html/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//dt/a')
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

                if len(title) > 0 and len(title.replace(' ', '')) > 0:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'ytn'
                    result_list.append(item)

        return result_list