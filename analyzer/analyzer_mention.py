import MySQLdb
from datetime import datetime, timedelta
import sys

candidates = ['문재인', '안철수', '이재명', '유승민', '안희정', '황교안', '남경필']

host = sys.argv[1]
db = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]

db = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, charset="utf8", use_unicode=True)

candidates_list = ''
for speaker in candidates:
    for target in candidates:
        if speaker != target:
            query = "select title, cp, id, created_at from scraps WHERE created_at between '" + str(
                datetime.now() - timedelta(hours=24)) + "' and '" + str(
                datetime.now()) + "' and title regexp '.*" + speaker + ".*[\"\\'“]" + target + ".*[\"\\'”].*'"

            cursor = db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for d in data:
                cursor.execute("insert into love_or_hate (speaker, target, related_to) values (%s,%s,%s)",
                               (speaker, target, d[2]))
                db.commit()

db.close()
