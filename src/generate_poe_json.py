#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2

from src import local_settings


def to_json_author():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select authorid, birthyear, deathyear, authordesc, dynasty, authorname from authors order by AuthorName'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['authorid'] = row[0]
        result['birthyear'] = row[1]
        result['deathyear'] = row[2]
        result['authordesc'] = row[3]
        result['dynasty'] = row[4]
        result['authorname'] = row[5]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    with open(r'output\authors.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])


def to_json_poe():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select works.Dynasty, Content, Title, Translation, MasterComment, authors.AuthorName from works left join Authors on AuthorObjectId = Authors.ObjectId'''
    cur.execute(sql_str)
    data = cur.fetchall()
    cur.close()
    conn.close()
    jo = []
    for row in data:
        result = dict()
        result['Dynasty'] = row[0]
        result['Content'] = row[1]
        result['Title'] = row[2]
        result['Translation'] = row[3]
        result['MasterComment'] = row[4]
        result['AuthorName'] = row[5]
        jo.append(result)

    json_str = json.dumps(jo, ensure_ascii=False)
    with open(r'output\works.json', 'w', encoding='utf-8') as f:
        f.write(json_str[1:-1])


def format_json_file():
    file_data = ''
    with open(r'output\authors.json', encoding='utf-8') as f:
        for line in f:
            line = line.replace('},', '}\n')
            line = line.replace(r'\r\n', '')
            file_data += line 

    with open(r'output\authors_1.json', 'w', encoding='utf-8') as f:
        f.write(file_data)


to_json_author()
format_json_file()