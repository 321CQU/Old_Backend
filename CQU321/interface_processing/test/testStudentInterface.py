import time
import unittest
from typing import List, Dict

from configparser import ConfigParser

from CQU321.interface_processing.student_interface import *
from CQU321.utils.ExceptionProcessor import Result
from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/interface_processing/test/test.cfg')


class StudentInterfaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sid = config.get('User', 'sid')
        self.auth = config.get('User', 'auth')
        self.password = config.get('User', 'password')

        self.user_info_dict = {
            'Version': '2.0',
            'UserName': self.auth,
            'Password': self.password,
            'Sid': self.sid
        }

        self.get_score_param = self.user_info_dict.copy()
        self.get_score_param.update({
            'Version': '1.0',
            'Code': 'test',
            'NeedAll': False,
            'Debug': True,
        })

    def test_get_course_and_enrollment_v_1(self):
        self.user_info_dict['Version'] = '1.0'

        course = get_course_process(Result(False, self.user_info_dict.copy()))
        enrollment = get_enrollment_process(Result(False, self.user_info_dict.copy()))
        self.assertIsInstance(course.get_data(), Dict)
        self.assertIsInstance(enrollment.get_data(), Dict)

    def test_get_course_and_enrollment_v_2(self):
        course = get_course_process(Result(False, self.user_info_dict.copy()))
        time.sleep(1)
        enrollment = get_enrollment_process(Result(False, self.user_info_dict.copy()))
        self.assertIsInstance(course.get_data(), Dict)
        self.assertIsInstance(enrollment.get_data(), Dict)

    def test_get_gpa_ranking_v_1(self):
        self.user_info_dict['Version'] = '1.0'
        self.user_info_dict.pop('Sid')

        gpa_ranking = get_gpa_ranking_process(Result(False, self.user_info_dict))
        self.assertIsInstance(gpa_ranking.get_data(), Dict)
        self.assertIsInstance(gpa_ranking.get_data()['GpaRanking'], Dict)

    def test_get_score(self):
        score1 = get_score_process(Result(False, self.get_score_param.copy()))
        self.get_score_param['Version'] = '2.0'
        self.get_score_param.pop('NeedAll')
        score2 = get_score_process(Result(False, self.get_score_param.copy()))
        self.assertIsInstance(score1.get_data(), Dict)
        self.assertIsInstance(score2.get_data(), Dict)


if __name__ == '__main__':
    unittest.main()
