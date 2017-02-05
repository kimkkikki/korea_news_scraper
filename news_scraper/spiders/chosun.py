# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "chosun"
    allowed_domains = ["news.chosun.com"]
    start_urls = ['http://news.chosun.com/politics/index.html/']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "html_dir")]')
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
                    item['cp'] = 'chosun'

                    result_list.append(item)

        return result_list
