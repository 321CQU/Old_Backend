import unittest
from configparser import ConfigParser
from typing import Dict

from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR
from CQU321.interface_processing.announcement_interface import *

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class AnnouncementInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.get_announcement_list = {
            'Version': '2.0',
            'Page': 0,
        }

        self.get_announcement_detail = {
            'Version': '2.0',
            'Id': 1,
        }

        self.get_group_info = {
            'Version': '2.0',
            'Name': '测试员',
        }

        self.subscribe_group_info = {
            'Version': '2.0',
            'Sid': self.sid,
            'GroupName': '321CQU',
        }

        self.subscribe_list_info = {
            'Version': '2.0',
            'Sid': self.sid,
        }

    def test_get_announcement_detail(self):
        res = get_announcement_detail_process(Result(False, self.get_announcement_detail))

        self.assertIsInstance(res.get_data(), Dict)

    def test_get_announcement_list(self):
        data1 = self.get_announcement_list.copy()
        res1 = get_announcement_list_process(Result(False, data1))

        self.get_announcement_list['Version'] = '2.1'
        self.get_announcement_list['UserName'] = self.auth
        self.get_announcement_list['Type'] = 'subscribe'
        data2 = self.get_announcement_list.copy()
        res2 = get_announcement_list_process(Result(False, data2))

        self.get_announcement_list['Type'] = 'normal'
        data3 = self.get_announcement_list.copy()
        res3 = get_announcement_list_process(Result(False, data3))

        self.get_announcement_list['Type'] = 'group'
        data4 = self.get_announcement_list.copy()
        res4 = get_announcement_list_process(Result(False, data4))

        self.assertIsInstance(res1.get_data(), Dict)
        self.assertIsInstance(res2.get_data(), Dict)
        self.assertIsInstance(res3.get_data(), Dict)
        self.assertIsInstance(res4.get_data(), Dict)

    def test_get_group_info(self):
        res = get_group_info_process(Result(False, self.get_group_info))

        self.assertIsInstance(res.get_data(), Dict)

    def test_subscribe_group(self):
        test_info1 = self.subscribe_group_info.copy()
        test_info1['Type'] = 1
        test_info2 = self.subscribe_group_info.copy()
        test_info2['Type'] = 0
        res1 = subscribe_group_process(Result(False, test_info1))
        res2 = subscribe_group_process(Result(False, test_info2))

        return None

    def test_subscribe_list(self):
        res = subscribe_list_process(Result(False, self.subscribe_list_info))

        self.assertIsInstance(res.get_data(), Dict)


if __name__ == '__main__':
    unittest.main()
