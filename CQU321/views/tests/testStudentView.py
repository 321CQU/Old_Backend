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


class StudentViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.user_info_dict = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'UserName': self.auth,
                'Password': self.password,
                'Sid': self.sid
            },
        }

        self.get_score_param = self.user_info_dict.copy()
        self.get_score_param['Params'].update({
            'Code': 'test',
            'Debug': True,
        })

        self.client = Client()

    def test_get_course(self):
        res = self.client.post(reverse('321CQU:get_course'), json.dumps(self.user_info_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.user_info_dict.update(self.user_info_dict.pop('Params'))
        self.user_info_dict.pop('Version')
        res = self.client.post(reverse('321CQU:get_course'), json.dumps(self.user_info_dict),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_get_enrollment(self):
        res = self.client.post(reverse('321CQU:get_enrollment'), json.dumps(self.user_info_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.user_info_dict.update(self.user_info_dict.pop('Params'))
        self.user_info_dict.pop('Version')
        res = self.client.post(reverse('321CQU:get_enrollment'), json.dumps(self.user_info_dict),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_get_gpa_ranking(self):
        self.user_info_dict['Params'].pop('Sid')
        res = self.client.post(reverse('321CQU:get_gpa_ranking'), json.dumps(self.user_info_dict),
                               content_type='application/json')

        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

        self.user_info_dict.update(self.user_info_dict.pop('Params'))
        self.user_info_dict.pop('Version')
        res = self.client.post(reverse('321CQU:get_gpa_ranking'), json.dumps(self.user_info_dict),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_get_score(self):
        res1 = self.client.post(reverse('321CQU:get_score'), json.dumps(self.get_score_param),
                                content_type='application/json')
        r1 = json.loads(res1.content)
        self.assertEqual(res1.status_code, 200)

        self.get_score_param.pop('Version')
        self.get_score_param['Params']['NeedAll'] = False
        self.get_score_param.update(self.get_score_param.pop('Params'))
        res2 = self.client.post(reverse('321CQU:get_score'), json.dumps(self.get_score_param),
                                content_type='application/json')
        r2 = json.loads(res2.content)
        self.assertEqual(res2.status_code, 200)
