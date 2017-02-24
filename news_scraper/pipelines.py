# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from datetime import datetime


class NewsScraperPipeline(object):

    def __init__(self):
        host = 'localhost'
        user = 'root'
        password = ''
        self.database = 'daesun_development'
        self.table = 'scraps'

        self.conn = pymysql.connect(host=host, user=user, password=password, db=self.database, charset='utf8')
        self.curs = self.conn.cursor()

    def process_item(self, item, spider):
        if self.conn.open:
            title = item['title']
            link = item['link']
            cp = item['cp']
            self.curs.execute("select * from " + self.database + "." + self.table +
                              " where cp = %s and (title = %s or link = %s)", (cp, title, link))
            result = self.curs.fetchone()

            if result:
                print('data already exist')
            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.curs.execute("insert into " + self.database + "." + self.table + " (title, link, cp, created_at, updated_at)"
                                  " values (%s, %s, %s, %s, %s)", (title, link, cp, now, now))
                self.conn.commit()

            return item
        else:
            print('db is not connected')
            print(self.conn.Error)

    def spider_closed(self, spider):
        self.conn.close()
