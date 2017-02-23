import nltk
from konlpy.tag import Twitter
import MySQLdb
from datetime import datetime, timedelta
import sys
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

host = sys.argv[1]
db = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]

db = MySQLdb.connect(host=host, db=db, user=user, passwd=passwd, charset="utf8", use_unicode=True)
cursor = db.cursor()


def tokenize(data):
    ignore_types = ['Punctuation', 'Josa', 'Eomi']
    ignore_chars = ['…', '“', '”', '·', '’', '‘', '”“']
    result = []
    for t in data:
        if t[1] not in ignore_types and t[0] not in ignore_chars:
            result.append('/'.join(t))
    return result


def get_issue_keywors(candidate, start_date, end_date):
    if candidate == 'ALL':
        query = "select title from scraps WHERE created_at between '" + start_date + "' and '" + end_date + "';"
        most_common = 50
    else:
        query = "select title from scraps WHERE created_at between '" + start_date + "' and '" + end_date + \
                   "' and title like '%" + candidate + "%';"
        most_common = 20

    cursor.execute(query)
    recent_data = cursor.fetchall()

    raw_data = ''
    for obj in recent_data:
        raw_data += obj[0]

    pos = Twitter().pos(raw_data)
    token = tokenize(pos)
    nltk_text = nltk.Text(token)

    most_dict = {}
    for data in nltk_text.vocab().most_common(most_common):
        if data[1] > 1:
            most_dict[data[0]] = data[1]

    print(most_dict)

    finder = BigramCollocationFinder.from_words(nltk_text, 2)
    finder.apply_freq_filter(2)
    finder.apply_word_filter(lambda w: len(w) < 3)
    bigram_measures = BigramAssocMeasures()
    collocations = finder.nbest(bigram_measures.mi_like, 20)

    colloc_list = []
    for w1, w2 in collocations:
        if w1 in most_dict or w2 in most_dict:
            colloc_list.append(w1.split('/')[0] + ' ' + w2.split('/')[0])

    print(colloc_list)

    result_list = []
    for colloc in colloc_list:
        split_colloc = colloc.split(' ')
        check = True
        for result in result_list:
            if split_colloc[0] in result:
                index = result.index(split_colloc[0])
                result.insert(index + 1, split_colloc[1])
                check = False
            elif split_colloc[1] in result:
                index = result.index(split_colloc[1])
                result.insert(index - 1, split_colloc[0])
                check = False

        if check:
            result_list.append(split_colloc)

    result_string_list = []
    for result in result_list:
        result_string = ''
        for string in result:
            result_string += string + ' '
        result_string_list.append(result_string.strip())

    print(result_string_list)
    return result_string_list


candidates = ['문재인', '안희정', '안철수', '이재명', '유승민', '남경필', '황교안', 'ALL']


def get_keywords_of_day(date):
    for candidate in candidates:
        result = get_issue_keywors(candidate, date.strftime('%Y%m%d'), (date + timedelta(days=1)).strftime('%Y%m%d'))

        cursor.execute("select * from issue_keyword where candidate = %s and date = %s", (candidate, date.strftime('%Y%m%d')))
        if cursor.rowcount != 0:
            cursor.execute("update issue_keyword set keywords = %s where candidate = %s and date = %s", (str(result), candidate, date.strftime('%Y%m%d')))
        else:
            cursor.execute("insert into issue_keyword (candidate, keywords, date) values (%s,%s,%s)",
                           (candidate, str(result), date.strftime('%Y%m%d')))

        db.commit()

# get_keywords_of_day(datetime.strptime('20170209', '%Y%m%d'))
get_keywords_of_day(datetime.now())

db.close()
