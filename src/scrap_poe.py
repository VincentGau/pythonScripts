# encoding:utf-8
from collections import defaultdict

import requests
import json
import pymssql

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

    headers = {
        'X-LC-Id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
        'X-LC-Prod': '0',
        'X-LC-Sign': '328b7e24e9d678c600b391b039e7f881,1560524383359',
        'X-LC-UA': 'LeanCloud-JS-SDK/3.1.1 (Browser)'
    }

    authors_info = []
    page_no = 1
    while True:
        payload = {"page": page_no, "perPage": 1000}
        result_dict = json.loads(requests.post(url=url, data=payload, headers=headers).content)
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
    conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
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
    page_no = 1
    works_info = []
    while True:
        payload = {"authorId": objectId, "page": page_no, "perPage": 1000}
        result_dict = json.loads(requests.post(url=url_works_by_author, data=payload, headers=default_headers).content)
        works_dict = result_dict['result']
        if works_dict:
            for work in works_dict:
                work = defaultdict(lambda: 'DefaultValue', work)
                works_info.append((work['objectId'], work['workId'], work['Annotation'], work['AnnotationTr'],
                                  work['Appreciation'], work['AppreciationTr'], work['AuthorObjectId'], work['Content'],
                                  work['ContentTr'], work['Dynasty'], work['DynastyTr'], work['Foreword'],
                                  work['ForewordTr'], work['Intro'], work['IntroTr'], work['objectId'], work['Kind'],
                                  work['KindCN'], work['KindCNTr'], work['Title'], work['TitleTr'], work['Translation'],
                                  work['TranslationTr'], work['MasterComment'], work['MasterCommentTr']))
        else:
            break
        page_no += 1
    print(len(works_info))
    return works_info


def get_all_works():
    page_no = 1
    works_info = []
    while True:
        payload = {"page": page_no, "perPage": 1000}
        result_dict = json.loads(requests.post(url=url_all_works, data=payload, headers=default_headers).content)
        works_dict = result_dict['result']['works']

        if works_dict:
            for work in works_dict:
                work = defaultdict(lambda: 'DefaultValue', work)
                works_info.append((work['objectId'], work['workId'], work['Annotation'], work['AnnotationTr'],
                                   work['Appreciation'], work['AppreciationTr'], work['AuthorObjectId'],
                                   work['Content'],
                                   work['ContentTr'], work['Dynasty'], work['DynastyTr'], work['Foreword'],
                                   work['ForewordTr'], work['Intro'], work['IntroTr'], work['objectId'], work['Kind'],
                                   work['KindCN'], work['KindCNTr'], work['Title'], work['TitleTr'],
                                   work['Translation'],
                                   work['TranslationTr'], work['MasterComment'], work['MasterCommentTr']))
        else:
            break

        page_no += 1
        print(page_no, len(works_info))
    print(len(works_info))
    return works_info


def get_data(url, payload, filename):
    headers = {
        'X-LC-Id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
        'X-LC-Prod': '0',
        'X-LC-Sign': '328b7e24e9d678c600b391b039e7f881,1560524383359',
        'X-LC-UA': 'LeanCloud-JS-SDK/3.1.1 (Browser)'
    }
    with open(filename, 'wb') as f:
        f.write(requests.post(url=url, data=payload, headers=headers).content)


def get_all_author_object_id():
    conn = pymssql.connect(host='localhost', database='HakuTest', user='sa', password='sa')
    c = conn.cursor()
    c.execute("select ObjectId from Authors")
    return c.fetchall()


# insert_authors()
# get_data(url_works_by_author, {"authorId": "57b8fb582e958a005fa52193", "page": 2, "perPage": 500}, 'works-500-2.txt')
# get_works_by_author_id('57b8fb582e958a005fa52193')
# insert_works()
payload = {"page": 3, "perPage": 1000}
result_dict = json.loads(requests.post(url='https://9pq709je.engine.lncld.net/1.1/call/getWorksAllIncludeCount', data=payload, headers=default_headers).content)
with open('works-3-1000.txt', 'wb') as f:
    f.write(requests.post(url='https://9pq709je.engine.lncld.net/1.1/call/getWorksAllIncludeCount', data=payload, headers=default_headers).content)
print(result_dict)
# works_dict = result_dict['result']['works']
# print(len(works_dict))