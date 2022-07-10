import unittest
from typing import List, Dict

from configparser import ConfigParser

from CQU321.interface_processing.homepage_interface import *
from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class HomepageInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.homepage_dict = {
            'Version': '2.0'
        }

    def test_homepage(self):
        result1 = homepage_process(Result(False, self.homepage_dict.copy()))
        self.homepage_dict['Version'] = '1.0'
        result2 = homepage_process(Result(False, self.homepage_dict.copy()))
        self.homepage_dict['Version'] = '2.1'
        result3 = homepage_process(Result(False, self.homepage_dict.copy()))
        self.assertIsInstance(result1.get_data(), Dict)
        self.assertIsInstance(result2.get_data(), Dict)
        self.assertIsInstance(result3.get_data(), Dict)


if __name__ == '__main__':
    unittest.main()



