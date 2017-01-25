# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class SbsSpider(scrapy.Spider):
    name = "sbs"
    allowed_domains = ["http://news.sbs.co.kr"]
    start_urls = ['http://news.sbs.co.kr/news/newsSection.do?sectionType=01/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains(@href, "news_id")]')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            title = select.xpath('@title').extract()
            item['title'] = title
            item['link'] = select.xpath('@href').extract()
            item['cp'] = 'sbs'

            if len(str(title)) > 6:
                result_list.append(item)

        return result_list
