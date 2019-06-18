# encoding:utf-8
import datetime
from collections import defaultdict

import requests
import json
import pymssql
import psycopg2
import multiprocessing as mp
import time
import local_settings


url_collections = 'https://9pq709je.engine.lncld.net/1.1/call/getAllCollections'
url_authors_by_page = 'https://9pq709je.engine.lncld.net/1.1/call/getHotAuthorsIncludeCountByLikers'
url_works_by_author = 'https://9pq709je.engine.lncld.net/1.1/call/getWorksByAuthor'
url_author_by_id = 'https://9pq709je.engine.lncld.net/1.1/call/getAuthorById2'
url_all_works = 'https://9pq709je.engine.lncld.net/1.1/call/getWorksAllIncludeCount'

default_headers = {
    'X-LC-Id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
    'X-LC-Prod': '0',
    'X-LC-Sign': '328b7e24e9d678c600b391b039e7f881,1560524383359',
    'X-LC-UA': 'LeanCloud-JS-SDK/3.1.1 (Browser)'
}


def get_authors():
    """
    get all author info. LIST

    :return: authors_info
    """
    url = 'https://9pq709je.engine.lncld.net/1.1/call/getHotAuthorsIncludeCountByLikers'

    authors_info = []
    page_no = 1
    while True:
        payload = {"page": page_no, "perPage": 1000}
        result_dict = json.loads(requests.post(url=url, data=payload, headers=default_headers).content)
        authors_dict = result_dict['result']['authors']

        if authors_dict:
            for author in authors_dict:
                author = defaultdict(lambda: 'DefaultValue', author)

                # invalid data
                if author['authorId'] == 0:
                    continue

                authors_info.append(
                    (author['objectId'], author['authorId'], author['birthYear'], author['deathYear'], author['desc'],
                     author['descTr'], author['dynasty'], author['dynastyTr'], author['name'],
                     author['nameTr'], author['worksCiCount'], author['worksShiCount'],
                     author['worksQuCount'], author['worksWenCount'], author['worksFuCount'],
                     author['worksCount']))
        else:
            break

        page_no += 1
    return authors_info


def insert_authors():
    authors_info = get_authors()
    # conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost", port="5432")
    c = conn.cursor()
    c.executemany(
        '''insert into Authors (ObjectId, AuthorId, BirthYear, DeathYear, AuthorDesc, AuthorDescTr, Dynasty, DynastyTr, AuthorName, AuthorNameTr, WorksCiCount, WorksShiCount, WorksQuCount, WorksWenCount, WorksFuCount, WorksCount) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        authors_info)
    conn.commit()
    conn.close()


def insert_works():
    authors_id = get_all_author_object_id()
    works_info = []
    for id in authors_id:
        works_info += get_works_by_author_id(id)
    conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    c = conn.cursor()
    c.executemany('insert into Works (ObjectId, WorkId, Annotation, AnnotationTr, Appreciation, AppreciationTr, AuthorObjectId, Content, ContentTr, Dynasty, DynastyTr, Foreword, ForewordTr, Intro, IntroTr, Kind, KindCN, KindCNTr, Title, TitleTr, Translation, TranslationTr, MasterComment, MasterCommentTr) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  works_info)
    conn.commit()
    conn.close()


def get_works_by_author_id(objectId):
    # print(f"Processing {objectId}")
    page_no = 1
    works_info = []
    while True:
        payload = {"authorId": objectId, "page": page_no, "perPage": 1000}
        result_dict = json.loads(requests.post(url=url_works_by_author, data=payload, headers=default_headers).content)
        try:
            works_dict = result_dict['result']
        except KeyError as e:
            print(f"{objectId}-page:{page_no}-{str(e)}")
            # print(e)
            break
        if works_dict:
            for work in works_dict:
                work = defaultdict(lambda: 'DefaultValue', work)
                works_info.append((work['objectId'], work['workId'], work['annotation'], work['annotationTr'],
                                  work['appreciation'], work['appreciationTr'], work['author']['objectId'], work['content'],
                                  work['contentTr'], work['dynasty'], work['dynastyTr'], work['foreword'],
                                  work['forewordTr'], work['intro'], work['introTr'], work['kind'],
                                  work['kindCN'], work['kindCNTr'], work['title'], work['titleTr'], work['translation'],
                                  work['translationTr'], work['masterComment'], work['masterCommentTr']))
        else:
            break
        page_no += 1
    return works_info


def get_data(url, payload, filename):
    with open(filename, 'wb') as f:
        f.write(requests.post(url=url, data=payload, headers=default_headers).content)


def get_all_author_object_id():
    conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    c = conn.cursor()
    c.execute("select ObjectId from Authors")
    return c.fetchall()


def get_author_id_from_db():
    # conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost", port="5432")
    c = conn.cursor()
    c.execute("select ObjectId from Authors")
    return c.fetchall()


def get_all_works():
    all_works = []
    for author_id in get_author_id_from_db():
        all_works += get_works_by_author_id(author_id)
    return all_works


def insert_all_works():
    conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    c = conn.cursor()
    c.executemany('insert into Works (ObjectId, WorkId, Annotation, AnnotationTr, Appreciation, AppreciationTr, AuthorObjectId, Content, ContentTr, Dynasty, DynastyTr, Foreword, ForewordTr, Intro, IntroTr, Kind, KindCN, KindCNTr, Title, TitleTr, Translation, TranslationTr, MasterComment, MasterCommentTr) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  get_all_works())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print(datetime.datetime.now())
    start_time = time.time()
    pool = mp.Pool(8)
    result = pool.map(get_works_by_author_id, get_author_id_from_db())

    pool.close()
    pool.join()

    works = []
    for i in result:
        for j in i:
            works.append(j)

    # conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    conn = psycopg2.connect(database="postgres", user="postgres", password=local_settings.POSTGRE_PWD, host="localhost", port="5432")
    c = conn.cursor()
    c.executemany(
        'insert into Works (ObjectId, WorkId, Annotation, AnnotationTr, Appreciation, AppreciationTr, AuthorObjectId, Content, ContentTr, Dynasty, DynastyTr, Foreword, ForewordTr, Intro, IntroTr, Kind, KindCN, KindCNTr, Title, TitleTr, Translation, TranslationTr, MasterComment, MasterCommentTr) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        works)
    conn.commit()
    conn.close()

    end_time = time.time() - start_time
    print(datetime.datetime.now())
    print(f"Time took: {end_time}s")

