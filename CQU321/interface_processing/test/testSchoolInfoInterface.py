import unittest
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR
from CQU321.interface_processing.school_info_interface import *

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class StudentInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_fees_data = {
            'UserName': self.auth,
            'Password': self.password,
            'IsHuXi': True,
            'Room': 'B5321',
            'Version': '1.0',
        }

    def test_get_fees(self):
        res = get_fees_process(Result(False, self.get_fees_data))

        self.assertIsInstance(res, Dict)
