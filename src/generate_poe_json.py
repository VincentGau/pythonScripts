#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import psycopg2

from src import local_settings


def to_json():
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    cur = conn.cursor()
    sql_str = '''select authorid, birthyear, deathyear, authordesc, dynasty, authorname from authors limit 100'''
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


to_json()
