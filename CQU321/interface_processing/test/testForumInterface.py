import unittest
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR
from CQU321.interface_processing.forum_interface import *

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class ForumInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_post_list_data = {
            'Version': '2.0',
            'Page': 0,
            'Type': 'all',
        }

    def test_get_post_list(self):
        res = get_post_list_process(Result(False, self.get_post_list_data))

        self.assertIsInstance(res.get_data(), Dict)

