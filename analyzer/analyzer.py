import nltk
from konlpy.tag import Twitter
import MySQLdb
from datetime import datetime, timedelta
import sys

pos_tagger = Twitter()


def tokenize(doc):
    return_array = []
    for t in pos_tagger.pos(doc, norm=True, stem=True):
        if t[1] in 'Noun' and t[0] not in candidates:
            return_array.append('/'.join(t))

    return return_array


candidates = ['문재인', '안철수', '이재명', '유승민', '안희정', '황교안', '남경필']
ignore = ['대선', '대행', '행보', '오늘', '권한', '에서']

host = sys.argv[1]
db = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]

db = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, charset="utf8", use_unicode=True)

for candidate in candidates:
    cursor = db.cursor()
    cursor.execute("select title, cp, id, created_at from scraps WHERE created_at between '" +
                   str(datetime.now() - timedelta(hours=3)) + "' and '" + str(datetime.now()) +
                   "' and title like '%" + candidate + "%' ")

    recent_data = cursor.fetchall()

    data_doc = [(tokenize(data[0]), data[2]) for data in recent_data]
    tokens = [t.split('/')[0] for d in data_doc for t in d[0]]
    text = nltk.Text(tokens, name='news_data')

    top_text = {}

    for text_data in text.vocab().most_common():
        if len(text_data[0]) > 1 and text_data[1] > 1 and text_data[1] / len(data_doc) >= 0.3 \
                and (text_data[1] not in ignore):
            top_text[text_data[0]] = text_data[1]

        if len(top_text) == 3:
            break

    for text in top_text:
        cursor.execute("insert into keywords (candidate, keyword, count, created_at) values (%s,%s,%s, %s)",
                       (candidate, text, top_text[text], datetime.now().strftime('%Y-%m-%d %H:%M')))
        db.commit()

db.close()
