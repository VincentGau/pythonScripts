import json
import os

from bs4 import BeautifulSoup
import requests
import re


def get_img():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102',
               'atp_isdpp': 'gv2880059',
               'eagleeye-traceid': '0a67a60f15645757252906541e5e37',
               'p3p': 'CP="CAO PSA OUR"'
               }
    url = r'https://www.aliexpress.com/store/all-wholesale-products/2880059.html?spm=a2g1y.12024536.pcShopHead_35343482.1'
    r = requests.get(url, headers=headers, verify=False)
    print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    all = soup.find_all('a', class_='pic-rind')
    print(all)
    for i in all:
        print(i.get('href'))


get_img()
