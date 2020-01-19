import json
from collections import defaultdict

import psycopg2
import requests

from src import local_settings

default_headers = {
    'X-LC-Id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
    'X-LC-Prod': '0',
    'X-LC-Sign': '328b7e24e9d678c600b391b039e7f881,1560524383359',
    'X-LC-UA': 'LeanCloud-JS-SDK/3.1.1 (Browser)'
}


def get_collection_by_id(collectionId):
    url = 'https://avoscloud.com/1.1/call/getWorksByCollection'
    payload={
        'collectionId': collectionId,
        'page':1,
        'perPage':1000
    }
    result_dict = json.loads(requests.post(url=url, data=payload, headers=default_headers).content)
    print(len(result_dict['result']))
    result_list = []
    for i, w in enumerate(result_dict['result']):
        # w = defaultdict(lambda: 'DefaultValue', w)
        try:
            result_list.append((w['workId'],))
        except Exception as e:
            print(e)
    return result_list


def get_all_collections():
    '''
    抓取所有合集信息
    :return:
    '''
    url = 'https://avoscloud.com/1.1/call/getAllCollections'
    payload = {}
    result_dict = json.loads(requests.post(url=url, data=payload, headers=default_headers).content)
    collections = []
    # print(len(result_dict['result']))
    for i in result_dict['result']:
        collections.append((i['collectionId'], i['desc'], i['childOrder'], i['name'], i['shortDesc'], i['order'], i['objectId'], i['updatedAt'], i['kindId']))
    return collections


def insert_all_collections():
    '''
    向数据库插入所有合集信息
    :return:
    '''
    collections = get_all_collections()
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table collections CASCADE''')
    c.executemany(
        '''insert into collections (collectionid, collectiondesc, childorder, collectionname, shortdesc, oorder, objectid, updatedat, kindid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        collections)
    conn.commit()
    conn.close()


def insert_ci_300():
    ci = get_collection_by_id(ci_300)
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table ci_300 CASCADE''')
    c.executemany(
        '''insert into ci_300 (workid) values (%s)''',
        ci)
    conn.commit()
    conn.close()


def insert_shi_300():
    shi = get_collection_by_id(shi_300)
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost",
                            port="5432")
    c = conn.cursor()
    c.execute('''truncate table shi_300 CASCADE''')
    c.executemany(
        '''insert into shi_300 (workid) values (%s)''',
        shi)
    conn.commit()
    conn.close()


if __name__ == '__main__':

    ci_300 = '57ea81d30bd1d0005b1a8fb2'
    shi_300 = '57ea81d38ac247005be5621c'

    # 插入所有集合数据
    # insert_all_collections()

    # 插入宋词300首
    # insert_ci_300()

    # 插入唐诗300首
    # insert_shi_300()
