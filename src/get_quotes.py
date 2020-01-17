#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import psycopg2
import requests
from collections import defaultdict

from src import local_settings

url = 'https://avoscloud.com/1.1/call/getQuotesIncludeCount'


def get_quotes():
    """
    调用接口获取所有名句
    :return: 
    """
    quotes = []
    page = 1

    while True:
        print(f"Processing:{page}")
        payload = {"authorId": '', "kind": '', "dynasty": '', "collectionId": '', "page": page, "perPage": 500}

        headers = {
            'x-lc-id'  : '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
            'x-lc-prod': '0',
            'x-lc-sign': '14a8f5d694c8e29291aa7d07764b7408,1579223201180',
            'x-lc-ua'  : 'LeanCloud-JS-SDK/3.13.2 (Browser)'
        }

        r = requests.post(url=url, headers=headers, data=payload, verify=False)

        result_dict = json.loads(r.content)
        quotes_dict = result_dict['result']['quotes']

        if quotes_dict:
            for quote in quotes_dict:

                quote = defaultdict(lambda: 'DefaultValue', quote)
                
                try:
                    # 忽略缺少work的元素
                    quotes.append((quote['objectId'], quote['quoteId'], quote['quote'], quote['quoteTr'],
                                   quote['authorName'], quote['work']['title'], quote['work']['objectId']))
                except:
                    print(quote)
        else:
            print(f"END at page {page}")
            break
        page += 1
    return quotes


def insert_quotes():
    """

    将作者信息插入quote表

    :return:
    """
    quotes_info = set(get_quotes())
    conn = psycopg2.connect(database="hakudb", user="haku", password="haku", host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table quote CASCADE''')
    c.executemany(
        '''insert into quote (objectId, quoteId, quote, quoteTr, authorName, workTitle, workObjectId) values (%s, %s, %s, %s, %s, %s, %s)''',
        quotes_info)
    conn.commit()
    conn.close()


insert_quotes()
