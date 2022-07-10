from typing import Dict, List

from CQU321.register.WebsiteExpection import UnKnowError
from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.tools import *
from utils.cos_tools import get_credential

__all__ = ['get_cos_credential_process']


def get_cos_credential_v_2_0(params: Dict):
    return get_credential(prefix='announcements/*', type=params['Type'])


@process_exception
def get_cos_credential_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '2.0': get_cos_credential_v_2_0
    }, params)

    result = func(params)

    if result is None:
        raise UnKnowError

    return {
        'Version': params.pop('Version'),
        'ExpiredTime': result['expiredTime'],
        'Expiration': result['expiration'],
        'Credentials': {
            'SessionToken': result['credentials']['sessionToken'],
            'TmpSecretId': result['credentials']['tmpSecretId'],
            'TmpSecretKey': result['credentials']['tmpSecretKey'],
        }
    }

