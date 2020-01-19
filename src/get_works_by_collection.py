#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import psycopg2
import requests
from collections import defaultdict

from src import local_settings

url = 'https://avoscloud.com/1.1/call/getWorksByCollection'


def get_works_by_collection(collectionObjectId, collectionId):
    """
    调用接口获取分类下所有作品
    :return:
    """
    collection_work = []
    page = 1

    while True:
        print(f"Processing:{page}")
        payload = {"collectionId":collectionObjectId,"page":page,"perPage":500}

        headers = {
            'x-lc-id'  : '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
            'x-lc-prod': '0',
            'x-lc-sign': '14a8f5d694c8e29291aa7d07764b7408,1579223201180',
            'x-lc-ua'  : 'LeanCloud-JS-SDK/3.13.2 (Browser)'
        }

        r = requests.post(url=url, headers=headers, data=payload, verify=False)

        result_dict = json.loads(r.content)
        works_dict = result_dict['result']
        print(len(works_dict))

        if works_dict:
            for work in works_dict:
                try:
                    collection_work.append((collectionObjectId, collectionId, work['objectId'], work['workId']))
                except:
                    print(work)
        else:
            print(f"END at page {page}")
            break
        page += 1
    return collection_work


def insert_collection_work():
    """

    将作者信息插入work表

    :return:
    """
    works_info = set(get_all_connections())
    conn = psycopg2.connect(database="hakudb", user="haku", password="haku", host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table collection_work CASCADE''')
    c.executemany(
        '''insert into collection_work (collectionObjectId, collectionId, workObjectId, workId) values (%s, %s, %s, %s)''',
        works_info)
    conn.commit()
    conn.close()


def get_collections():
    """
    从数据库获取分类数据
    :return:
    """
    conn = psycopg2.connect(database="hakudb", user="haku", password="haku", host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute("select ObjectId, collectionid from collection")
    return c.fetchall()


def get_all_connections():
    result = []
    for a, b in get_collections():
        print(a, b)
        result += get_works_by_collection(a, b)
    return result

insert_collection_work()