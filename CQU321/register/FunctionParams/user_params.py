from .. import ParamsInfo

BINDING_AUTH_PARAMS = {
    '2.0': [
        ParamsInfo('UserName', str, '统一身份认证号'),
        ParamsInfo('Password', str, '统一身份认证密码'),
    ]
}
