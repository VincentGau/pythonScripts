import json

import requests

page = 1

url = 'https://avoscloud.com/1.1/call/getLikedWorks'


default_headers = {
    'X-LC-Id': '9pq709je4y36ubi10xphdpovula77enqrz27idozgry7x644',
    'X-LC-Prod': '1',
    'X-LC-Sign': '526c0efa5149a27e8a6cfa256cfeaca9,1579175579521',
    'X-LC-Session': 'hvpvveicnv6r9n8c1awyho08k'
}

while True:
    payload = {
        "perPage": 100,
        "page": page
    }
    result_dict = json.loads(requests.post(url=url, data=payload, headers=default_headers, verify=False).content)
    try:
        for i in result_dict['result']:
            print(i['workId'])
    except:
        break
    page += 1