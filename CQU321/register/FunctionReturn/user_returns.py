from typing import List, Dict

from .. import ParamsInfo


BINDING_AUTH_RETURNS = {
    '2.0': [
        ParamsInfo('Sid', str, '学号'),
        ParamsInfo('Name', str, '用户姓名'),
    ]
}
