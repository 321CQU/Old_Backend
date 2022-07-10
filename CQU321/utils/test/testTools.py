import json
import unittest
from configparser import ConfigParser

from CQU321.utils.tools import post_json_analyses
from Website.settings import BASE_DIR

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/utils/utils_Config.cfg')


class ToolsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.post_data = {
            'Key': config.get("Website", "key"),
            'Version': '2.0',
            'Params': {
                'Sid': "test",
                'UserName': "test",
                'Password': "test",
            }
        }

        self.except_result = {
            'Version': '2.0',
            'Sid': "test",
            'UserName': "test",
            'Password': "test",
        }

    def test_post_json_analyses(self):
        result = post_json_analyses(json.dumps(self.post_data), 'get_course_process')

        self.assertDictEqual(self.except_result, result.get_data())

    def test_post_json_analyses_without_version(self):
        self.post_data.update({
            'Sid': "test",
            'UserName': "test",
            'Password': "test",
        })
        self.post_data.pop('Params')
        self.post_data.pop('Version')
        self.except_result['Version'] = '1.0'
        result = post_json_analyses(json.dumps(self.post_data), 'get_course_process')

        self.assertDictEqual(self.except_result, result.get_data())

    def test_post_json_analyses_with_error_key(self):
        except_result = self._init_error_dict(1, '无效的接口密钥')

        self.post_data.update({
            'Key': "*******"
        })
        result1 = post_json_analyses(json.dumps(self.post_data), 'get_course_process')

        self.post_data.pop('Key')
        result2 = post_json_analyses(json.dumps(self.post_data), 'get_course_process')

        self.assertDictEqual(except_result, result1.get_exception_info())
        self.assertDictEqual(except_result, result2.get_exception_info())

    def test_post_json_analyses_with_error_version(self):
        self.post_data.update({
            'Version': '3.0'
        })

        except_result = self._init_error_dict(2, '错误的版本号')

        result = post_json_analyses(json.dumps(self.post_data), 'get_course_process')
        self.assertDictEqual(except_result, result.get_exception_info())

    def test_post_json_analyses_with_error_params(self):
        self.post_data['Params'].pop('Sid')
        except_result = self._init_error_dict(3, '错误的请求参数')

        result = post_json_analyses(json.dumps(self.post_data), 'get_course_process')
        self.assertDictEqual(except_result, result.get_exception_info())

    @staticmethod
    def _init_error_dict(error_code: int, error_info: str):
        return {
            'Statue': 0,
            'ErrorCode': error_code,
            'ErrorInfo': error_info
        }


if __name__ == '__main__':
    unittest.main()
