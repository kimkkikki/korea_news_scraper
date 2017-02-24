# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "ohmynews"
    allowed_domains = ["www.ohmynews.com"]
    start_urls = ['http://www.ohmynews.com/NWS_Web/ArticlePage/Total_Article.aspx?PAGE_CD=C0400']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "at_pg")]')
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
                link = links[0].replace('&CMPT_CD=C1500_mini', '').replace('&CMPT_CD=Ranking_mini', '')

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = 'http://www.ohmynews.com' + link
                    item['cp'] = 'ohmynews'
                    result_list.append(item)

        return result_list
