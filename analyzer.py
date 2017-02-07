#!/usr/bin/env python
#-*- coding: utf-8 -*-

import nltk
from konlpy.tag import Twitter
import MySQLdb
from datetime import datetime, timedelta

pos_tagger = Twitter()


def tokenize(doc):
    return_array = []
    for t in pos_tagger.pos(doc, norm=True, stem=True):
       if(t[1] in ('Noun') and t[0] not in [candi[0] for candi in candidates]):
           return_array.append('/'.join(t))

    return return_array


candidates = [('문재인', 'moon'), ('안철수', 'ahn'), ('이재명', 'lee'), ('유승민', 'you'), ('안희정', 'hee'), ('황교안', 'hwang'), ('남경필', 'nam')]

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

db = MySQLdb.connect(host="104.199.133.72", user="daesun", passwd="aabb1122", charset="utf8", db="daesun", use_unicode=True)

start_date = datetime.strptime('2017-02-01 21:00', '%Y-%m-%d %H:%M')
end_date = datetime.strptime('2017-02-07 19:00', '%Y-%m-%d %H:%M')

while start_date <= end_date :

    for candidate in candidates:
        cursor = db.cursor()
        cursor.execute("select title, cp, id, created_at from scraps WHERE created_at between '" + str(start_date - timedelta(hours=3)) + "' and '" + str(start_date) + "' and title like '%" + candidate[0] + "%' ")

        recent_data = cursor.fetchall()

        data_doc = [(tokenize(data[0]), data[2]) for data in recent_data]
        tokens = [t.split('/')[0] for d in data_doc for t in d[0]]
        text = nltk.Text(tokens, name='news_data')

        top_text = {}

        for text_data in text.vocab().most_common():
            if len(text_data[0]) > 1 and text_data[1] > 1 and text_data[1] / len(data_doc) >= 0.3:
                top_text[text_data[0]] = text_data[1]

            if len(top_text) == 3:
                break

        for text in top_text:
            cursor.execute("insert into keywords (candidate, keyword, count, created_at) values (%s,%s,%s, %s)", (candidate[1], text, top_text[text], str(start_date)))
            db.commit()

    start_date += timedelta(hours=1)
