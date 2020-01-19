#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2

from src import local_settings


def gen_csv_hot():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select WorkId, Annotation, Appreciation, Content, Works.Dynasty, Intro, Kind, Title, Translation, MasterComment, authors.AuthorName, authors.AuthorId, authors.ObjectId, layout, likescount, listscount, postscount, quotescount, viewscount, works.baiduwiki from works left join Authors on AuthorObjectId = Authors.ObjectId where likescount + listscount > 10'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()

    with open(f'output\works_hot.csv', 'w', encoding='utf-8') as f:
        f.write('WorkId, Annotation, Appreciation, Content, Dynasty, Intro, Kind, Title, Translation, MasterComment, AuthorName, AuthorId, AuthorObjId, Layout, LikesCount, ListsCount, PostsCount, QuotesCount, ViewsCount, BaiduWiki ')
        for row in data:
            f.write(','.join(str(i).replace(r'\r\n', r'\\r\\n') for i in row))


def gen_csv_cold():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select WorkId, Annotation, Appreciation, Content, Works.Dynasty, Intro, Kind, Title, Translation, MasterComment, authors.AuthorName, authors.AuthorId, authors.ObjectId, layout, likescount, listscount, postscount, quotescount, viewscount, works.baiduwiki from works left join Authors on AuthorObjectId = Authors.ObjectId where likescount + listscount <= 10'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()

    with open(f'output\works_cold.csv', 'w', encoding='utf-8') as f:
        f.write('WorkId, Annotation, Appreciation, Content, Dynasty, Intro, Kind, Title, Translation, MasterComment, AuthorName, AuthorId, AuthorObjId, Layout, LikesCount, ListsCount, PostsCount, QuotesCount, ViewsCount, BaiduWiki ')
        for row in data:
            f.write(','.join(str(i).replace(r'\r\n', r'\\r\\n') for i in row))


