import json
import time

from configparser import ConfigParser

from django.test import SimpleTestCase, Client
from django.urls import reverse
import requests
from CQU321.utils.SqlProcessor import _connect_db

from Website.settings import BASE_DIR
from tqdm import tqdm

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/views/tests/test.cfg')


class HomepageViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')

        self.homepage_dict = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {},
        }

        self.client = Client()

    def test_homepage(self):
        res = self.client.post(reverse('321CQU:homepage'), json.dumps(self.homepage_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.homepage_dict.update({'Version': '2.1'})
        res = self.client.post(reverse('321CQU:homepage'), json.dumps(self.homepage_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.homepage_dict.update(self.homepage_dict.pop('Params'))
        self.homepage_dict.pop('Version')
        res = self.client.post(reverse('321CQU:homepage'), json.dumps(self.homepage_dict),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)


