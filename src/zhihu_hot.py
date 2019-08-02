#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = r'https://www.zhihu.com/hot'
headers = {
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie'         : 'q_c1=6537fab2f844429fbb9d747f617dc245|1506301315000|1463040014000; __DAYU_PP=RumiAJMFeJru2ijBrN3z2b95d82dc2ed; _zap=0eb6e9ad-bc5a-4417-afec-2e28fb0cdfd4; __gads=ID=fd9b296a6ef05041:T=1542014803:S=ALNI_Mbu-ufJcDRZprRLOE-LHsbqXYcOJw; _xsrf=AuO8aNXnrv3aZG0MK0KFjSxLBEFi5UYY; d_c0="AMDoyhkDbA-PTqnyNVKfvxDJImVin8JjVVc=|1557726607"; __utmv=51854390.100-1|2=registration_date=20130626=1^3=entry_date=20130626=1; __utma=51854390.2063786968.1560501744.1560914480.1562118194.5; __utmz=51854390.1562118194.5.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga=GA1.2.2063786968.1560501744; capsion_ticket="2|1:0|10:1564386297|14:capsion_ticket|44:NDAxYTA5ODA0MjAzNGFlMjgyZjc1MjhiMjI5MGQ5OTE=|190139a9be9f46fe5f141828e060fb2ebb4db4e5b25e5b43b56955725e4b7080"; z_c0="2|1:0|10:1564386299|4:z_c0|92:Mi4xQTJ3UEFBQUFBQUFBd09qS0dRTnNEeVlBQUFCZ0FsVk4tX0VyWGdEQ0FYZGEzd2tnc2pZUmlLSXV3UFdzVDBTYjRB|df5e92770d9c7393d49504adec8023753ada4ed04a46adfee1a84cb0ab00dfcd"; tst=h; tshl=; q_c1=6537fab2f844429fbb9d747f617dc245|1564567143000|1463040014000; tgw_l7_route=80f350dcd7c650b07bd7b485fcab5bf7',
}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')
print(soup.title)
hot_items = soup.findAll('div', attrs={"class": "HotItem-content"})
for i, item in enumerate(hot_items):
    print(i, item.contents[0]['href'], item.contents[0]['title'])
