import json
import time

from configparser import ConfigParser

from django.test import SimpleTestCase, Client
from django.urls import reverse

from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/views/tests/test.cfg')


class UserViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')
        self.client = Client()

        self.binding_auth_info = {
            'Version': '2.0',
            'Key': self.key,
            'Params': {
                'UserName': self.auth,
                'Password': self.password,
            }
        }

    def test_binding_auth(self):
        res = self.client.post(reverse('321CQU:bind_auth'), json.dumps(self.binding_auth_info),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

