# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from news_scraper.spiders import chosun, jtbc, mbc, sbs

process = CrawlerProcess()
process.settings = settings

process.crawl(chosun.NewsSpider)
process.crawl(jtbc.NewsSpider)
process.crawl(mbc.NewsSpider)
process.crawl(sbs.NewsSpider)

process.start()
