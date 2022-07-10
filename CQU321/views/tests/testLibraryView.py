import json
from configparser import ConfigParser

from Website.settings import BASE_DIR

from django.test import SimpleTestCase, Client
from django.urls import reverse

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/views/tests/test.cfg')

class LibraryViewTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.key = config.get('321CQU', 'key')
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.search_book_dict = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'UserName': self.auth,
                'Password': self.password,
                'Keyword': 'c#',
                'Page': 1,
                'OnlyHuxi': False,
            },
        }

        self.get_book_pos_dict = {
            'Key': self.key,
            'Version': '2.0',
            'Params': {
                'UserName': self.auth,
                'Password': self.password,
                'BookId': '744317275163526080',
            },
        }

        self.client = Client()

    def test_search_book(self):
        res = self.client.post(reverse('321CQU:search_book'), json.dumps(self.search_book_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)

    def test_get_book_pos(self):
        res = self.client.post(reverse('321CQU:get_book_pos'), json.dumps(self.get_book_pos_dict),
                               content_type='application/json')
        r = json.loads(res.content)
        self.assertEqual(res.status_code, 200)


