from konlpy.tag import Twitter
import MySQLdb
from datetime import datetime, timedelta
import sys

pos_tagger = Twitter()


def tokenize(doc):
    return_array = []
    for tok in pos_tagger.pos(doc, norm=True, stem=True):
        if tok[1] in 'Noun':
            return_array.append('/'.join(tok))

    return return_array


candidates = ['문재인', '안철수', '이재명', '유승민', '안희정', '황교안', '남경필']

host = sys.argv[1]
db = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]

db = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, charset="utf8", use_unicode=True)

candidates_list = ''
for c in candidates:
    if candidates_list != '':
        candidates_list += '|' + c
    else:
        candidates_list += c

query = "select title, cp, id, created_at from scraps WHERE created_at between '" + str(
    datetime.now() - timedelta(hours=24)) + "' and '" + str(
    datetime.now()) + "' and title regexp '" + candidates_list + "' "

cursor = db.cursor()
cursor.execute(query)

recent_data = cursor.fetchall()

data_doc = [(tokenize(data[0]), data[2]) for data in recent_data]

for d in data_doc:
    # 문장의 첫 명사가 후보자이면
    if d[0][0].split('/')[0] in candidates:
        speaker = d[0][0].split('/')[0]  # 화자
        target_list = []
        for t in d[0]:
            token = t.split('/')[0]
            # 키워드가 화자가 아닌 후보자이면
            if token in candidates and token != speaker:
                target_list.append(token)

        if len(target_list) == 1:
            print(d[0])
            print(speaker, target_list[0], d[1])
            cursor.execute("insert into love_or_hate (speaker, target, related_to) values (%s,%s,%s)",
                           (speaker, target_list[0], d[1]))
            db.commit()
        else:
            print(d[0])

db.close()
