import json
from datetime import datetime
from functools import wraps
import traceback
from typing import Dict, Tuple, Optional
import csv

from CQU321.register import FUNC_EXCEPTION_LIST
from CQU321.register.WebsiteExpection import *
from CQU321.utils.http_adapter_queue import QueueBusyException

from Website.settings import BASE_DIR

__all__ = ['Result', 'ExceptionProcessor', 'process_exception', 'log_exception_counter', 'log_exception_traceback']

NETWORK_ERROR = [ConnectionError.__name__, ConnectTimeout.__name__, ReadTimeout.__name__, QueueBusyException.__name__]


class Result:
    def __init__(self, is_exception_info: bool, data):
        self.is_exception_info = is_exception_info
        self._data = data

    def get_data(self):
        if self.is_exception_info:
            raise ExceptionNotCatch(self._data)
        return self._data

    def get_exception_info(self):
        if not self.is_exception_info:
            raise ExceptionResultNoFound
        return self._data


class ExceptionProcessor:
    @staticmethod
    def process(exception: Exception, func_name: str, params: dict = None) -> Result:
        exception_name = exception.__class__.__name__
        exception_list = FUNC_EXCEPTION_LIST.get(func_name)
        temp = []
        for arg in params['args']:
            if isinstance(arg, Result):
                if arg.is_exception_info:
                    arg = arg.get_exception_info()
                else:
                    arg = arg.get_data()
            temp.append(arg)

        params['args'] = temp

        if exception_list is None:
            log_exception_traceback(func_name, exception_name, params and json.dumps(params))
            raise NoExistFunctionName

        exception_info = exception_list.get(exception_name)
        if exception_name in NETWORK_ERROR:
            log_exception_traceback(func_name, exception_name + '_network_error', None)
            return Result(True,
                          {
                              'Statue': 0,
                              'ErrorCode': 0,
                              'ErrorInfo': '连接超时，请稍后再试'
                          })
        if exception_info is None:
            log_exception_traceback(func_name, exception_name, params and json.dumps(params))
            return Result(True, {
                'Statue': 0,
                'ErrorCode': 1,
                'ErrorInfo': '未知异常'
            })
        exception_index = {key: index
                           for index, key in enumerate(exception_list.keys())}.get(exception_name)

        log_exception_counter(func_name, exception_name)

        return Result(True,
                      {
                          'Statue': 0,
                          'ErrorCode': exception_index + 1,
                          'ErrorInfo': exception_info,
                      })


def log_exception_traceback(func_name: str, exception_name: str, params: Optional[str]):
    if params is None:
        params = ''

    if isinstance(params, Dict):
        params = json.dumps(params)

    with open(str(BASE_DIR) + '/exception_infos/' + func_name + '_exception_info.txt', 'a') as f:
        f.write(datetime.now().strftime('"%Y-%m-%d %H:%M:%S"') + '\n')
        f.write('params:\n' + params + '\n')
        f.write(traceback.format_exc())

    log_exception_counter(func_name, exception_name)


def log_exception_counter(func_name: str, exception_name: str):
    with open(str(BASE_DIR) + '/exception_counter/' + func_name + '_exception_info.csv', 'a') as cf:
        writer = csv.writer(cf)
        writer.writerow([exception_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])


def process_exception(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs) -> Result:
        try:
            if _is_exception_happened(args):
                return _get_exception_result(args)
            data = func(*args, **kwargs)
            result = Result(False, data)
        except Exception as e:
            if args or kwargs:
                params = {
                    'args': args,
                    'kwargs': kwargs
                }
            else:
                params = None
            result = ExceptionProcessor.process(e, func.__name__, params)

        return result

    return wrapped_function


def _is_exception_happened(args: Tuple) -> bool:
    for arg in args:
        if isinstance(arg, Result) and arg.is_exception_info:
            return True
    return False


def _get_exception_result(args: Tuple) -> Result:
    for arg in args:
        if isinstance(arg, Result) and arg.is_exception_info:
            return arg

    raise ExceptionResultNoFound
