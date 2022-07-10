import unittest
from typing import List, Dict

from configparser import ConfigParser

from CQU321.interface_processing.user_interface import *
from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class UserInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.binding_auth_info = {
            'Version': '2.0',
            'UserName': self.auth,
            'Password': self.password
        }

    def test_binding_auth(self):
        data1 = self.binding_auth_info.copy()
        res1 = binding_auth_process(Result(False, data1))
        self.assertIsInstance(res1.get_data(), Dict)
