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


class AnnouncementViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_list = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {'Page': 0},
        }

        self.get_detail = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {'Id': 1},
        }

        self.get_group_info = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {'Name': '测试员'}
        }

        self.subscribe_group_info = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'UserName': '07102028',
                'GroupName': '321CQU',
                'Type': 1,
            }
        }

        self.subscribe_list_info = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'UserName': '07102028',
            }
        }

        self.client = Client()

    def test_get_list(self):
        data1 = self.get_list.copy()
        res1 = self.client.post(reverse('321CQU:get_announcement_list'), json.dumps(data1),
                               content_type='application/json')
        r = json.loads(res1.content)
        self.assertEqual(res1.status_code, 200)

        self.get_list['Version'] = '2.1'
        self.get_list['Params']['UserName'] = self.auth
        self.get_list['Params']['Type'] = 'subscribe'
        data2 = self.get_list.copy()
        res2 = self.client.post(reverse('321CQU:get_announcement_list'), json.dumps(data2),
                               content_type='application/json')
        r2 = json.loads(res2.content)
        self.assertEqual(res2.status_code, 200)

        self.get_list['Params']['Type'] = 'normal'
        data3 = self.get_list.copy()
        res3 = self.client.post(reverse('321CQU:get_announcement_list'), json.dumps(data3),
                                content_type='application/json')
        r3 = json.loads(res3.content)
        self.assertEqual(res3.status_code, 200)

        self.get_list['Params']['Type'] = 'group'
        data4 = self.get_list.copy()
        res4 = self.client.post(reverse('321CQU:get_announcement_list'), json.dumps(data4),
                                content_type='application/json')
        r4 = json.loads(res4.content)
        self.assertEqual(res4.status_code, 200)

    def test_get_detail(self):
        res = self.client.post(reverse('321CQU:get_announcement_detail'), json.dumps(self.get_detail),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

    def test_get_group_info(self):
        res = self.client.post(reverse('321CQU:get_group_info'), json.dumps(self.get_group_info),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

    def test_subscribe_group(self):
        res = self.client.post(reverse('321CQU:subscribe_group'), json.dumps(self.subscribe_group_info),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.subscribe_group_info['Params']['Type'] = 0
        res = self.client.post(reverse('321CQU:subscribe_group'), json.dumps(self.subscribe_group_info),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

    def test_subscribe_list(self):
        res = self.client.post(reverse('321CQU:subscribe_list'), json.dumps(self.subscribe_list_info),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

