from unittest import TestCase
from src import monitoring


class MonitorTestCase(TestCase):
    def test_get_sites(self):
        sites = monitoring.get_sites()
        self.assertNotEqual(sites, None)

    def test_check_site(self):
        site = {'url': 'https://baidu.com',
                'keywords': [],
                'bad_words': []
                }
        self.assertEqual(monitoring.check_site(site), True)

    def test_check_site_wrong_url(self):
        site = {'url': 'https://kohakuuu.cc',
                'keywords': [],
                'bad_words': []
                }
        self.assertEqual(monitoring.check_site(site), False)

    def test_check_site_missing_keywords(self):
        site = {'url': 'https://kohaku.cc',
                'keywords': ['keyword'],
                'bad_words': []
                }
        self.assertEqual(monitoring.check_site(site), False)

    def test_check_site_with_keywords(self):
        site = {'url': 'https://kohaku.cc',
                'keywords': ['lalala'],
                'bad_words': []
                }
        self.assertEqual(monitoring.check_site(site), True)
