import json
from datetime import datetime

from configparser import ConfigParser
from typing import Dict, Tuple, List, Any, Union
from functools import wraps
import requests

from pymysql.err import MySQLError

from CQU321.utils.SqlProcessor import _connect_db, SqlProcessor
from Website.settings import BASE_DIR
from CQUGetter.Getter.CQUGetter import CQUGetter

from CQU321.utils.ExceptionProcessor import process_exception, Result, log_exception_traceback
from CQU321.register.WebsiteExpection import *
from CQU321.register.Version import FUNCTION_SUPPORT_VERSION
from CQU321.register import verify_data_same_as_registered, FUNC_EXCEPTION_LIST, \
    get_params_info_by_name

from mycqu.exception import MycquUnauthorized

config = ConfigParser()
config.read(str(BASE_DIR) + '/CQU321/utils/utils_config.cfg')

__all__ = ['post_json_analyses', 'launch_return_data', 'launch_template_data', 'func_select_by_version',
           'getter_login_and_access', 'invalid_login_cookie_process', 'get_code', 'sql_exception_process',
           'parse_dict', 'login_access_and_update_db', 'transform_query_to_dict']


def invalid_login_cookie_process(func):
    @wraps(func)
    def wrapped_function(getter: CQUGetter, params: Dict):
        try:
            return func(getter, params)
        except MycquUnauthorized:
            login_access_and_update_db(getter, params['UserName'], params['Password'], True)
            return func(getter, params)

    return wrapped_function


def sql_exception_process(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MySQLError as e:
            if args or kwargs:
                params = {
                    'args': args,
                    'kwargs': kwargs
                }
            else:
                params = None
            log_exception_traceback('sql_error', e.__class__.__name__, params)

    return wrapped_function


def get_code(code: str, is_debug: bool):
    if is_debug:
        return code
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'
    res = requests.get(url.format(config.get('Weixin_App_Setting', 'appid'),
                                  config.get('Weixin_App_Setting', 'secret'),
                                  code))
    try:
        open_id = json.loads(res.content)['openid']
    except:
        with open('./code_get_error', 'ab') as f:
            f.write(res.content)
        open_id = None
    return open_id


@process_exception
def post_json_analyses(post_data, func_name: str) -> Dict:
    data = json.loads(post_data)
    _verify_key(data.get('Key'))
    data.pop('Key')
    version = _verify_or_creat_version(data.get('Version'), func_name)
    if data.get('Version'):
        data.pop('Version')
    data = data if version == '1.0' else data.get('Params')

    verify_data_same_as_registered(data, func_name, version, False)

    data['Version'] = version

    return data


def launch_return_data(return_data: Result, func_name: str) -> Dict:
    if return_data.is_exception_info:
        return return_data.get_exception_info()

    return_data = return_data.get_data()
    version = return_data.pop('Version')

    verify_data_same_as_registered(return_data, func_name, version, True)
    if float(version) >= 2.0:
        return {
            'Statue': 1,
            'data': return_data
        }
    else:
        temp = {'Statue': 1}
        temp.update(return_data)
        return temp


def launch_template_data(title: str, func_name: str, version: str) -> Dict:
    return {
        'title': title,
        'versions': _launch_version_info(func_name),
        'input_params': _launch_param_info(func_name, version, False),
        'return_params': _launch_param_info(func_name, version, True),
        'error_info': _launch_error_info(func_name),
    }


def getter_login_and_access(getter: CQUGetter, params: Dict, need_access: bool = True):
    db_result = _get_login_cookie_by_username(params['UserName'])

    if db_result is None:
        login_access_and_update_db(getter, params['UserName'], params['Password'], need_access)
    else:
        if _is_login_cookie_expired(str(db_result[1])):
            login_access_and_update_db(getter, params['UserName'], params['Password'], need_access)
        else:
            getter.set_login_cookie(db_result[0])


def func_select_by_version(version_func: Dict, params: Dict):
    for key, value in version_func.items():
        if key == params['Version']:
            return value

    raise UnSupportVersion


def _launch_param_info(func_name: str, version: str, is_return_params: bool) -> List[Dict]:
    if version is None:
        version = _get_version_list(func_name)[-1]
    params_info_list = get_params_info_by_name(func_name, version, is_return_params)

    result = []
    for param_info in params_info_list:
        result.extend(param_info.print())

    return result


def _launch_error_info(func_name: str) -> List:
    exception_list = FUNC_EXCEPTION_LIST.get(func_name)
    if exception_list is None:
        raise UnregisteredException

    result = []
    for name, info in exception_list.items():
        index = {key: i for i, key in enumerate(exception_list.keys())}.get(name)
        temp = {'error_code': index + 1, 'error_info': info}
        result.append(temp)

    return result


def _launch_version_info(func_name) -> List[Dict]:
    versions = FUNCTION_SUPPORT_VERSION.get(func_name)
    if versions is None:
        raise UnregisteredException

    result = []
    for version in versions:
        temp = {
            'link': "?version=" + version,
            'name': version
        }
        result.append(temp)

    return result


def _verify_key(key: str) -> None:
    if key != config.get("Website", "key"):
        raise InvalidKey


def _verify_or_creat_version(version: str, func_name: str) -> str:
    if version is None:
        return '1.0'

    if version not in _get_version_list(func_name):
        raise UnSupportVersion

    return version


def _get_version_list(func_name: str) -> List:
    versions = FUNCTION_SUPPORT_VERSION.get(func_name)
    if versions is None:
        raise UnregisteredException
    return versions


def _is_login_cookie_expired(update_date: str) -> bool:
    update_date = datetime.strptime(update_date, "%Y-%m-%d %H:%M:%S")
    if (datetime.now() - update_date).days >= 7:  # 7 * 24 * 3600
        return True
    else:
        return False


def login_access_and_update_db(getter: CQUGetter, username: str, password: str, is_access: bool):
    getter.login(username, password)
    if is_access:
        getter.access()
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        authorization = getter.get_login_cookie()
        process = SqlProcessor()
        process.execute("call UpdateLoginCookie(%s, %s, %s)", (username, authorization, now_time))


def _get_login_cookie_by_username(username: str):
    connection, cursor = _connect_db()
    sql = "select Cookie, UpdateTime from LoginCookie where UserName = %s"
    cursor.execute(sql, (username,))
    return cursor.fetchone()


def parse_dict(dicts: List[Dict], need_pop: List[str] = None, name_change: Dict = None, move_as_key: str = None) -> \
        Tuple[Union[List[Dict], Dict[str, List]], Dict[str, List[Any]]]:
    result = []
    pop_item = {}
    if need_pop:
        for t in need_pop:
            pop_item[t] = []
    for item in dicts:
        temp = {}
        if need_pop:
            for t in need_pop:
                pop_item[t].append(item.pop(t))

        if name_change:
            for k, v in name_change.items():
                item[v] = item.pop(k)

        if move_as_key:
            temp[item.pop(move_as_key)] = item
            result.append(temp)
            continue
        result.append(item)

    if move_as_key:
        temp = {}
        for item in result:
            for key, value in item.items():
                if key in temp.keys():
                    temp[key].append(value)
                else:
                    temp[key] = [value]

        result = temp

    return result, pop_item


def transform_query_to_dict(query: List, keys: List) -> List[Dict]:
    result = []

    for i in range(len(query)):
        temp = {}
        for j in range(len(keys)):
            temp[keys[j]] = str(query[i][j])
        result.append(temp)

    return result

