from .. import ParamsInfo

GET_FEES_PARAMS = {
    '1.0': [
        ParamsInfo('UserName', str, '统一身份认证账号'),
        ParamsInfo('Password', str, '统一身份认证密码'),
        ParamsInfo('IsHuXi', bool, '是否为虎溪校区水电费'),
        ParamsInfo('Room', str, '房间号'),
    ]
}
