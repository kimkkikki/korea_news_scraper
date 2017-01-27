# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "mbn"
    allowed_domains = ["mbn.mk.co.kr"]
    start_urls = ['http://mbn.mk.co.kr/pages/news/newsSectionMain.mbn?category=mbn00006']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "news_seq_no")]')
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

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = links[0]
                    item['cp'] = 'mbn'
                    result_list.append(item)

        return result_list
