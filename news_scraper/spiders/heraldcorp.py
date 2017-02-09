# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from .. import items


class NewsSpider(scrapy.Spider):
    name = "heraldcorp"
    allowed_domains = ["biz.heraldcorp.com"]
    start_urls = ['http://biz.heraldcorp.com/list.php?ct=010108000000']

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath('//a[contains (@href, "view.php")]')
        result_list = []
        for select in selects:
            item = items.NewsScraperItem()
            titles = select.xpath('div/div[@class="list_t1 ellipsis"]/text()').extract()
            links = select.xpath('@href').extract()
            if len(titles) > 0 and len(links) > 0:
                title = ''
                for text in titles:
                    title += text
                title = title.replace('\r', '').replace('\t', '').replace('\n', '').strip()

                if 10 < len(title) < 100:
                    item['title'] = title
                    item['link'] = 'http://biz.heraldcorp.com/' + links[0]
                    item['cp'] = 'heraldcorp'
                    result_list.append(item)

        return result_list
