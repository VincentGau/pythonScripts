#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import json
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.json import json_normalize

# cookies = driver.get_cookies()
# # print(cookies)
# pickle.dump(cookies, open("cookies.pickle", "wb"))
# cookies = pickle.load(open("cookies.pickle", "rb"))
s = requests.session()
# for cookie in cookies:
#     s.cookies.set(cookie['name'], cookie['value'])


headers={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    'Sec-Fetch-Mode':'cors',
    'Pragma':'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://ilogistics.aliexpress.com/recommendation_engine_internal.htm?spm=5261.order_list.aenewaside.10.41c53e5fnZ5gvK',
    'Cookie': 'ali_apache_id=10.103.166.15.1564575673547.177615.0; cna=unXIFU8aEwoCAXxA0zQnct2B; aep_common_f=v3qGXOp1GoXMhA/2VVDvFJf2Z4oEFQrkeqQ90IZZIk2dxi1BCQ16Yw==; _ga=GA1.2.1460708672.1564575686; _lang=zh_CN; _fbp=fb.1.1564581537949.1289620551; ali_beacon_id=10.103.166.15.1564575673547.177615.0; _gid=GA1.2.2102218627.1565009292; UM_distinctid=16c6697c305357-04289e78a2e922-3a65460c-384000-16c6697c30e28e; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000029219793%094000029579588%094000043032234%094000069147733%094000064789395%094000065883456%094000069147733%094000065883456; xman_us_f=x_l=1&x_locale=zh_CN&no_popup_today=n&x_user=CN|Ying|Xia|cnfm|238871718&zero_order=y&last_popup_time=1564575687325; intl_common_forever=DKrFrXGbqO1ex5k/XaS7K5Hk6Z/q6CjtxIwQ598mRulZFnR3Ejl/xA==; acs_usuc_t=x_csrf=1ahb91xizgkrs&acs_rt=ed8f9eaa986143c8a01425a0b40636d2; ali_apache_track=mt=2|mid=cn1528697535hccf; ali_apache_tracktmp=; _m_h5_tk=3f29a58c85ff6aa118b60e624ff6d43f_1565183745711; _m_h5_tk_enc=b6b56a4a3646e02412dee75f84717e7e; _hvn_login=13; aep_usuc_f=site=glo&region=CN&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&c_tp=USD&x_alimid=238871718; xman_us_t=x_lid=cn1528697535hccf&sign=y&x_user=81f5wK8D/WurmhxrFE+0LIuH15dhuFpJS0wD4XfflUE=&ctoken=lta862rv6q5i&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=ZCvWtiRWQIqn5MlMXGWc1iN9sq6gKcBvZXOR0w6X14ZaHQ+4/fo/6A/mRTCmtzEMaRSyofmkOWptGM+I8fYUzItKI1sBMz+iuiMFBC5YEcWUxlPt47twPnmHZH5irKrisHZ/izoV4gSi9p+z/3XkPyOLj4f+t0m3UVpZNQCpNNsUw+Bn9kLctKlj4Ym9RNs9f4HV+Tdf6Vs59/X/BbRGKK8TckNbWsG5rpJfOhj7FMvLtb95kn+6AuJ1nAvG8uKwbPS1RMqcWvgz7v70Dl4jVk862XaHEgzvg5NVlo4QwrlSa3S6tC/EBQCs++RHAuXipfGjvqlF4DWoM7Wz/Lhf2Bkixo4wgp0fohm72hyzbm2LLHyBh1QNKFmTr1BGnBuFvv/60mJwMaSFYqWi08EZsZz/hRCdhwTC8rJG4LgAwEUVJ2UW8FekSw==; xman_t=2qO9aaUfySo8yL78DoRBnJAOXLix6hvM1fsOjE6kWT+YBWXA+EIQ7DZbPzKr3OQBzwbyiy7JKZrjIbfxeMa6ZK1SXp2oka9PrfLcasNwbGrr4dlkqc3Dw3gU5bzgq8J2/0Q1j2re6vGT2oQp/+UcCuh82IgX2OjiBlscdVUx1oUHIuz/wFtiouOjxmOL/DO2esX9lJffQVcam7aizf4ycK020j0pkd+IxNQREgrajGwrYGJh8In5WtHUrHEHsgnRBsxbvt+q49OJ1hl2qBGryhgdpzrAEKWDE3J0/d3CYbX1SAzuequJJXFNOLbA6wdYTLHMku8UybUQ/fmdW4KC11ThBDejTKeIb5cwZrboGOi+weCIT0+//CAjJmYZ7ihiQfo/MWkNORwHeM5aCrzp9vasbLih3EsCTclTdEgEJevLkBwaCJ48lMrCLIh/yB6ApPmwLSmH99CjTI4sQe/rGVyxo1wYltPCmHaHLVeJf8AEvRUiIdj7DdcrergA5k/OQUUAJhCNFACZb4bqYkXFP1mBrkULWmcKz4Cc9ysO7xZcs8MOZu7fTtVhBK/B/8HrMr/Cv8fZb9BW83XQYqImuxZ2NNMFfXRV1onY7k46+exosVX64fHa7o2SWY5FggH3KtRZbmjlflvnagHmyxc+OAcTImhpFY2A+CLs4cmjTXdI8BIUzlv3oQ==; isg=BIKCdbSUaxfZQHfAe7xQS0qG04gk-4d9RsoZCsybwfWgHyOZtOOAfMVdy1vGT_4F; l=cBSQzz7gqbbLJKMoBOCNZuI8LI_OcIRfguPRwCbwi_5Qv1Y6-0bOk58i_ev6cjWhTd8B4jXUyweOfqK7JIz71dY2AkVC5',
}
print(s.cookies)

