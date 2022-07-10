from mycqu.exception import IncorrectLoginCredentials
from mycqu.exception import CQUWebsiteError

from pymysql.err import OperationalError
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout


class InvalidKey(Exception):
    """当接口密钥错误时抛出"""


class UnSupportVersion(Exception):
    """当接口版本号不在支持列表中时抛出"""


class IncorrectParams(Exception):
    """当参数与配置冲突时抛出"""

    def __init__(self, str):
        super().__init__(str)


class NoExistFunctionName(Exception):
    """当函数名为未注册列表中时抛出"""


class UnregisteredException(Exception):
    """当错误未在函数错误字典中注册时抛出"""


class ExceptionResultNoFound(Exception):
    """当未在指定元组中找到错误信息时抛出"""


class ExceptionNotCatch(Exception):
    """当Result中数据出错，但试图获取时抛出"""
    def __init__(self, str):
        if str is None:
            str = ''
        super(ExceptionNotCatch, self).__init__(str)


class InfoIsNull(Exception):
    """当从教务网获取信息为空时抛出"""


class OpenidAccessError(Exception):
    """当Openid获取错误时抛出"""


class UserNotFound(Exception):
    """当查询用户不存在时抛出"""


class UnKnowError(Exception):
    """未知错误"""


class NoAuthority(Exception):
    """无权进行此操作"""
