import unittest
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR
from CQU321.interface_processing.cos_interface import *

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class CosInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_cos_credential_info = {
            'Version': '2.0',
            'Type': 'upload'
        }

    def testGetCosCredential(self):
        res = get_cos_credential_process(Result(False, self.get_cos_credential_info))

        self.assertIsInstance(res.get_data(), Dict)

