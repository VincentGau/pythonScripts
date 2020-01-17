#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import psycopg2
import requests
from collections import defaultdict

from src import local_settings

url = 'https://avoscloud.com/1.1/call/getAllCollections'


def get_collections():
    """
    调用接口获取所有分类
    :return:
    """
    collections = []

    payload = {}

    headers = {
        'x-lc-id'  : '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
        'x-lc-prod': '0',
        'x-lc-sign': '14a8f5d694c8e29291aa7d07764b7408,1579223201180',
        'x-lc-ua'  : 'LeanCloud-JS-SDK/3.13.2 (Browser)'
    }

    r = requests.post(url=url, headers=headers, data=payload, verify=False)

    result_dict = json.loads(r.content)
    collections_dict = result_dict['result']

    if collections_dict:
        for collection in collections_dict:

            collection = defaultdict(lambda: 'DefaultValue', collection)

            try:
                collections.append(
                    (collection['objectId'], collection['collectionId'], collection['name'], collection['desc'], collection['kindId'],
                     collection['order'], collection['childOrder'], collection['cover']))
            except:
                print(collection)
    return collections


def insert_collections():
    """

    将作者信息插入collection表

    :return:
    """
    collections_info = set(get_collections())
    conn = psycopg2.connect(database="hakudb", user="haku", password="haku", host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table collection CASCADE''')
    c.executemany(
        '''insert into collection (objectId, collectionId, name, collectionDesc, kindId, collectionOrder, childOrder, cover) values (%s, %s, %s, %s, %s, %s, %s, %s)''',
        collections_info)
    conn.commit()
    conn.close()


insert_collections()