import json
from typing import Dict, List

from CQU321.register.WebsiteExpection import InfoIsNull
from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.tools import *

from CQUGetter.Getter.DeanGetter import DeanGetter

__all__ = ['binding_auth_process']


def binding_auth_v_2_0(params: Dict):
    getter = DeanGetter()
    login_access_and_update_db(getter, params['UserName'], params['Password'], True)
    url = "https://my.cqu.edu.cn/authserver/simple-user"
    res = getter.session.get(url)
    data = json.loads(res.content)
    return {
        'Sid': data['code'],
        'Name': data['name']
    }


@process_exception
def binding_auth_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': binding_auth_v_2_0
    }, params)

    data = func(params)

    result = {'Version': params.pop('Version')}
    result.update(data)

    return result
