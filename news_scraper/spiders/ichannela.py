# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "ichannela"
    allowed_domains = ["www.ichannela.com"]
    start_urls = ['http://www.ichannela.com/news/template/politic_news.do?cateCode=000401']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "news_detail")]')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            titles = select.xpath('span/span[@class="subject"]/text()').extract()
            links = select.xpath('@href').extract()
            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = 'http://www.ichannela.com' + links[0]
                    item['cp'] = 'ichannela'
                    result_list.append(item)

        return result_list
