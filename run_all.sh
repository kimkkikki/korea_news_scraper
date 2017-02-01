#!/bin/bash

cd /home/kimkkikki/korea_news_scraper
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl chosun >> /home/kimkkikki/cron.log 2>&1
scrapy crawl jtbc >> /home/kimkkikki/cron.log 2>&1
scrapy crawl mbc >> /home/kimkkikki/cron.log 2>&1
scrapy crawl sbs >> /home/kimkkikki/cron.log 2>&1
scrapy crawl joins >> /home/kimkkikki/cron.log 2>&1
scrapy crawl donga >> /home/kimkkikki/cron.log 2>&1
scrapy crawl yonhap >> /home/kimkkikki/cron.log 2>&1
scrapy crawl ytn >> /home/kimkkikki/cron.log 2>&1
scrapy crawl sisain >> /home/kimkkikki/cron.log 2>&1
scrapy crawl newsis >> /home/kimkkikki/cron.log 2>&1
scrapy crawl munhwa >> /home/kimkkikki/cron.log 2>&1
scrapy crawl hani >> /home/kimkkikki/cron.log 2>&1
scrapy crawl khan >> /home/kimkkikki/cron.log 2>&1
scrapy crawl kmib >> /home/kimkkikki/cron.log 2>&1
scrapy crawl ohmynews >> /home/kimkkikki/cron.log 2>&1
scrapy crawl ichannela >> /home/kimkkikki/cron.log 2>&1
scrapy crawl tvchosun >> /home/kimkkikki/cron.log 2>&1
scrapy crawl asiae >> /home/kimkkikki/cron.log 2>&1
scrapy crawl mk >> /home/kimkkikki/cron.log 2>&1
scrapy crawl mbn >> /home/kimkkikki/cron.log 2>&1
scrapy crawl heraldcorp >> /home/kimkkikki/cron.log 2>&1
scrapy crawl segye >> /home/kimkkikki/cron.log 2>&1
scrapy crawl mt >> /home/kimkkikki/cron.log 2>&1
scrapy crawl sedaily >> /home/kimkkikki/cron.log 2>&1
scrapy crawl seoul >> /home/kimkkikki/cron.log 2>&1
scrapy crawl edaily >> /home/kimkkikki/cron.log 2>&1
