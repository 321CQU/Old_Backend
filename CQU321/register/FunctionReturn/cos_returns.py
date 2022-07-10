from typing import List, Dict

from .. import ParamsInfo

GET_COS_CREDENTIAL_RETURNS = {
    '2.0': [
        ParamsInfo('ExpiredTime', int, '临时密钥到期时间戳'),
        ParamsInfo('Expiration', str, '临时密钥到期时间'),
        ParamsInfo('Credentials', Dict, '临时密钥', [
            ParamsInfo('SessionToken', str, 'session token'),
            ParamsInfo('TmpSecretId', str, 'temp secret id'),
            ParamsInfo('TmpSecretKey', str, 'temp secret key'),
        ]),
    ]
}