certFile = "./123.crt"
# r = s.get(r'https://ilogistics.aliexpress.com/areaJson.do?type=parent&country=CN&v=4317&_=1565148371272', headers=headers, verify=certFile)
# print(r.text)
print(s.cookies)


def lalala(country):
    order_amount = ''
    pkg_weight = 1.2
    pkg_length = 29
    pkg_width = 18
    pkg_height = 19
    data = f'_csrf_token_=1ahb91xizgkrs&logistics-services-set=%2F&logistics-services-list-all=%5B%5BLjava.lang.String%3B%4092008f3%2C&logistics-class-filter=ALL&sort-by-recommend-points=0&sort-by-logistics-freight=0&toCountry={country}&fromCountry=CN&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY%23CAINIAO_SUPER_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY_SG%23CAINIAO_SUPER_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_ECONOMY%23YANWEN_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY_SG%23CAINIAO_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23SGP_OMP%23SGP_OMP%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_EXPEDITED_ECONOMY%23CAINIAO_EXPEDITED_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY%23CAINIAO_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_JYT%23YANWEN_JYT%23ECONOMY&logistics-express-item=CAINIAO%23SF_EPARCEL_OM%23SF_EPARCEL_OM%23ECONOMY&logistics-express-item=CAINIAO%23SUNYOU_ECONOMY%23SUNYOU_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23SINOTRANS_PY%23SINOTRANS_PY%23ECONOMY&logistics-express-item=AE%23E_PACKET%23EMS_ZX_ZX_US%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_SG%23CAINIAO_STANDARD_SG%23STANDARD&logistics-express-item=CAINIAO%23CPAM%23CPAM%23STANDARD&logistics-express-item=CAINIAO%23ITELLA%23ITELLA%23STANDARD&logistics-express-item=CAINIAO%23ZHONG_YOU_EUB_ONLINE%23ZHONG_YOU_EUB_ONLINE%23STANDARD&logistics-express-item=CAINIAO%23SGP%23SGP%23STANDARD&logistics-express-item=CAINIAO%23CPAM_HRB%23CPAM_HRB%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_G2G_DIRECTSHIP%23CAINIAO_G2G_DIRECTSHIP%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_CONSOLIDATION%23CAINIAO_CONSOLIDATION%23STANDARD&logistics-express-item=CAINIAO%23YANWEN_AM%23YANWEN_AM%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_HEAVY%23CAINIAO_STANDARD_HEAVY%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD%23CAINIAO_STANDARD%23STANDARD&logistics-express-item=CAINIAO%23AE_RU_MP_COURIER_PH3%23AE_RU_MP_COURIER_PH3%23STANDARD&logistics-express-item=STANDARD%23U_POST%23U_POST%23STANDARD&logistics-express-item=STANDARD%23PONY%23PONY%23STANDARD&logistics-express-item=STANDARD%23SEP%23SEP%23STANDARD&logistics-express-item=STANDARD%23FOURPX_RM%23FOURPX_RM%23STANDARD&logistics-express-item=STANDARD%23SFC%23SFC%23STANDARD&logistics-express-item=STANDARD%23CHUKOU1%23CHUKOU1%23STANDARD&logistics-express-item=STANDARD%23CTR_LAND_PICKUP%23CTR_LAND_PICKUP%23STANDARD&logistics-express-item=STANDARD%23UAPOST%23UAPOST%23STANDARD&logistics-express-item=STANDARD%23THPOST%23THPOST%23STANDARD&logistics-express-item=STANDARD%23GES%23GES%23STANDARD&logistics-express-item=STANDARD%23SF_EPARCEL%23SF_EPARCEL%23STANDARD&logistics-express-item=STANDARD%23TEA%23TEA%23STANDARD&logistics-express-item=STANDARD%23CHP%23CHP%23STANDARD&logistics-express-item=STANDARD%23CORREIOS_BR%23CORREIOS_BR%23STANDARD&logistics-express-item=STANDARD%23HUPOST%23HUPOST%23STANDARD&logistics-express-item=STANDARD%23CKE%23CKE%23STANDARD&logistics-express-item=STANDARD%23CNE%23CNE%23STANDARD&logistics-express-item=STANDARD%23TWPOST%23TWPOST%23STANDARD&logistics-express-item=STANDARD%23PTT%23PTT%23STANDARD&logistics-express-item=STANDARD%23MIUSON%23MIUSON%23STANDARD&logistics-express-item=STANDARD%23UBI%23UBI%23STANDARD&logistics-express-item=STANDARD%23JCEX%23JCEX%23STANDARD&logistics-express-item=STANDARD%23CHOICE%23CHOICE%23STANDARD&logistics-express-item=STANDARD%23YODEL%23YODEL%23STANDARD&logistics-express-item=STANDARD%23CJ%23CJ%23STANDARD&logistics-express-item=STANDARD%23VNPOST%23VNPOST%23STANDARD&logistics-express-item=STANDARD%23MEEST%23MEEST%23STANDARD&logistics-express-item=STANDARD%23DPD%23DPD%23STANDARD&logistics-express-item=STANDARD%23CPAP%23CPAP%23STANDARD&logistics-express-item=STANDARD%23SUNYOU_RM%23SUNYOU_RM%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_AE%23CAINIAO_CONSOLIDATION_AE%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_BE_STANDARD%23CAINIAO_BE_STANDARD%23STANDARD&logistics-express-item=STANDARD%23ASENDIA%23ASENDIA%23STANDARD&logistics-express-item=STANDARD%23FLYT%23FLYT%23STANDARD&logistics-express-item=STANDARD%23POST_NL%23POST_NL%23STANDARD&logistics-express-item=STANDARD%23POST_MY%23POST_MY%23STANDARD&logistics-express-item=STANDARD%23DHLECOM%23DHLECOM%23STANDARD&logistics-express-item=STANDARD%23Anjun_Tracked%23Anjun_Tracked%23STANDARD&logistics-express-item=STANDARD%23ONEWORLD%23ONEWORLD%23STANDARD&logistics-express-item=STANDARD%23BPOST%23BPOST%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_SA%23CAINIAO_CONSOLIDATION_SA%23STANDARD&logistics-express-item=STANDARD%23EKC%23EKC%23STANDARD&logistics-express-item=STANDARD%23HKPAM%23HKPAM%23STANDARD&logistics-express-item=STANDARD%23CDEK%23CDEK%23STANDARD&logistics-express-item=STANDARD%23ECONOMIC139%23ECONOMIC139%23STANDARD&logistics-express-item=STANDARD%23ARAMEX%23ARAMEX%23STANDARD&logistics-express-item=STANDARD%23NZPOST%23NZPOST%23STANDARD&logistics-express-item=STANDARD%23LAOPOST%23LAOPOST%23STANDARD&logistics-express-item=STANDARD%23POSTKR%23POSTKR%23STANDARD&logistics-express-item=STANDARD%23ETOTAL%23ETOTAL%23STANDARD&logistics-express-item=STANDARD%23CAPOST%23CAPOST%23STANDARD&logistics-express-item=WM%23FEDEX%23FEDEX%23EXPRESS&logistics-express-item=WM%23UPS%23UPS%23EXPRESS&logistics-express-item=WM%23DHL%23DHL%23EXPRESS&logistics-express-item=WM%23E_EMS%23E_EMS%23EXPRESS&logistics-express-item=WM%23EMS%23EMS%23EXPRESS&logistics-express-item=WM%23UPSE%23UPSE%23EXPRESS&logistics-express-item=WM%23TOLL%23TOLL%23EXPRESS&logistics-express-item=WM%23FEDEX_IE%23FEDEX_IE%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_STATION%23CAINIAO_STATION%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_PREMIUM%23CAINIAO_PREMIUM%23EXPRESS&logistics-express-item=STANDARD%23GATI%23GATI%23EXPRESS&logistics-express-item=STANDARD%23TNT%23TNT%23EXPRESS&logistics-express-item=STANDARD%23SPEEDPOST%23SPEEDPOST%23EXPRESS&logistics-express-item=STANDARD%23SPSR_CN%23SPSR_CN%23EXPRESS&logistics-express-item=STANDARD%23SF%23SF%23EXPRESS&limitedGoods=general&orderAmount={order_amount}&packageWeight={pkg_weight}&packageLength={pkg_length}&packageWidth={pkg_width}&packageHeight={pkg_height}'
    r = s.post(r'https://ilogistics.aliexpress.com/recommendationJsonPublic.do', data=data, headers=headers, verify=certFile)
    print(r.text)
    j = json.loads(r.text)
    for i in j['logisticsServices']:
        if(not i['freight'] == '请咨询物流商'):
            print(i['serviceName'].ljust(40), i['recommendPoints'].ljust(20), i['deliveryPeriod'].ljust(20), i['freight'].ljust(20))
    dd = json_normalize(j['logisticsServices'])
    print(dd)
    # 保留服务名等四列数据
    dd = dd[['serviceName', 'recommendPoints', 'deliveryPeriod', 'freight']]
    # 删除运费位置的行
    dd = dd[dd['freight'] != '请咨询物流商']
    # 在第一列插入国家信息
    dd.insert(0, '国家', 'RU')
    print(dd)
    dd.to_excel(f'{country}.xlsx', index=0)

