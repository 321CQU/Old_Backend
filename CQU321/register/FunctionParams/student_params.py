from .. import ParamsInfo

GET_COURSE_PARAMS = {
    '1.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
    '2.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
}

GET_ENROLLMENT_PARAMS = {
    '1.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
    '2.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
}

GET_GPA_RANKING_PARAMS = {
    '1.0': [
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
    '2.0': [
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
    ],
}

GET_SCORE_PARAMS = {
    '1.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
        ParamsInfo('Code', str, 'openid获取码'),
        ParamsInfo('NeedAll', bool, '是否获取所有学期信息'),
        ParamsInfo('IsDebug', bool, '当该值置为True，Openid获取会被绕过，请仅在测试时使用', is_optional=True)
    ],
    '2.0': [
        ParamsInfo('Sid', str, '用户学号'),
        ParamsInfo('UserName', str, '统一认证账号'),
        ParamsInfo('Password', str, '统一认证密码'),
        ParamsInfo('Code', str, 'openid获取码'),
        ParamsInfo('IsDebug', bool, '当该值置为True，Openid获取会被绕过，请仅在测试时使用', is_optional=True)
    ]
}