import json
from configparser import ConfigParser

from Website.settings import BASE_DIR

from django.test import SimpleTestCase, Client
from django.urls import reverse

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/views/tests/test.cfg')


class SchoolInfoViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_fees_data = {
            'Key': self.key,
            'Version': '1.0',
            'UserName': self.auth,
            'Password': self.password,
            'Room': 'b5321',
            'IsHuXi': True,
        }

    def test_get_fees(self):
        res = self.client.post(reverse('321CQU:get_fees'), json.dumps(self.get_fees_data),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

