import unittest
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR
from CQU321.interface_processing.library_interface import *

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class StudentInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.search_book_dict = {
            'Version': '2.0',
            'UserName': self.auth,
            'Password': self.password,
            'Keyword': '深度学习',
            'Page': 1,
            'OnlyHuxi': True,
        }

        self.get_book_pos_dict = {
            'Version': '2.0',
            'UserName': self.auth,
            'Password': self.password,
            'BookId': '744317275163526080',
        }

    def test_search_book(self):
        res = search_book_process(Result(False, self.search_book_dict))

        self.assertIsInstance(res, Dict)

    def test_get_book_pos(self):
        res = get_book_pos_process(Result(False, self.get_book_pos_dict))

        self.assertIsInstance(res, Dict)


if __name__ == '__main__':
    unittest.main()

