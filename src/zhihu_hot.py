#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import logging


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from src import local_settings




def get_zhihu_hot():
    url = r'https://www.zhihu.com/hot'
    headers = {
        'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cookie'         : local_settings.ZH_COOKIE,
    }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        hot_items = soup.findAll('div', attrs={"class": "HotItem-content"})
        if not os.path.exists('c:/data'):
            os.makedirs('c:/data')
        today = datetime.now()
        with open(f'c:/data/zhihu-hot-{today.year}-{today.month}-{today.day}.txt', 'w') as f:
            for i, item in enumerate(hot_items):
                print(i, item.contents[0]['href'], item.contents[0]['title'])
                f.write(f"{i+1} {item.contents[0]['href']} {item.contents[0]['title']}\n")
        logging.info('Success')
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    if not os.path.exists('c:/HLog'):
        os.makedirs('c:/HLog')
    logging.basicConfig(level=logging.INFO, filename='c:/HLog/zhihu_hot.log', filemode='a', format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    get_zhihu_hot()
