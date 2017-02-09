# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "kmib"
    allowed_domains = ["news.kmib.co.kr"]
    start_urls = ['http://news.kmib.co.kr/article/list.asp?sid1=pol']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "arcid")]')
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
                    item['link'] = 'http://news.kmib.co.kr/article/' + links[0]
                    item['cp'] = 'kmib'
                    result_list.append(item)

        return result_list
