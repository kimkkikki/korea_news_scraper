# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "seoul"
    allowed_domains = ["www.seoul.co.kr"]
    start_urls = ['http://www.seoul.co.kr/news/newsList.php?section=politics']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "newsView")]')
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
                link = links[0].replace('&wlog_sub=svt_100', '')

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = 'http://www.seoul.co.kr' + link
                    item['cp'] = 'seoul'
                    result_list.append(item)

        return result_list
