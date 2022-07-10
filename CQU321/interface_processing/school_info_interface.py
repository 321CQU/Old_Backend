from typing import Dict, List

from CQU321.register.WebsiteExpection import InfoIsNull
from CQU321.utils.ExceptionProcessor import process_exception, Result
from CQU321.utils.SqlProcessor import SqlProcessor
from CQU321.utils.tools import *
from CQU321.utils.tools import parse_dict

from CQUGetter.Getter.CardGetter import CardGetter

__all__ = ['get_fees_process']


def get_fee_v_1_0(getter: CardGetter, params: Dict) -> Dict:
    getter.login(params['UserName'], params['Password'])
    getter.access()
    result = getter.get_fees_by_mycqu(params['IsHuXi'], params['Room'])
    if params['IsHuXi']:
        result['Eamount'] = str(result['Eamount'])
        result['Wamount'] = str(result['Wamount'])
    else:
        result['Subsidies'] = str(result['Subsidies'])
    return result


@process_exception
def get_fees_process(params: Result):
    params = params.get_data()

    func = func_select_by_version({
        '1.0': get_fee_v_1_0,
    }, params)
    data = func(CardGetter(), params)

    return {
        'FeesInfo': data,
        'Version': params.pop('Version')
    }

