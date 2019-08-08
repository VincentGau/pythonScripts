#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from src import local_settings

url = r'https://www.zhihu.com/hot'
headers = {
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie'         : local_settings.ZH_COOKIE,
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')
print(soup.title)
hot_items = soup.findAll('div', attrs={"class": "HotItem-content"})
for i, item in enumerate(hot_items):
    print(i, item.contents[0]['href'], item.contents[0]['title'])
