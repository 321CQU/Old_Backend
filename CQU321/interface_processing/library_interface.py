from typing import Dict, List

from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.tools import *

from CQUGetter.Getter.LibGetter import LibGetter


__all__ = ['search_book_process', 'get_book_pos_process']


def _search_book_v_2_0(getter: LibGetter, params: Dict):
    getter.login(params['UserName'], params['Password'])
    getter.access()

    return getter.search_book(params['Keyword'], params['Page'], params['OnlyHuxi'])


@process_exception
def search_book_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': _search_book_v_2_0
    }, params)

    result = func(LibGetter(), params)

    return {
        'SearchSet': result,
        'Version': params.pop('Version')
    }


@invalid_login_cookie_process
def _get_book_pos_v_2_0(getter: LibGetter, params: Dict):
    getter.login(params['UserName'], params['Password'])
    getter.access()

    return getter.get_book_pos(params['BookId'])


@process_exception
def get_book_pos_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': _get_book_pos_v_2_0
    }, params)

    result = func(LibGetter(), params)

    return {
        'Pos': result,
        'Version': params.pop('Version')
    }