# lalala('RU')

# r = s.get('https://ilogistics.aliexpress.com/recommendation_engine_internal.htm')
# soup = BeautifulSoup(r.text, 'lxml')
# to_country = soup.find('select', id='select-dest-country')
# ccc = to_country.find_all('option')
# for c in ccc:
#     print(c.text, c["value"])


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
            'Cookie': 'ali_apache_id=10.103.166.15.1564575673547.177615.0; cna=unXIFU8aEwoCAXxA0zQnct2B; aep_common_f=v3qGXOp1GoXMhA/2VVDvFJf2Z4oEFQrkeqQ90IZZIk2dxi1BCQ16Yw==; _ga=GA1.2.1460708672.1564575686; _lang=zh_CN; _fbp=fb.1.1564581537949.1289620551; ali_beacon_id=10.103.166.15.1564575673547.177615.0; _gid=GA1.2.2102218627.1565009292; UM_distinctid=16c6697c305357-04289e78a2e922-3a65460c-384000-16c6697c30e28e; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094000029219793%094000029579588%094000043032234%094000069147733%094000064789395%094000065883456%094000069147733%094000065883456; xman_us_f=x_l=1&x_locale=zh_CN&no_popup_today=n&x_user=CN|Ying|Xia|cnfm|238871718&zero_order=y&last_popup_time=1564575687325; intl_common_forever=DKrFrXGbqO1ex5k/XaS7K5Hk6Z/q6CjtxIwQ598mRulZFnR3Ejl/xA==; acs_usuc_t=x_csrf=1ahb91xizgkrs&acs_rt=ed8f9eaa986143c8a01425a0b40636d2; ali_apache_track=mt=2|mid=cn1528697535hccf; ali_apache_tracktmp=; _m_h5_tk=3f29a58c85ff6aa118b60e624ff6d43f_1565183745711; _m_h5_tk_enc=b6b56a4a3646e02412dee75f84717e7e; _hvn_login=13; aep_usuc_f=site=glo&region=CN&b_locale=en_US&iss=y&s_locale=zh_CN&isfm=y&c_tp=USD&x_alimid=238871718; xman_us_t=x_lid=cn1528697535hccf&sign=y&x_user=81f5wK8D/WurmhxrFE+0LIuH15dhuFpJS0wD4XfflUE=&ctoken=lta862rv6q5i&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; xman_f=ZCvWtiRWQIqn5MlMXGWc1iN9sq6gKcBvZXOR0w6X14ZaHQ+4/fo/6A/mRTCmtzEMaRSyofmkOWptGM+I8fYUzItKI1sBMz+iuiMFBC5YEcWUxlPt47twPnmHZH5irKrisHZ/izoV4gSi9p+z/3XkPyOLj4f+t0m3UVpZNQCpNNsUw+Bn9kLctKlj4Ym9RNs9f4HV+Tdf6Vs59/X/BbRGKK8TckNbWsG5rpJfOhj7FMvLtb95kn+6AuJ1nAvG8uKwbPS1RMqcWvgz7v70Dl4jVk862XaHEgzvg5NVlo4QwrlSa3S6tC/EBQCs++RHAuXipfGjvqlF4DWoM7Wz/Lhf2Bkixo4wgp0fohm72hyzbm2LLHyBh1QNKFmTr1BGnBuFvv/60mJwMaSFYqWi08EZsZz/hRCdhwTC8rJG4LgAwEUVJ2UW8FekSw==; xman_t=2qO9aaUfySo8yL78DoRBnJAOXLix6hvM1fsOjE6kWT+YBWXA+EIQ7DZbPzKr3OQBzwbyiy7JKZrjIbfxeMa6ZK1SXp2oka9PrfLcasNwbGrr4dlkqc3Dw3gU5bzgq8J2/0Q1j2re6vGT2oQp/+UcCuh82IgX2OjiBlscdVUx1oUHIuz/wFtiouOjxmOL/DO2esX9lJffQVcam7aizf4ycK020j0pkd+IxNQREgrajGwrYGJh8In5WtHUrHEHsgnRBsxbvt+q49OJ1hl2qBGryhgdpzrAEKWDE3J0/d3CYbX1SAzuequJJXFNOLbA6wdYTLHMku8UybUQ/fmdW4KC11ThBDejTKeIb5cwZrboGOi+weCIT0+//CAjJmYZ7ihiQfo/MWkNORwHeM5aCrzp9vasbLih3EsCTclTdEgEJevLkBwaCJ48lMrCLIh/yB6ApPmwLSmH99CjTI4sQe/rGVyxo1wYltPCmHaHLVeJf8AEvRUiIdj7DdcrergA5k/OQUUAJhCNFACZb4bqYkXFP1mBrkULWmcKz4Cc9ysO7xZcs8MOZu7fTtVhBK/B/8HrMr/Cv8fZb9BW83XQYqImuxZ2NNMFfXRV1onY7k46+exosVX64fHa7o2SWY5FggH3KtRZbmjlflvnagHmyxc+OAcTImhpFY2A+CLs4cmjTXdI8BIUzlv3oQ==; isg=BIKCdbSUaxfZQHfAe7xQS0qG04gk-4d9RsoZCsybwfWgHyOZtOOAfMVdy1vGT_4F; l=cBSQzz7gqbbLJKMoBOCNZuI8LI_OcIRfguPRwCbwi_5Qv1Y6-0bOk58i_ev6cjWhTd8B4jXUyweOfqK7JIz71dY2AkVC5',
        }
        # self.countries = self.get_countries()
        # self.countries = {'RU': 'Russian', 'US': 'United States'}

    def get_countries(self):
        dict = {}
        r = self.s.get('https://ilogistics.aliexpress.com/recommendation_engine_internal.htm', headers=self.headers, verify=self.certFile)
        soup = BeautifulSoup(r.text, 'lxml')
        to_country = soup.find('select', id='select-dest-country')
        ccc = to_country.find_all('option')
        for c in ccc:
            print(c.text, c["value"])
            dict[c.text] = c['value']
        return dict

    def get_freight(self, country, country_name, pkg_weight, pkg_length, pkg_width, pkg_height):
        if(country_name == 'Country & Territories (A-Z)' or 'ther' in country_name):
            return
        order_amount = 1
        data = f'_csrf_token_=1ahb91xizgkrs&logistics-services-set=%2F&logistics-services-list-all=%5B%5BLjava.lang.String%3B%4092008f3%2C&logistics-class-filter=ALL&sort-by-recommend-points=0&sort-by-logistics-freight=0&toCountry={country}&fromCountry=CN&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY%23CAINIAO_SUPER_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_SUPER_ECONOMY_SG%23CAINIAO_SUPER_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_ECONOMY%23YANWEN_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY_SG%23CAINIAO_ECONOMY_SG%23ECONOMY&logistics-express-item=CAINIAO%23SGP_OMP%23SGP_OMP%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_EXPEDITED_ECONOMY%23CAINIAO_EXPEDITED_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23CAINIAO_ECONOMY%23CAINIAO_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23YANWEN_JYT%23YANWEN_JYT%23ECONOMY&logistics-express-item=CAINIAO%23SF_EPARCEL_OM%23SF_EPARCEL_OM%23ECONOMY&logistics-express-item=CAINIAO%23SUNYOU_ECONOMY%23SUNYOU_ECONOMY%23ECONOMY&logistics-express-item=CAINIAO%23SINOTRANS_PY%23SINOTRANS_PY%23ECONOMY&logistics-express-item=AE%23E_PACKET%23EMS_ZX_ZX_US%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_SG%23CAINIAO_STANDARD_SG%23STANDARD&logistics-express-item=CAINIAO%23CPAM%23CPAM%23STANDARD&logistics-express-item=CAINIAO%23ITELLA%23ITELLA%23STANDARD&logistics-express-item=CAINIAO%23ZHONG_YOU_EUB_ONLINE%23ZHONG_YOU_EUB_ONLINE%23STANDARD&logistics-express-item=CAINIAO%23SGP%23SGP%23STANDARD&logistics-express-item=CAINIAO%23CPAM_HRB%23CPAM_HRB%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_G2G_DIRECTSHIP%23CAINIAO_G2G_DIRECTSHIP%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_CONSOLIDATION%23CAINIAO_CONSOLIDATION%23STANDARD&logistics-express-item=CAINIAO%23YANWEN_AM%23YANWEN_AM%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD_HEAVY%23CAINIAO_STANDARD_HEAVY%23STANDARD&logistics-express-item=CAINIAO%23CAINIAO_STANDARD%23CAINIAO_STANDARD%23STANDARD&logistics-express-item=CAINIAO%23AE_RU_MP_COURIER_PH3%23AE_RU_MP_COURIER_PH3%23STANDARD&logistics-express-item=STANDARD%23U_POST%23U_POST%23STANDARD&logistics-express-item=STANDARD%23PONY%23PONY%23STANDARD&logistics-express-item=STANDARD%23SEP%23SEP%23STANDARD&logistics-express-item=STANDARD%23FOURPX_RM%23FOURPX_RM%23STANDARD&logistics-express-item=STANDARD%23SFC%23SFC%23STANDARD&logistics-express-item=STANDARD%23CHUKOU1%23CHUKOU1%23STANDARD&logistics-express-item=STANDARD%23CTR_LAND_PICKUP%23CTR_LAND_PICKUP%23STANDARD&logistics-express-item=STANDARD%23UAPOST%23UAPOST%23STANDARD&logistics-express-item=STANDARD%23THPOST%23THPOST%23STANDARD&logistics-express-item=STANDARD%23GES%23GES%23STANDARD&logistics-express-item=STANDARD%23SF_EPARCEL%23SF_EPARCEL%23STANDARD&logistics-express-item=STANDARD%23TEA%23TEA%23STANDARD&logistics-express-item=STANDARD%23CHP%23CHP%23STANDARD&logistics-express-item=STANDARD%23CORREIOS_BR%23CORREIOS_BR%23STANDARD&logistics-express-item=STANDARD%23HUPOST%23HUPOST%23STANDARD&logistics-express-item=STANDARD%23CKE%23CKE%23STANDARD&logistics-express-item=STANDARD%23CNE%23CNE%23STANDARD&logistics-express-item=STANDARD%23TWPOST%23TWPOST%23STANDARD&logistics-express-item=STANDARD%23PTT%23PTT%23STANDARD&logistics-express-item=STANDARD%23MIUSON%23MIUSON%23STANDARD&logistics-express-item=STANDARD%23UBI%23UBI%23STANDARD&logistics-express-item=STANDARD%23JCEX%23JCEX%23STANDARD&logistics-express-item=STANDARD%23CHOICE%23CHOICE%23STANDARD&logistics-express-item=STANDARD%23YODEL%23YODEL%23STANDARD&logistics-express-item=STANDARD%23CJ%23CJ%23STANDARD&logistics-express-item=STANDARD%23VNPOST%23VNPOST%23STANDARD&logistics-express-item=STANDARD%23MEEST%23MEEST%23STANDARD&logistics-express-item=STANDARD%23DPD%23DPD%23STANDARD&logistics-express-item=STANDARD%23CPAP%23CPAP%23STANDARD&logistics-express-item=STANDARD%23SUNYOU_RM%23SUNYOU_RM%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_AE%23CAINIAO_CONSOLIDATION_AE%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_BE_STANDARD%23CAINIAO_BE_STANDARD%23STANDARD&logistics-express-item=STANDARD%23ASENDIA%23ASENDIA%23STANDARD&logistics-express-item=STANDARD%23FLYT%23FLYT%23STANDARD&logistics-express-item=STANDARD%23POST_NL%23POST_NL%23STANDARD&logistics-express-item=STANDARD%23POST_MY%23POST_MY%23STANDARD&logistics-express-item=STANDARD%23DHLECOM%23DHLECOM%23STANDARD&logistics-express-item=STANDARD%23Anjun_Tracked%23Anjun_Tracked%23STANDARD&logistics-express-item=STANDARD%23ONEWORLD%23ONEWORLD%23STANDARD&logistics-express-item=STANDARD%23BPOST%23BPOST%23STANDARD&logistics-express-item=STANDARD%23CAINIAO_CONSOLIDATION_SA%23CAINIAO_CONSOLIDATION_SA%23STANDARD&logistics-express-item=STANDARD%23EKC%23EKC%23STANDARD&logistics-express-item=STANDARD%23HKPAM%23HKPAM%23STANDARD&logistics-express-item=STANDARD%23CDEK%23CDEK%23STANDARD&logistics-express-item=STANDARD%23ECONOMIC139%23ECONOMIC139%23STANDARD&logistics-express-item=STANDARD%23ARAMEX%23ARAMEX%23STANDARD&logistics-express-item=STANDARD%23NZPOST%23NZPOST%23STANDARD&logistics-express-item=STANDARD%23LAOPOST%23LAOPOST%23STANDARD&logistics-express-item=STANDARD%23POSTKR%23POSTKR%23STANDARD&logistics-express-item=STANDARD%23ETOTAL%23ETOTAL%23STANDARD&logistics-express-item=STANDARD%23CAPOST%23CAPOST%23STANDARD&logistics-express-item=WM%23FEDEX%23FEDEX%23EXPRESS&logistics-express-item=WM%23UPS%23UPS%23EXPRESS&logistics-express-item=WM%23DHL%23DHL%23EXPRESS&logistics-express-item=WM%23E_EMS%23E_EMS%23EXPRESS&logistics-express-item=WM%23EMS%23EMS%23EXPRESS&logistics-express-item=WM%23UPSE%23UPSE%23EXPRESS&logistics-express-item=WM%23TOLL%23TOLL%23EXPRESS&logistics-express-item=WM%23FEDEX_IE%23FEDEX_IE%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_STATION%23CAINIAO_STATION%23EXPRESS&logistics-express-item=CAINIAO%23CAINIAO_PREMIUM%23CAINIAO_PREMIUM%23EXPRESS&logistics-express-item=STANDARD%23GATI%23GATI%23EXPRESS&logistics-express-item=STANDARD%23TNT%23TNT%23EXPRESS&logistics-express-item=STANDARD%23SPEEDPOST%23SPEEDPOST%23EXPRESS&logistics-express-item=STANDARD%23SPSR_CN%23SPSR_CN%23EXPRESS&logistics-express-item=STANDARD%23SF%23SF%23EXPRESS&limitedGoods=general&orderAmount={order_amount}&packageWeight={pkg_weight}&packageLength={pkg_length}&packageWidth={pkg_width}&packageHeight={pkg_height}'
        r = self.s.post(r'https://ilogistics.aliexpress.com/recommendationJsonPublic.do', data=data, headers=self.headers, verify=self.certFile)
        print(r.text)
        j = json.loads(r.text)

        dd = json_normalize(j['logisticsServices'])
        # print(dd)
        # 保留服务名等四列数据
        dd = dd[['serviceName', 'recommendPoints', 'deliveryPeriod', 'freight']]
        # 删除运费位置的行
        dd = dd[dd['freight'] != '请咨询物流商']
        # 在第一列插入国家信息
        dd.insert(0, '国家', country_name)
        # print(dd)
        # dd.to_excel(f'{country}.xlsx', index=0)
        return dd


m = MyClass()
# m.get_countries()
result = pd.DataFrame()
for k, v in m.get_countries().items():
    print(k, v)
    result = result.append(m.get_freight(v, k,  1.2, 10, 10, 10))

result.to_excel(f'123.xlsx', index=0)
