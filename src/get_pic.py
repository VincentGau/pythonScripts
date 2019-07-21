#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import requests


root_url = r'https://hytechcn.en.alibaba.com/productlist-9.html?spm=a2700.8304367.topnav.2.a62e5f45jv2ctM'
# url = r'https://hytechcn.en.alibaba.com/product/62045872915-800587624/60_60_resolution_compact_infrared_camera_thermal_imager_used_in_floorheating_leakage_detecting_and_electric_products_repairing.html?spm=a2700.8304367.prewdfa4cf.64.31ca57bbXFKBx4'
url = r'https://hytechcn.en.alibaba.com/product/60831994709-800587624/HT_102_32_32_resolution_advanced_mini_thermal_camera_mobile.html?spm=a2700.8304367.prewdfa4cf.4.3c6157bbJZATey'

pic_url = r'//sc01.alicdn.com/kf/HTB1JymcNwDqK1RjSZSyq6yxEVXaU/60-60-resolution-compact-infrared-camera-thermal.jpg_350x350.jpg'
path_base = r'C:\Users\Kohaku\Desktop\X\\'


def get_all_prod_urls():
    results = []
    r = requests.get(root_url)
    soup = BeautifulSoup(r.text, 'lxml')
    prod_c = soup.find('form', id='products-container').find_all('a')
    for i in prod_c:
        h = i['href']
        if h.startswith('/'):
            results.append('http://hytechcn.en.alibaba.com/' + h)
    return set(results)


def get_pics(url):
    print('processing ' + url)
    page_data = requests.get(url)
    soup = BeautifulSoup(page_data.text, 'lxml')
    imgs = []
    folder_name = url.split('/')[-1]
    print(folder_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for img in soup.find_all('img'):
        imgs.append(img.get('src'))
    for i, img in enumerate(imgs):
        filename = os.path.join(folder_name, str(i) + '.jpg')
        if not img.startswith('http'):
            img = 'http:' + img
        open(filename, 'wb').write(requests.get(img).content)


prods_url = get_all_prod_urls()
for prod in prods_url:
    get_pics(prod)


def get_pic(url):
    page_data = requests.get(url)
    soup = BeautifulSoup(page_data.text, 'lxml')
    model_name = list(soup.find(name='span', attrs={'title': 'Model Number'}).parent.parent.children)[-2]
    model_name = model_name.get_text().strip()
    dir_name = path_base + model_name
    if os.path.exists(dir_name):
        return model_name, []
    os.mkdir(dir_name)
    imgs = []
    for img in soup.find_all('img'):
        imgs.append(img.get('src'))
    return model_name, imgs


def download_pic(pic_urls, sub_dir):
    for i, url in enumerate(pic_urls):
        file_path = path_base + '\\' + sub_dir + '\\' + str(i) + '.jpg'
        print(file_path)
        if not url.startswith('http'):
            url = 'http:' + url
        open(file_path, 'wb').write(requests.get(url).content)


# prods_url = get_all_prod_urls()
# for i in prods_url:
#     print(i)
# for url in prods_url:
#     print(url)
#     m_name, imgs = get_pic(url)
#     print(m_name)
#     download_pic(imgs, m_name)
