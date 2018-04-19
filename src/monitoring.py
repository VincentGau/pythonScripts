"""
Monitor sites status. Email if sites not accessible.
"""
import json
import multiprocessing

import requests


def check_site(site):
    """
    Check site usability.

    Check status code;
    Check whether specific keywords exist in the page content;

    :param site:
    :return:
    """
    url, keywords, bad_words = site['url'], site['keywords'], site['bad_words']
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers)

        if r.status_code != 200:
            print('f{url} status code: {r.status_code}.')
            return False

        # should be there and not exist
        absent_words = [k for k in keywords if k not in r.text]
        # should not be there and it appears
        unexpected_words = [k for k in bad_words if k in r.text]

        if absent_words or unexpected_words:
            print(f'{url} failed.')
            # print(
            #     f'--should not be there and it appears: {unexpected_words}\n\
            #     --should be there and not exist: {absent_words}')
            return False

    except requests.exceptions.ConnectionError as e:
        print(f'{url} failed. \n--{e}')
        return False

    print(f'{url} passed.')
    return True


def get_sites():
    """
    get sites from json file

    :return:
    """
    with open('sites.json', 'rb') as f:
        data = json.load(f)

    return data['sites']


if __name__ == '__main__':
    p = multiprocessing.Pool(16)
    p.imap_unordered(check_site, get_sites())
    p.close()
    p.join()
