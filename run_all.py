# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from news_scraper.spiders import chosun, jtbc, mbc, sbs, joins, donga

process = CrawlerProcess()
process.settings = settings

process.crawl(chosun.NewsSpider)
process.crawl(jtbc.NewsSpider)
process.crawl(mbc.NewsSpider)
process.crawl(sbs.NewsSpider)
process.crawl(joins.NewsSpider)
process.crawl(donga.NewsSpider)

process.start()
