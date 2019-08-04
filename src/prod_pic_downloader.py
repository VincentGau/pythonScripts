import json
import os

from bs4 import BeautifulSoup
import requests
import re

# prod_link = r'https://www.aliexpress.com/item/32798232410.html?gps-id=pcStoreJustForYou&scm=1007.23125.122752.0&scm_id=1007.23125.122752.0&scm-url=1007.23125.122752.0&pvid=2b745e1d-0093-4aaa-afd7-9f40a188d415&spm=a2g1y.12024536.smartJustForYou_145116788.0'
download_path = r'D:/ProductImages/'


def get_prod_detail(prod_link):
    # 真实产品链接隐藏在script的descriptionUrl中
    r = requests.get(prod_link)
    soup = BeautifulSoup(r.text, 'lxml')
    pattern = re.compile(r'"descriptionUrl":"(.*?)"')
    script = soup.find('script', text=pattern)
    real_url = pattern.search(script.text).group(1)
    prod_title = soup.title.string.split('-')[0]
    return prod_title, get_imgs(real_url)


def get_imgs(url):
    # 获取所有图片url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    imgs = soup.find_all('img')
    result = []
    for img in imgs:
        result.append(img.get('src'))
    return result


def downloader(prod_link):
    title, img_urls = get_prod_detail(prod_link)
    sub_dir = os.path.join(download_path, title)
    print(sub_dir)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
        print('Making dir: ' + sub_dir)

    for i, img_url in enumerate(img_urls):
        try:
            with open(os.path.join(sub_dir, str(i) + '.jpg'), 'wb') as f:
                f.write(requests.get(img_url).content)
        except Exception as e:
            print(f"Failed. {img_url}\n{str(e)}")


def get_prod_links():
    url = r'https://gpsfront.aliexpress.com/getI2iRecommendingResults.do?scenario=pcStoreJustForYou&storeId=2880059&offset=1&limit=25&callback=jsonp_1563683427442_57848'
    url = r'https://gpsfront.aliexpress.com/getI2iRecommendingResults.do?scenario=pcStoreJustForYou&storeId=3666081&offset=1&limit=25&callback=jsonp_1563685418340_83370'

    r = requests.get(url)
    products_dict = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
    result = []

    for prod in products_dict['results']:
        product_title, product_detail_url = prod['productTitle'], prod['productDetailUrl']
        # print(product_title, product_detail_url)
        if not product_detail_url.startswith('http'):
            product_detail_url = 'http:' + product_detail_url
        result.append(product_detail_url)
    return result


for i in get_prod_links():
    print(i)
    downloader(i)