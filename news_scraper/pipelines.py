# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from datetime import datetime


class NewsScraperPipeline(object):

    def __init__(self):
        host = '104.199.133.72'
        user = 'daesun'
        password = 'aabb1122'
        self.database = 'daesun'
        self.table = 'scraps'

        self.conn = pymysql.connect(host=host, user=user, password=password, db=self.database, charset='utf8')
        self.curs = self.conn.cursor()

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        cp = item['cp']
        self.curs.execute("select * from " + self.database + "." + self.table + " where title = %s or link = %s", (title, link))
        result = self.curs.fetchone()

        if result:
            print('data already exist')
        else:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.curs.execute("insert into " + self.database + "." + self.table + " (title, link, cp, created_at, updated_at)"
                              " values (%s, %s, %s, %s, %s)", (title, link, cp, now, now))
            self.conn.commit()

        return item

    def spider_closed(self, spider):
        self.conn.close()
