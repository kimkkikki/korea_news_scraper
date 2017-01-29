# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from news_scraper.spiders import chosun, jtbc, mbc, sbs, joins, donga, yonhap, ytn, sisain, newsis, munhwa
from news_scraper.spiders import hani, ohmynews, khan, kmib, ichannela, tvchosun, asiae, mk, mbn, heraldcorp
from news_scraper.spiders import sedaily, segye, mt

process = CrawlerProcess()
process.settings = settings

process.crawl(chosun.NewsSpider)
process.crawl(jtbc.NewsSpider)
process.crawl(mbc.NewsSpider)
process.crawl(sbs.NewsSpider)
process.crawl(joins.NewsSpider)
process.crawl(donga.NewsSpider)
process.crawl(yonhap.NewsSpider)
process.crawl(ytn.NewsSpider)
process.crawl(sisain.NewsSpider)
process.crawl(newsis.NewsSpider)
process.crawl(munhwa.NewsSpider)
process.crawl(hani.NewsSpider)
process.crawl(khan.NewsSpider)
process.crawl(kmib.NewsSpider)
process.crawl(ohmynews.NewsSpider)
process.crawl(ichannela.NewsSpider)
process.crawl(tvchosun.NewsSpider)
process.crawl(asiae.NewsSpider)
process.crawl(mk.NewsSpider)
process.crawl(mbn.NewsSpider)
process.crawl(heraldcorp.NewsSpider)
process.crawl(segye.NewsSpider)
process.crawl(mt.NewsSpider)
process.crawl(sedaily.NewsSpider)

process.start()
