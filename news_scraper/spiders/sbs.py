# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "sbs"
    allowed_domains = ["news.sbs.co.kr"]
    start_urls = ['http://news.sbs.co.kr/news/newsSection.do?sectionType=01/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains(@href, "news_id")]')
        result_list = []
        for select in selects:
            titles = select.xpath('@title').extract()
            links = select.xpath('@href').extract()

            if len(titles) > 0 and len(links) > 0:
                item = items.NewsScraperItem()
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'sbs'
                    result_list.append(item)

        return result_list
