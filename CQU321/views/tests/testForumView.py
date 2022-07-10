import json
import time

from configparser import ConfigParser

from django.test import SimpleTestCase, Client
from django.urls import reverse
import requests

from Website.settings import BASE_DIR
from tqdm import tqdm

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/views/tests/test.cfg')


class ForumViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_post_list_data = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'Type': 'all',
                'Page': 0,
            },
        }

    def test_get_post_list(self):
        data1 = self.get_post_list_data.copy()
        res1 = self.client.post(reverse('321CQU:get_post_list'), json.dumps(data1),
                                content_type='application/json')
        r = json.loads(res1.content)
        self.assertEqual(res1.status_code, 200)