def gen_csv_author():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",port="5432")
    cur = conn.cursor()
    sql_str = '''select authorid, objectid, birthyear, deathyear, authordesc, dynasty, authorname, WorksCiCount, WorksShiCount, WorksQuCount, WorksWenCount, WorksFuCount, WorksCount, baiduWiki, likerscount from authors'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    with open(r'output\authors.csv', 'w', encoding='utf-8') as f:
        f.write('authorid, objectid, birthyear, deathyear, authordesc, dynasty, authorname, WorksCiCount, WorksShiCount, WorksQuCount, WorksWenCount, WorksFuCount, WorksCount, baiduWiki, likerscount')
        for row in data:
            f.write(','.join(str(i) for i in row))

def gen_json_hot():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select WorkId, Annotation, Appreciation, Content, Works.Dynasty, Intro, Kind, Title, Translation, MasterComment, authors.AuthorName, authors.AuthorId, authors.ObjectId, layout, likescount, listscount, postscount, quotescount, viewscount, works.baiduwiki from works left join Authors on AuthorObjectId = Authors.ObjectId where likescount + listscount > 10'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['WorkId'] = row[0]
        result['Annotation'] = row[1]
        result['Appreciation'] = row[2]
        result['Content'] = row[3]
        result['Dynasty'] = row[4]
        result['Intro'] = row[5]
        result['Kind'] = row[6]
        result['Title'] = row[7]
        result['Translation'] = row[8]
        result['MasterComment'] = row[9]
        result['AuthorName'] = row[10]
        result['AuthorId'] = row[11]
        result['AuthorObjId'] = row[12]
        result['Layout'] = row[13]
        result['LikesCount'] = row[14]
        result['ListsCount'] = row[15]
        result['PostsCount'] = row[16]
        result['QuotesCount'] = row[17]
        result['ViewsCount'] = row[18]
        result['BaiduWiki'] = row[19]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    json_str = json_str.replace('}, {"WorkId"', '}\n{"WorkId"')
    json_str = json_str.replace(r'\r\n', r'\\r\\n')
    with open(f'output\works_hot.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])


def gen_json_all():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select WorkId, Annotation, Appreciation, Content, Works.Dynasty, Intro, Kind, Title, Translation, MasterComment, authors.AuthorName, authors.AuthorId, authors.ObjectId, layout, likescount, listscount, postscount, quotescount, viewscount, works.baiduwiki from works left join Authors on AuthorObjectId = Authors.ObjectId'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['WorkId'] = row[0]
        result['Annotation'] = row[1]
        result['Appreciation'] = row[2]
        result['Content'] = row[3]
        result['Dynasty'] = row[4]
        result['Intro'] = row[5]
        result['Kind'] = row[6]
        result['Title'] = row[7]
        result['Translation'] = row[8]
        result['MasterComment'] = row[9]
        result['AuthorName'] = row[10]
        result['AuthorId'] = row[11]
        result['AuthorObjId'] = row[12]
        result['Layout'] = row[13]
        result['LikesCount'] = row[14]
        result['ListsCount'] = row[15]
        result['PostsCount'] = row[16]
        result['QuotesCount'] = row[17]
        result['ViewsCount'] = row[18]
        result['BaiduWiki'] = row[19]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    json_str = json_str.replace('}, {"WorkId"', '}\n{"WorkId"')
    json_str = json_str.replace(r'\r\n', r'\\r\\n')
    with open(f'output\works_all.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])


def gen_json_cold():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select WorkId, Annotation, Appreciation, Content, Works.Dynasty, Intro, Kind, Title, Translation, MasterComment, authors.AuthorName, authors.AuthorId, authors.ObjectId, layout, likescount, listscount, postscount, quotescount, viewscount, works.baiduwiki from works left join Authors on AuthorObjectId = Authors.ObjectId where likescount + listscount <= 10'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['WorkId'] = row[0]
        result['Annotation'] = row[1]
        result['Appreciation'] = row[2]
        result['Content'] = row[3]
        result['Dynasty'] = row[4]
        result['Intro'] = row[5]
        result['Kind'] = row[6]
        result['Title'] = row[7]
        result['Translation'] = row[8]
        result['MasterComment'] = row[9]
        result['AuthorName'] = row[10]
        result['AuthorId'] = row[11]
        result['AuthorObjId'] = row[12]
        result['Layout'] = row[13]
        result['LikesCount'] = row[14]
        result['ListsCount'] = row[15]
        result['PostsCount'] = row[16]
        result['QuotesCount'] = row[17]
        result['ViewsCount'] = row[18]
        result['BaiduWiki'] = row[19]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    json_str = json_str.replace('}, {"WorkId"', '}\n{"WorkId"')
    json_str = json_str.replace(r'\r\n', r'\\r\\n')
    with open(f'output\works_cold.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])



def to_json_author():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select authorid, objectid, birthyear, deathyear, authordesc, dynasty, authorname, WorksCiCount, WorksShiCount, WorksQuCount, WorksWenCount, WorksFuCount, WorksCount, baiduWiki, likerscount from authors'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['authorid'] = row[0]
        result['objectid'] = row[1]
        result['birthyear'] = row[2]
        result['deathyear'] = row[3]
        result['authordesc'] = row[4]
        result['dynasty'] = row[5]
        result['authorname'] = row[6]
        result['WorksCiCount'] = row[7]
        result['WorksShiCount'] = row[8]
        result['WorksQuCount'] = row[9]
        result['WorksWenCount'] = row[10]
        result['WorksFuCount'] = row[11]
        result['WorksCount'] = row[12]
        result['baiduWiki'] = row[13]
        result['likerscount'] = row[14]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    json_str = json_str.replace('}, {"authorid"', '}\n{"authorid"')
    json_str = json_str.replace(r'\r\n', '')
    with open(r'output\authors.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])



if __name__ == '__main__':
    # gen_json_hot()
    # gen_json_cold()
    to_json_author()
    # gen_json_all()