# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "khan"
    allowed_domains = ["news.khan.co.kr"]
    start_urls = ['http://news.khan.co.kr/kh_politics/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "khan_art_view")]')
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

                if 10 < len(title) < 200:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'khan'
                    result_list.append(item)

        return result_list
