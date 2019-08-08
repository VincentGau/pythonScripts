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

user = local_settings.ALIEX_USER
pwd = local_settings.ALIEX_PWD


class MyClass:
    def __init__(self):
        self.s = requests.session()
        self.certFile = "./123.crt"
        self.headers={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Sec-Fetch-Mode':'cors',
            'Pragma':'no-cache',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://ilogistics.aliexpress.com/recommendation_engine_internal.htm?spm=5261.order_list.aenewaside.10.41c53e5fnZ5gvK',
            'Cookie': 'ali_apache_id=10.103.166.15.1563590726812.350681.8; cna=Oyu7D4ouyVACAXOrRRCRcFiJ; aep_common_f=u8QFpxm0oh6/rYWKSO/lzqEtCS0JrO8FUzvkDGbHggZ0N6Oy00uWHg==; _ga=GA1.2.911908548.1563591492; _lang=zh_CN; _fbp=fb.1.1564239860576.352070620; UM_distinctid=16c57bdff0932c-071a65968f8049-c343162-1fa400-16c57bdff0a6fd; ali_beacon_id=10.103.166.15.1563590726812.350681.8; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0933061507270%0933060510377%094000043822258%094000047018951%094000022569251%0933056743091%094000045597013%0933055692051; _m_h5_tk=f459d95ce87afc4ef6ae11ced339fd20_1565238252576; _m_h5_tk_enc=1903068b8a2a625cdcf272546b1982ca; ali_apache_tracktmp=W_signed=Y; XSRF-TOKEN=775efbf2-bdc3-45de-8fa2-d1096808f591; acs_usuc_t=acs_rt=89495638c90d41e2a8b6beee74848de1&x_csrf=1awek74bt2xl4; ali_apache_track=mt=2|mid=cn1528697535hccf; _hvn_login=13; xman_us_t=x_lid=cn1528697535hccf&sign=y&x_user=u9nvNiH98IOg/EjiD1Yw6jsvHwZK/X5YKTadQ8PaZ9M=&ctoken=8l04vvn3mso8&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=AntxqVgk5JN1/8HW8VrxYBSqtB/KhW7CpR9xkVk4zlKhLt8Rs4sZQKFnrxvFuYG4nsX0hJsHriZpued+PjLfCI83DLR0xBjsfEouGgzmaVG6DDmVFvRopo9F3lJWvt2qyeG9NeN1PIikTEeERFtRdohRE41oEKEEog1I9GXWMO7o4i5pRUnUM7azF3J4yD9kK/ximxS34V9wiRGrz7d6sAG2PUS0MOXD/tv7DOqaxuCqBmzoU7HO9KkRzlVskBn8MUvK9r+FeqRovCzthJIyNGYhWCFwjmMQaxuqGFXltYN2caCjOne8bUmMsIfENTxMbZlQ1/I+c/+qRu8JxY90/K/1I07tMWM5Hi9fn4f6C6Y3yXr8pLQ4c6FXgATw/FubMn9h1O38Hr1V7j5COJa7CHb1kWhGj1F+ctGJqw/jdnjjmIPexUybVA==; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1563590771453&x_user=CN|Ying|Xia|cnfm|238871718&no_popup_today=n; intl_locale=en_US; aep_usuc_f=isfm=y&site=glo&c_tp=USD&x_alimid=238871718&iss=y&s_locale=zh_CN&region=US&b_locale=en_US; xman_t=VqLf27YJt5ivVsLhpm2K9678rapB06Md7MfBm6QvqwsnaIGDpcMaIyIc3wLh9XxVZAHHvs2vSWgZ0+MTcEFAEBYkhLK1YZQnzY5fAB7zvUdECv81GnYfTHoidXS3BTnmyEcJi5r23BMmWgYfF6j/4pvegMjMe533MZBujJf88NaJCmQ3naF6z8e/yu9y7akTTft9uv1ZUGECSEQ0+x3gnLsArw1uyEGo4SW+BHSht/IsPqPOXfWSw7HEPS2jbJvDyWIA4mx35wYbaZMw9yg4WvtoOX7XSaMTtcSnH08bQtFKO0eKtC7FdM0Wdz+TWnN5X9q4UDtDiGRp9Jz+aPlRGxeSKwe0rD/VPC6Gwpfn7c4/K92PWRISmkLAlZpJEv6pb5T+/WH1I+E67jygwjysnMWeLGbVrePOZhtGly0e/zYQGAopfVLfUUKBZH2QBOaEu4u9VVV+tk81kJPZhjeTWPLB4rJ6945r/V9TjP6TZ3Us7lLeIWU6+oDvxgH8AtOBPiVmFi+RW+eGcKMfyF91dzAc5oZtrq1sUz+IcOnIZipCSJfXxNYmSCtIqEiGU6O8cL5RzOkI8uPOF3kezv6AS6LbabqAWlj5MBZliURUJrheUrxj5WS/Rz2gUvdnxZ+Wk2mvkj8wYEzptgJUN1jOOXv/fFXGWMQbKDmYUagesHM4vMhKn0rELQ==; intl_common_forever=OdIR/b+XBmW6rZRBDTKDOyG7jlTBFWp4n/YXdU4/6Er6+PA3rEP87Q==; isg=BB0dKW_WHPdej_iiz967rSGzLPkXOlGMkZliDd_iWXSjlj3IpophXOsAxMo1VmlE; l=cBro8b8Rq_Bn3NMhBOCwourza77OSIRAguPzaNbMi_5ac6L1Ca7Ok5vEpFp6cjWdOuTp4aVvW6J9-etkiuVDCjB8ieSF',
            # 'Cookie': self.get_cookie(),
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
        if country_name == 'Country & Territories (A-Z)' or 'ther' in country_name:
            return
        order_amount = 1
        data = f'logistics-services-set=%2F&logistics-services-list-all=%5B%5BLjava.lang.String%3B%4092008f3%2C&logistics-class-filter=ALL&sort-by-recommend-points=0&sort-by-logistics-freight=0&toCountry={country}&fromCountry=CN&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY%23CAINIAO_SUPER_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY_SG%23CAINIAO_SUPER_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_ECONOMY%23YANWEN_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY_SG%23CAINIAO_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23SGP_OMP%23SGP_OMP%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_EXPEDITED_ECONOMY%23CAINIAO_EXPEDITED_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY%23CAINIAO_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_JYT%23YANWEN_JYT%23ECONOMY&logistics-express-item=CAINIAO%23SF_EPARCEL_OM%23SF_EPARCEL_OM%23ECONOMY&logistics-express-item=CAINIAO%23SUNYOU_ECONOMY%23SUNYOU_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23SINOTRANS_PY%23SINOTRANS_PY%23ECONOMY&logistics-express-item=AE%23E_PACKET%23EMS_ZX_ZX_US%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_SG%23CAINIAO_STANDARD_SG%23STANDARD&logistics-express-item=CAINIAO%23CPAM%23CPAM%23STANDARD&logistics-express-item=CAINIAO%23ITELLA%23ITELLA%23STANDARD&logistics-express-item=CAINIAO%23ZHONG_YOU_EUB_ONLINE%23ZHONG_YOU_EUB_ONLINE%23STANDARD&logistics-express-item=CAINIAO%23SGP%23SGP%23STANDARD&logistics-express-item=CAINIAO%23CPAM_HRB%23CPAM_HRB%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_G2G_DIRECTSHIP%23CAINIAO_G2G_DIRECTSHIP%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_CONSOLIDATION%23CAINIAO_CONSOLIDATION%23STANDARD&logistics-express-item=CAINIAO%23YANWEN_AM%23YANWEN_AM%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_HEAVY%23CAINIAO_STANDARD_HEAVY%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD%23CAINIAO_STANDARD%23STANDARD&logistics-express-item=CAINIAO%23AE_RU_MP_COURIER_PH3%23AE_RU_MP_COURIER_PH3%23STANDARD&logistics-express-item=STANDARD%23U_POST%23U_POST%23STANDARD&logistics-express-item=STANDARD%23PONY%23PONY%23STANDARD&logistics-express-item=STANDARD%23SEP%23SEP%23STANDARD&logistics-express-item=STANDARD%23FOURPX_RM%23FOURPX_RM%23STANDARD&logistics-express-item=STANDARD%23SFC%23SFC%23STANDARD&logistics-express-item=STANDARD%23CHUKOU1%23CHUKOU1%23STANDARD&logistics-express-item=STANDARD%23CTR_LAND_PICKUP%23CTR_LAND_PICKUP%23STANDARD&logistics-express-item=STANDARD%23UAPOST%23UAPOST%23STANDARD&logistics-express-item=STANDARD%23THPOST%23THPOST%23STANDARD&logistics-express-item=STANDARD%23GES%23GES%23STANDARD&logistics-express-item=STANDARD%23SF_EPARCEL%23SF_EPARCEL%23STANDARD&logistics-express-item=STANDARD%23TEA%23TEA%23STANDARD&logistics-express-item=STANDARD%23CHP%23CHP%23STANDARD&logistics-express-item=STANDARD%23CORREIOS_BR%23CORREIOS_BR%23STANDARD&logistics-express-item=STANDARD%23HUPOST%23HUPOST%23STANDARD&logistics-express-item=STANDARD%23CKE%23CKE%23STANDARD&logistics-express-item=STANDARD%23CNE%23CNE%23STANDARD&logistics-express-item=STANDARD%23TWPOST%23TWPOST%23STANDARD&logistics-express-item=STANDARD%23PTT%23PTT%23STANDARD&logistics-express-item=STANDARD%23MIUSON%23MIUSON%23STANDARD&logistics-express-item=STANDARD%23UBI%23UBI%23STANDARD&logistics-express-item=STANDARD%23JCEX%23JCEX%23STANDARD&logistics-express-item=STANDARD%23CHOICE%23CHOICE%23STANDARD&logistics-express-item=STANDARD%23YODEL%23YODEL%23STANDARD&logistics-express-item=STANDARD%23CJ%23CJ%23STANDARD&logistics-express-item=STANDARD%23VNPOST%23VNPOST%23STANDARD&logistics-express-item=STANDARD%23MEEST%23MEEST%23STANDARD&logistics-express-item=STANDARD%23DPD%23DPD%23STANDARD&logistics-express-item=STANDARD%23CPAP%23CPAP%23STANDARD&logistics-express-item=STANDARD%23SUNYOU_RM%23SUNYOU_RM%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_AE%23CAINIAO_CONSOLIDATION_AE%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_BE_STANDARD%23CAINIAO_BE_STANDARD%23STANDARD&logistics-express-item=STANDARD%23ASENDIA%23ASENDIA%23STANDARD&logistics-express-item=STANDARD%23FLYT%23FLYT%23STANDARD&logistics-express-item=STANDARD%23POST_NL%23POST_NL%23STANDARD&logistics-express-item=STANDARD%23POST_MY%23POST_MY%23STANDARD&logistics-express-item=STANDARD%23DHLECOM%23DHLECOM%23STANDARD&logistics-express-item=STANDARD%23Anjun_Tracked%23Anjun_Tracked%23STANDARD&logistics-express-item=STANDARD%23ONEWORLD%23ONEWORLD%23STANDARD&logistics-express-item=STANDARD%23BPOST%23BPOST%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_SA%23CAINIAO_CONSOLIDATION_SA%23STANDARD&logistics-express-item=STANDARD%23EKC%23EKC%23STANDARD&logistics-express-item=STANDARD%23HKPAM%23HKPAM%23STANDARD&logistics-express-item=STANDARD%23CDEK%23CDEK%23STANDARD&logistics-express-item=STANDARD%23ECONOMIC139%23ECONOMIC139%23STANDARD&logistics-express-item=STANDARD%23ARAMEX%23ARAMEX%23STANDARD&logistics-express-item=STANDARD%23NZPOST%23NZPOST%23STANDARD&logistics-express-item=STANDARD%23LAOPOST%23LAOPOST%23STANDARD&logistics-express-item=STANDARD%23POSTKR%23POSTKR%23STANDARD&logistics-express-item=STANDARD%23ETOTAL%23ETOTAL%23STANDARD&logistics-express-item=STANDARD%23CAPOST%23CAPOST%23STANDARD&logistics-express-item=WM%23FEDEX%23FEDEX%23EXPRESS&logistics-express-item=WM%23UPS%23UPS%23EXPRESS&logistics-express-item=WM%23DHL%23DHL%23EXPRESS&logistics-express-item=WM%23E_EMS%23E_EMS%23EXPRESS&logistics-express-item=WM%23EMS%23EMS%23EXPRESS&logistics-express-item=WM%23UPSE%23UPSE%23EXPRESS&logistics-express-item=WM%23TOLL%23TOLL%23EXPRESS&logistics-express-item=WM%23FEDEX_IE%23FEDEX_IE%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_STATION%23CAINIAO_STATION%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_PREMIUM%23CAINIAO_PREMIUM%23EXPRESS&logistics-express-item=STANDARD%23GATI%23GATI%23EXPRESS&logistics-express-item=STANDARD%23TNT%23TNT%23EXPRESS&logistics-express-item=STANDARD%23SPEEDPOST%23SPEEDPOST%23EXPRESS&logistics-express-item=STANDARD%23SPSR_CN%23SPSR_CN%23EXPRESS&logistics-express-item=STANDARD%23SF%23SF%23EXPRESS&limitedGoods=general&orderAmount={order_amount}&packageWeight={pkg_weight}&packageLength={pkg_length}&packageWidth={pkg_width}&packageHeight={pkg_height}'
        r = self.s.post(r'https://ilogistics.aliexpress.com/recommendationJsonPublic.do', data=data, headers=self.headers, verify=self.certFile)
        # print(r.text)
        j = json.loads(r.text)
        dd = json_normalize(j['logisticsServices'])
        try:
            # 保留服务名等四列数据
            dd = dd[['serviceName', 'recommendPoints', 'deliveryPeriod', 'freight']]
            # 删除运费未知的行
            dd = dd[dd['freight'] != '请咨询物流商']
            # 在第一列插入国家信息
            dd.insert(0, '国家', country_name)
            # print(dd)
            # dd.to_excel(f'{country}.xlsx', index=0)
            dd = dd.sort_values(by='freight', ascending=True)
            # print(dd)
            return dd
        except KeyError:
            print('ERROR ', country, country_name)




m = MyClass()
continents = ['AS', 'AF', 'NA', 'SA', 'EU', 'OA']
weight = 1.2
length = 10
width = 10
height = 10
# for c in continents:
#     result = pd.DataFrame()
#     for k, v in m.get_countries(c).items():
#         print(k, v)
#         result = result.append(m.get_freight(v, k,  weight, length, width, height))
#     result = result.sort_values(by='国家', ascending=True)
#     result.to_excel(f'output/{c}-{weight}-{length}-{width}-{height}.xlsx', index=0)
