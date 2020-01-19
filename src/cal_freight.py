#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.json import json_normalize
from src import local_settings
from selenium import webdriver
import requests
import numpy as np
import time

user = local_settings.ALIEX_USER
pwd = local_settings.ALIEX_PWD


class MyClass:
    def __init__(self):
        self.s = requests.session()
        # self.certFile = "depend/123.crt"
        self.certFile = None
        self.headers={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Sec-Fetch-Mode':'cors',
            'Pragma':'no-cache',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://ilogistics.aliexpress.com/recommendation_engine_internal.htm?spm=5261.order_list.aenewaside.10.41c53e5fnZ5gvK',
            'Cookie': self.get_cookie(),
        }

        if not os.path.exists('output'):
            print("making output dir...")
            os.makedirs('output')
        # self.countries = self.get_countries()
        # self.countries = {'RU': 'Russian', 'US': 'United States'}

    def get_cookie(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                                  chrome_options=options)

        driver.get("https://login.aliexpress.com/")

        frame = driver.find_element_by_id("alibaba-login-box")
        driver.switch_to.frame(frame)

        driver.find_element_by_id("fm-login-id").send_keys(user)
        driver.find_element_by_id("fm-login-password").clear()
        driver.find_element_by_id("fm-login-password").send_keys(pwd)
        driver.find_element_by_class_name("fm-submit").click()
        # 等待cookie完整
        time.sleep(2)
        cookies = driver.get_cookies()
        cookee = ''
        for cookie in cookies:
            cookee += f"{cookie['name']}={cookie['value']};"
        print(cookee)
        return cookee

    def get_countries(self, continent):
        '''
        预先将运费模板中6个大洲的国家存在文本中，根据大洲分组计算运费
        :param continent:
        :return:
        '''
        dict = {}
        country_list = []
        if not os.path.exists('depend/Countries.txt'):
            self.get_all_countries()
        print(f'depend/{continent}.txt')
        with open(f'depend/{continent}.txt', encoding='utf-8') as f:
            for line in f:
                country_list.append(' '.join(line.split(' ')[:-1]))
        r = self.s.get('https://ilogistics.aliexpress.com/recommendation_engine_internal.htm', headers=self.headers, verify=self.certFile)
        soup = BeautifulSoup(r.text, 'lxml')
        to_country = soup.find('select', id='select-dest-country')
        ccc = to_country.find_all('option')
        for cc in ccc:
            # print(cc.text, cc["value"])
            if cc.text in country_list:
                dict[cc.text] = cc['value']
        return dict

    def get_all_countries(self):
        '''
        从运费计算页下拉框中获取到所有国家，写入文本
        :return:
        '''
        r = self.s.get('https://ilogistics.aliexpress.com/recommendation_engine_internal.htm', headers=self.headers, verify=self.certFile)
        soup = BeautifulSoup(r.text, 'lxml')
        to_country = soup.find('select', id='select-dest-country')
        ccc = to_country.find_all('option')

        with open('depend/Countries.txt', 'w', encoding='UTF-8') as f:
            for cc in ccc:
                f.write(f'{cc.text} {cc["value"]}\n')

    def get_freight(self, country, country_name, pkg_weight, pkg_length, pkg_width, pkg_height):
        if country_name in ['Country & Territories (A-Z)', 'other', 'Other']:
            return
        order_amount = 100
        data = f'logistics-services-set=%2F&logistics-services-list-all=%5B%5BLjava.lang.String%3B%4092008f3%2C&logistics-class-filter=ALL&sort-by-recommend-points=0&sort-by-logistics-freight=0&toCountry={country}&fromCountry=CN&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY%23CAINIAO_SUPER_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY_SG%23CAINIAO_SUPER_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_ECONOMY%23YANWEN_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY_SG%23CAINIAO_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23SGP_OMP%23SGP_OMP%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_EXPEDITED_ECONOMY%23CAINIAO_EXPEDITED_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY%23CAINIAO_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_JYT%23YANWEN_JYT%23ECONOMY&logistics-express-item=CAINIAO%23SF_EPARCEL_OM%23SF_EPARCEL_OM%23ECONOMY&logistics-express-item=CAINIAO%23SUNYOU_ECONOMY%23SUNYOU_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23SINOTRANS_PY%23SINOTRANS_PY%23ECONOMY&logistics-express-item=AE%23E_PACKET%23EMS_ZX_ZX_US%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_SG%23CAINIAO_STANDARD_SG%23STANDARD&logistics-express-item=CAINIAO%23CPAM%23CPAM%23STANDARD&logistics-express-item=CAINIAO%23ITELLA%23ITELLA%23STANDARD&logistics-express-item=CAINIAO%23ZHONG_YOU_EUB_ONLINE%23ZHONG_YOU_EUB_ONLINE%23STANDARD&logistics-express-item=CAINIAO%23SGP%23SGP%23STANDARD&logistics-express-item=CAINIAO%23CPAM_HRB%23CPAM_HRB%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_G2G_DIRECTSHIP%23CAINIAO_G2G_DIRECTSHIP%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_CONSOLIDATION%23CAINIAO_CONSOLIDATION%23STANDARD&logistics-express-item=CAINIAO%23YANWEN_AM%23YANWEN_AM%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_HEAVY%23CAINIAO_STANDARD_HEAVY%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD%23CAINIAO_STANDARD%23STANDARD&logistics-express-item=CAINIAO%23AE_RU_MP_COURIER_PH3%23AE_RU_MP_COURIER_PH3%23STANDARD&logistics-express-item=STANDARD%23U_POST%23U_POST%23STANDARD&logistics-express-item=STANDARD%23PONY%23PONY%23STANDARD&logistics-express-item=STANDARD%23SEP%23SEP%23STANDARD&logistics-express-item=STANDARD%23FOURPX_RM%23FOURPX_RM%23STANDARD&logistics-express-item=STANDARD%23SFC%23SFC%23STANDARD&logistics-express-item=STANDARD%23CHUKOU1%23CHUKOU1%23STANDARD&logistics-express-item=STANDARD%23CTR_LAND_PICKUP%23CTR_LAND_PICKUP%23STANDARD&logistics-express-item=STANDARD%23UAPOST%23UAPOST%23STANDARD&logistics-express-item=STANDARD%23THPOST%23THPOST%23STANDARD&logistics-express-item=STANDARD%23GES%23GES%23STANDARD&logistics-express-item=STANDARD%23SF_EPARCEL%23SF_EPARCEL%23STANDARD&logistics-express-item=STANDARD%23TEA%23TEA%23STANDARD&logistics-express-item=STANDARD%23CHP%23CHP%23STANDARD&logistics-express-item=STANDARD%23CORREIOS_BR%23CORREIOS_BR%23STANDARD&logistics-express-item=STANDARD%23HUPOST%23HUPOST%23STANDARD&logistics-express-item=STANDARD%23CKE%23CKE%23STANDARD&logistics-express-item=STANDARD%23CNE%23CNE%23STANDARD&logistics-express-item=STANDARD%23TWPOST%23TWPOST%23STANDARD&logistics-express-item=STANDARD%23PTT%23PTT%23STANDARD&logistics-express-item=STANDARD%23MIUSON%23MIUSON%23STANDARD&logistics-express-item=STANDARD%23UBI%23UBI%23STANDARD&logistics-express-item=STANDARD%23JCEX%23JCEX%23STANDARD&logistics-express-item=STANDARD%23CHOICE%23CHOICE%23STANDARD&logistics-express-item=STANDARD%23YODEL%23YODEL%23STANDARD&logistics-express-item=STANDARD%23CJ%23CJ%23STANDARD&logistics-express-item=STANDARD%23VNPOST%23VNPOST%23STANDARD&logistics-express-item=STANDARD%23MEEST%23MEEST%23STANDARD&logistics-express-item=STANDARD%23DPD%23DPD%23STANDARD&logistics-express-item=STANDARD%23CPAP%23CPAP%23STANDARD&logistics-express-item=STANDARD%23SUNYOU_RM%23SUNYOU_RM%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_AE%23CAINIAO_CONSOLIDATION_AE%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_BE_STANDARD%23CAINIAO_BE_STANDARD%23STANDARD&logistics-express-item=STANDARD%23ASENDIA%23ASENDIA%23STANDARD&logistics-express-item=STANDARD%23FLYT%23FLYT%23STANDARD&logistics-express-item=STANDARD%23POST_NL%23POST_NL%23STANDARD&logistics-express-item=STANDARD%23POST_MY%23POST_MY%23STANDARD&logistics-express-item=STANDARD%23DHLECOM%23DHLECOM%23STANDARD&logistics-express-item=STANDARD%23Anjun_Tracked%23Anjun_Tracked%23STANDARD&logistics-express-item=STANDARD%23ONEWORLD%23ONEWORLD%23STANDARD&logistics-express-item=STANDARD%23BPOST%23BPOST%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_SA%23CAINIAO_CONSOLIDATION_SA%23STANDARD&logistics-express-item=STANDARD%23EKC%23EKC%23STANDARD&logistics-express-item=STANDARD%23HKPAM%23HKPAM%23STANDARD&logistics-express-item=STANDARD%23CDEK%23CDEK%23STANDARD&logistics-express-item=STANDARD%23ECONOMIC139%23ECONOMIC139%23STANDARD&logistics-express-item=STANDARD%23ARAMEX%23ARAMEX%23STANDARD&logistics-express-item=STANDARD%23NZPOST%23NZPOST%23STANDARD&logistics-express-item=STANDARD%23LAOPOST%23LAOPOST%23STANDARD&logistics-express-item=STANDARD%23POSTKR%23POSTKR%23STANDARD&logistics-express-item=STANDARD%23ETOTAL%23ETOTAL%23STANDARD&logistics-express-item=STANDARD%23CAPOST%23CAPOST%23STANDARD&logistics-express-item=WM%23FEDEX%23FEDEX%23EXPRESS&logistics-express-item=WM%23UPS%23UPS%23EXPRESS&logistics-express-item=WM%23DHL%23DHL%23EXPRESS&logistics-express-item=WM%23E_EMS%23E_EMS%23EXPRESS&logistics-express-item=WM%23EMS%23EMS%23EXPRESS&logistics-express-item=WM%23UPSE%23UPSE%23EXPRESS&logistics-express-item=WM%23TOLL%23TOLL%23EXPRESS&logistics-express-item=WM%23FEDEX_IE%23FEDEX_IE%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_STATION%23CAINIAO_STATION%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_PREMIUM%23CAINIAO_PREMIUM%23EXPRESS&logistics-express-item=STANDARD%23GATI%23GATI%23EXPRESS&logistics-express-item=STANDARD%23TNT%23TNT%23EXPRESS&logistics-express-item=STANDARD%23SPEEDPOST%23SPEEDPOST%23EXPRESS&logistics-express-item=STANDARD%23SPSR_CN%23SPSR_CN%23EXPRESS&logistics-express-item=STANDARD%23SF%23SF%23EXPRESS&limitedGoods=electric&orderAmount={order_amount}&packageWeight={pkg_weight}&packageLength={pkg_length}&packageWidth={pkg_width}&packageHeight={pkg_height}'
        r = self.s.post(r'https://ilogistics.aliexpress.com/recommendationJsonPublic.do', data=data, headers=self.headers, verify=self.certFile)
        # print(r.text)
        j = json.loads(r.text)
        dd = json_normalize(j['logisticsServices'])
        try:
            # 保留服务名等四列数据
            dd = dd[['serviceName', 'recommendPoints', 'deliveryPeriod', 'freight']]
            # 删除运费未知的行
            dd = dd[dd['freight'] != '请咨询物流商']
            # 删除serviceName为TNT的行
            dd = dd[dd['serviceName'] != 'TNT']
            # 去掉运费的CN￥前缀，去掉价格中的逗号，并转换为float类型，保留两位小数
            dd['freight'] = dd['freight'].str[3:]
            dd['freight'] = dd['freight'].str.replace(',', '').astype('float').round(2)
            # 在第一列插入国家信息
            dd.insert(0, '国家', country_name)
            return dd
        except KeyError:
            print('ERROR ', country, country_name)


m = MyClass()
continents = ['AS', 'AF', 'NA', 'SA', 'EU', 'OA']
# continents = ['AS']
weight = 2
length = 30
width = 16
height = 10

with pd.ExcelWriter(f'output/{weight}-{length}-{width}-{height}.xlsx') as writer:
    for c in continents:
        result = pd.DataFrame()
        for k, v in m.get_countries(c).items():
            print(k, v)
            result = result.append(m.get_freight(v, k,  weight, length, width, height))
        result = result.sort_values(by=['国家', 'freight'], ascending=True)

        # 按分组填充flag值，奇数组0，偶数组1
        result['flag'] = np.where(result['国家'] == result['国家'].shift(-1), 0, 1) # just test
        start_index = 0
        gnumber = 0
        for s in result.groupby('国家').size():
            result['flag'][start_index:start_index+s] = gnumber % 2
            gnumber += 1
            start_index += s

        # 不保留小数位
        result.to_excel(writer, sheet_name=c, index=0, float_format='%.0f')
