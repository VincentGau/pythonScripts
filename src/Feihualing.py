import re
import time

import psycopg2

from src import local_settings


def get_hot_works():
    """
    获取作品热表
    :return:
    """
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute("select content from works where workid in (select workid from hot_works)")
    result = []
    for work in c.fetchall():
        result.append(work[0])
    return result


def keywords_filter(works, keyword):
    """
    筛选出works中包含有keyword的作品
    :param works:
    :param keyword:
    :return:
    """
    return [work for work in works if set(work) & set(keyword)]


def get_paragraphs(work):
    return re.split('\r\n|\n', work)


def get_paragraphs_all(works):
    result = []
    for work in works:
        result += get_paragraphs(work)


def get_single_sentence(work):
    """
    切分单句，\r\n暂不处理，返回时再删去，Lazy原则
    :param work:
    :return:
    """
    return re.split('，|。|！|？', work)


def get_single_sentence_all(works):
    result = []
    for work in works:
        result += get_single_sentence(work)
    return result

# keywords = '风光'
# print(keywords_filter(get_hot_works(), keywords))

# l = get_hot_works()
# print(set(l[0]) & set('风光四十'))
# print(l[0])

# print('a' if set("asdfasdfasfd") & set("ddd") else 'b')

# get_paragraphs_all(keywords_filter(get_hot_works(), '风'))

# s = get_single_sentence(get_hot_works()[0])
# print(s)

# print(len(get_hot_works()))
# print(keywords_filter(get_hot_works(), '风'))

# ws = get_hot_works()
# print(get_single_sentence(ws[0]))
# print('----------------')
# print(get_single_sentence(ws[1]))
# print('----------------')
# print(get_single_sentence(ws[0]) + get_single_sentence(ws[1]))


print(len(keywords_filter(get_hot_works(), '词')))
r=[]
for s in get_single_sentence_all(keywords_filter(get_hot_works(), '词')):
    # print(s)
    if set(s) & set('三山半落青天外') and set(s) & set('词'):
        print(s)
        r.append(s)
print(r)