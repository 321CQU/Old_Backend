from typing import List, Dict

from .. import ParamsInfo

GET_FEES_RETURNS = {
    '1.0': [
        ParamsInfo('FeesInfo', Dict, '水电费信息', [
            ParamsInfo('Amount', float, '余额'),
            ParamsInfo('Eamount', str, '电剩余补助', is_optional=True),
            ParamsInfo('Wamount', str, '水剩余补助', is_optional=True),
            ParamsInfo('Subsidies', str, '剩余补助', is_optional=True),
        ])
    ]
}
