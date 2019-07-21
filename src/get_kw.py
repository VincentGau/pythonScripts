#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


def get_kw(url):
    page_data = requests.get(url)
    soup = BeautifulSoup(page_data.text, 'lxml')
    keywords = soup.find(attrs={"name": "keywords"})['content']
    title = soup.title.string
    return title.split('-')[0], keywords


def get_urls():
    results = []
    with open(r"C:\Users\Kohaku\Desktop\urls.txt") as f:
        for line in f:
            if line.startswith('http'):
                results.append(line)
    return results


urls = get_urls()
result = []
for url in urls:
    print('---')
    i = get_kw(url)
    result.append(i)

print(len(result))
for i in result:
    print(i[0])

print('----------------------')
for i in result:
    print(i[1])
